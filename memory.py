import os
import json
from collections import deque
from typing import List, Dict, Optional, Any

# Carpeta predeterminada para guardar las memorias
CARPETA_MEMORIAS = "memorias"

def asegurar_carpeta_destino():
    """Asegura que exista la carpeta para guardar las memorias."""
    if not os.path.exists(CARPETA_MEMORIAS):
        os.makedirs(CARPETA_MEMORIAS)


class MemoriaCorta:
    """
    Gestiona la memoria a corto plazo (búfer rotativo de mensajes).
    """
    def __init__(self, max_msg: int = 20):
        # max_msg: número de mensajes a retener.
        # Al excederse, deque elimina automáticamente el elemento más antiguo.
        self.memory: deque = deque(maxlen=max_msg)

    def agregar_mensaje(self, role: str, content: str, tool_calls: Optional[List] = None, name: Optional[str] = None) -> Optional[Dict]:
        """
        Añade un mensaje. Si la memoria está llena, devuelve el mensaje
        que ha sido expulsado para que la Memoria a Medio Plazo pueda procesarlo.
        """
        expulsado = None
        if len(self.memory) == self.memory.maxlen:
            expulsado = self.memory[0]  # El elemento más antiguo que va a salir

        nuevo_msg = {"role": role, "content": content}
        if tool_calls is not None:
            nuevo_msg["tool_calls"] = tool_calls
        if name is not None:
            nuevo_msg["name"] = name

        self.memory.append(nuevo_msg)
        return expulsado

    def obtener_mensajes(self) -> List[Dict]:
        return list(self.memory)

    def vaciar(self):
        self.memory.clear()


class MemoriaMedioPlazo:
    """
    Gestiona resúmenes episódicos y hechos clave (cuaderno de notas activas).
    """
    def __init__(self):
        self.resumenes_episodicos: List[str] = []
        self.hechos_clave: Dict[str, Any] = {
            "temas_activos": [],
            "preferencias_usuario": {},
            "metas_actuales": []
        }

    def agregar_resumen(self, resumen: str):
        if resumen and resumen not in self.resumenes_episodicos:
            self.resumenes_episodicos.append(resumen)

    def actualizar_hecho(self, categoria: str, clave: str, valor: Any):
        if categoria in self.hechos_clave:
            if isinstance(self.hechos_clave[categoria], dict):
                self.hechos_clave[categoria][clave] = valor
            elif isinstance(self.hechos_clave[categoria], list):
                if valor not in self.hechos_clave[categoria]:
                    self.hechos_clave[categoria].append(valor)

    def generar_prompt_contexto(self) -> str:
        """Genera el bloque que se inyectará dinámicamente en el sistema."""
        contexto = []
        if self.resumenes_episodicos:
            contexto.append("### Lo que hemos hablado recientemente (Resumen):")
            for res in self.resumenes_episodicos[-3:]:  # Limitamos a los últimos 3 resúmenes
                contexto.append(f"- {res}")
        
        preferencias = self.hechos_clave.get("preferencias_usuario", {})
        temas = self.hechos_clave.get("temas_activos", [])
        
        if preferencias or temas:
            contexto.append("\n### Notas sobre el usuario y el proyecto:")
            if temas:
                contexto.append(f"- Temas de interés activos: {', '.join(temas)}")
            for k, v in preferencias.items():
                contexto.append(f"- {k}: {v}")
                
        return "\n".join(contexto)


# --- Funciones de Cristalización y Carga Requeridas ---

def cristalizar(memoria_corta: MemoriaCorta, memoria_medio: MemoriaMedioPlazo, nombre: Optional[str] = None) -> str:
    """Guarda ambas memorias en un único archivo JSON en la carpeta predeterminada."""
    asegurar_carpeta_destino()
    nombre_archivo = nombre or "sesion_agente.json"
    if not nombre_archivo.endswith(".json"):
        nombre_archivo += ".json"
        
    ruta_completa = os.path.join(CARPETA_MEMORIAS, nombre_archivo)
    
    datos = {
        "max_msg": memoria_corta.memory.maxlen,
        "memoria_corta": memoria_corta.obtener_mensajes(),
        "memoria_medio": {
            "resumenes": memoria_medio.resumenes_episodicos,
            "hechos": list(memoria_medio.hechos_clave.items())
        }
    }
    
    with open(ruta_completa, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)
        
    return ruta_completa

def cargar_memoria(nombre_archivo: str) -> Optional[Dict[str, Any]]:
    """Carga los datos guardados desde la carpeta predeterminada."""
    if not nombre_archivo.endswith(".json"):
        nombre_archivo += ".json"
        
    ruta_completa = os.path.join(CARPETA_MEMORIAS, nombre_archivo)
    
    if not os.path.exists(ruta_completa):
        print(f"⚠️ Archivo no encontrado en: {ruta_completa}")
        return None
        
    with open(ruta_completa, "r", encoding="utf-8") as f:
        return json.load(f)