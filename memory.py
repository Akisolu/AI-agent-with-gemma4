"""
memory.py - Cristaliza (guarda) la memoria del agente en archivos JSON.
"""

import json
import os
from datetime import datetime


# Carpeta donde se guardan las memorias
MEMORIA_DIR = "memoria"


def _asegurar_carpeta():
    """Crea la carpeta de memorias si no existe."""
    if not os.path.exists(MEMORIA_DIR):
        os.makedirs(MEMORIA_DIR)


def _generar_nombre_archivo():
    """Genera un nombre unico basado en fecha y hora."""
    ahora = datetime.now()
    return f"sesion_{ahora.strftime('%Y-%m-%d_%H-%M-%S')}.json"


def _limpiar_memoria(memoria):
    """
    Convierte la memoria a formato JSON-serializable.
    Los ToolCall de Ollama se convierten a diccionarios simples.
    """
    memoria_limpia = []
    
    for msg in memoria:
        msg_limpio = {
            "role": msg.get("role", "unknown"),
            "content": msg.get("content", "")
        }
        
        # Convertir tool_calls si existen
        tool_calls_raw = msg.get("tool_calls")
        if tool_calls_raw:
            tool_calls_limpios = []
            for tc in tool_calls_raw:
                # Si es un objeto ToolCall de Ollama, convertirlo
                if hasattr(tc, "function"):
                    tool_calls_limpios.append({
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    })
                # Si ya es un diccionario, usarlo directamente
                elif isinstance(tc, dict):
                    tool_calls_limpios.append(tc)
            
            if tool_calls_limpios:
                msg_limpio["tool_calls"] = tool_calls_limpios
        
        # Incluir otros campos si existen
        if "name" in msg:
            msg_limpio["name"] = msg["name"]
        
        memoria_limpia.append(msg_limpio)
    
    return memoria_limpia


def cristalizar(memoria, nombre=None, metadata=None):
    """
    Guarda la memoria del agente en un archivo JSON.
    
    Args:
        memoria: Lista de mensajes (la memoria del chat)
        nombre: Nombre personalizado del archivo (opcional)
        metadata: Dict con info extra (opcional)
    
    Returns:
        Ruta del archivo guardado
    """
    _asegurar_carpeta()
    
    nombre_archivo = nombre or _generar_nombre_archivo()
    if not nombre_archivo.endswith(".json"):
        nombre_archivo += ".json"
    
    ruta = os.path.join(MEMORIA_DIR, nombre_archivo)
    
    # Limpiar la memoria antes de guardar
    memoria_limpia = _limpiar_memoria(memoria)
    
    # Preparar el contenido a guardar
    datos = {
        "timestamp": datetime.now().isoformat(),
        "total_mensajes": len(memoria_limpia),
        "metadata": metadata or {},
        "memoria": memoria_limpia
    }
    
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    
    print(f"Memoria cristalizada en: {ruta}")
    return ruta


def cargar_memoria(nombre_archivo):
    """
    Carga una memoria guardada desde un archivo JSON.
    
    Args:
        nombre_archivo: Nombre del archivo (con o sin .json)
    
    Returns:
        Lista de mensajes (memoria), o None si no existe
    """
    if not nombre_archivo.endswith(".json"):
        nombre_archivo += ".json"
    
    ruta = os.path.join(MEMORIA_DIR, nombre_archivo)
    
    if not os.path.exists(ruta):
        print(f"No se encontro: {ruta}")
        return None
    
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    print(f"Memoria cargada desde: {ruta}")
    print(f"   Fecha original: {datos.get('timestamp', 'desconocida')}")
    print(f"   Mensajes: {datos.get('total_mensajes', 0)}")
    
    return datos["memoria"]


def listar_memorias():
    """Muestra todas las memorias guardadas."""
    _asegurar_carpeta()
    
    archivos = [f for f in os.listdir(MEMORIA_DIR) if f.endswith(".json")]
    
    if not archivos:
        print("No hay memorias guardadas.")
        return []
    
    print(f"Memorias guardadas ({len(archivos)}):")
    for i, archivo in enumerate(sorted(archivos), 1):
        ruta = os.path.join(MEMORIA_DIR, archivo)
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        fecha = datos.get("timestamp", "desconocida")[:19].replace("T", " ")
        mensajes = datos.get("total_mensajes", 0)
        meta = datos.get("metadata", {})
        meta_str = f" | {meta}" if meta else ""
        
        print(f"   {i}. {archivo} ({mensajes} msgs, {fecha}){meta_str}")
    
    return archivos


def ver_memoria(nombre_archivo):
    """
    Muestra el contenido de una memoria de forma legible.
    
    Args:
        nombre_archivo: Nombre del archivo a visualizar
    """
    if not nombre_archivo.endswith(".json"):
        nombre_archivo += ".json"
    
    ruta = os.path.join(MEMORIA_DIR, nombre_archivo)
    
    if not os.path.exists(ruta):
        print(f"No se encontro: {ruta}")
        return
    
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
    
    print("=" * 60)
    print(f"MEMORIA: {nombre_archivo}")
    print(f"Guardada: {datos.get('timestamp', 'desconocida')}")
    print(f"Total mensajes: {datos.get('total_mensajes', 0)}")
    
    meta = datos.get("metadata", {})
    if meta:
        print(f"Metadata: {meta}")
    
    print("=" * 60)
    
    for i, msg in enumerate(datos["memoria"], 1):
        rol = msg.get("role", "desconocido")
        contenido = msg.get("content", "")
        
        # Truncar contenido muy largo para visualizacion
        if len(contenido) > 200:
            contenido = contenido[:200] + " [...]"
        
        print(f"\n[{i}] {rol.upper()}")
        print(f"    {contenido}")
        
        # Mostrar tool_calls si existen
        if "tool_calls" in msg:
            for tc in msg["tool_calls"]:
                nombre_func = tc.get("function", {}).get("name", "unknown")
                args = tc.get("function", {}).get("arguments", {})
                print(f"    Tool: {nombre_func}({args})")
    
    print("\n" + "=" * 60)


def borrar_memoria(nombre_archivo):
    """Elimina un archivo de memoria."""
    if not nombre_archivo.endswith(".json"):
        nombre_archivo += ".json"
    
    ruta = os.path.join(MEMORIA_DIR, nombre_archivo)
    
    if os.path.exists(ruta):
        os.remove(ruta)
        print(f"Memoria borrada: {nombre_archivo}")
    else:
        print(f"No existe: {nombre_archivo}")