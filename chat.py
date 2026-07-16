"""
chat.py - Maneja la comunicacion con Ollama y el ciclo de tools usando memoria a corto y medio plazo.
"""

import ollama
from tools import AVAILABLE_TOOLS, TOOLS_SCHEMA
from timer import timer
from memory import MemoriaCorta, MemoriaMedioPlazo, cristalizar, cargar_memoria

# Inicializamos las estructuras de memoria
memoria_c = MemoriaCorta() # Ajusta max_msg a tu hardware (10-12 suele ser rápido y útil)
memoria_m = MemoriaMedioPlazo()

# Prompts de sistema estables
SYSTEM_PROMPTS_BASE = [
    "Eres un asistente util. Tienes acceso a herramientas. Cuando el usuario lo pida, usalas.",
    "Te ejecutas en hardware no muy potente para estandares modernos, prioriza la velocidad sobre precision, a menos que se te indique lo contrario",
    "Tus respuestas deben en texto plano y no en markdown"
]


def consolidar_mensaje_expulsado(mensaje_expulsado: dict):
    """
    Analiza un mensaje descartado de la memoria corta y extrae 
    información valiosa para guardarla a medio plazo.
    """
    if not mensaje_expulsado or mensaje_expulsado.get("role") == "system":
        return

    rol = mensaje_expulsado.get("role", "").upper()
    contenido = mensaje_expulsado.get("content", "").strip()
    
    if not contenido or len(contenido) < 3:
        return

    print(f"\n[MMP] Analizando mensaje expulsado de {rol} para memoria a medio plazo...")

    # Creamos un prompt de extracción mucho más agresivo y claro
    prompt_analisis = (
        "Analiza el siguiente mensaje de un chat y extrae un dato clave (ej. el nombre del usuario, "
        "su lenguaje de programación, gustos, o un resumen muy corto de lo que hizo).\n"
        "REGLA: Responde ÚNICAMENTE con la información extraída en una sola frase corta, directa y sin rodeos. "
        "Si el mensaje no contiene información útil que valga la pena recordar, responde exactamente con la palabra 'OMITIR'.\n\n"
        f"Mensaje de {rol}: \"{contenido}\"\n"
        "Dato extraído:"
    )

    try:
        # Llamada rápida con baja temperatura
        res = ollama.chat(
            model="gemma4:e2b",
            messages=[{"role": "user", "content": prompt_analisis}],
            options={"temperature": 0.0, "num_predict": 40}  # Temp 0 para evitar divagaciones
        )
        
        nota = res["message"].get("content", "").strip()
        
        # Ignoramos respuestas vacías o las que el modelo decida omitir
        if not nota or "omitir" in nota.lower():
            print("[MMP] Mensaje descartado por falta de datos relevantes.")
            return

        print(f"[MMP] Información detectada: '{nota}'")

        # Clasificación inteligente de la nota en la memoria a medio plazo
        nota_lower = nota.lower()
        if any(x in nota_lower for x in ["llamo", "nombre es", "mi nombre"]):
            # Extraer y guardar nombre directamente en las preferencias
            memoria_m.actualizar_hecho("preferencias_usuario", "nombre_usuario", nota)
        elif any(x in nota_lower for x in ["gusta", "prefiero", "programo en", "lenguaje", "interes"]):
            memoria_m.actualizar_hecho("preferencias_usuario", "preferencia_detectada", nota)
        else:
            # Guardar como resumen general de la conversación
            memoria_m.agregar_resumen(nota)

    except Exception as e:
        # Ahora sí te avisará en consola si hay un problema de conexión o timeout con Ollama
        print(f"⚠️ [MMP] Error al procesar la memoria a medio plazo: {str(e)}")

def preparar_mensajes_para_ollama() -> list:
    """
    Construye la lista final de mensajes inyectando los System Prompts 
    y la memoria a medio plazo en el flujo del modelo.
    """
    lista_mensajes = []
    
    # Agregar instrucciones base del sistema
    for p in SYSTEM_PROMPTS_BASE:
        lista_mensajes.append({"role": "system", "content": p})
        
    # Inyectar el bloque de notas de la memoria a medio plazo
    notas_medio_plazo = memoria_m.generar_prompt_contexto()
    if notas_medio_plazo:
        lista_mensajes.append({
            "role": "system", 
            "content": f"Memoria de apoyo sobre el contexto de sesiones anteriores:\n{notas_medio_plazo}"
        })
        
    # Agregar el búfer dinámico de memoria a corto plazo
    lista_mensajes.extend(memoria_c.obtener_mensajes())
    return lista_mensajes


def ejecutar_tool(tool_call):
    """Ejecuta una herramienta y devuelve el resultado."""
    nombre = tool_call["function"]["name"]
    argumentos = tool_call["function"]["arguments"]

    if nombre in AVAILABLE_TOOLS:
        try:
            resultado = AVAILABLE_TOOLS[nombre](**argumentos)
            return str(resultado)
        except Exception as e:
            return f"Error: {str(e)}"
    else:
        return f"Herramienta '{nombre}' no encontrada."


@timer
def chat(mensaje):
    """
    Envia mensaje al modelo y maneja un ciclo recursivo (bucle) de herramientas
    hasta que el modelo decida responder directamente.
    """
    # 1. Añadimos el mensaje del usuario a la memoria a corto plazo
    expulsado = memoria_c.agregar_mensaje("user", mensaje)
    if expulsado:
        consolidar_mensaje_expulsado(expulsado)

    # Definimos un límite máximo de iteraciones para evitar bucles infinitos
    MAX_ITERACIONES = 5
    iteracion = 0

    while iteracion < MAX_ITERACIONES:
        # Preparamos el contexto actualizado con todo el historial hasta el momento
        mensajes_completos = preparar_mensajes_para_ollama()

        # Llamada al modelo pasando el esquema de herramientas
        respuesta = ollama.chat(
            model="gemma4:e2b",
            messages=mensajes_completos,
            tools=TOOLS_SCHEMA,
            options={"temperature": 0.3, "top_p": 0.95, "top_k": 64}  # Bajamos temperatura para mayor precisión en tools
        )

        mensaje_modelo = respuesta["message"]
        tool_calls = mensaje_modelo.get("tool_calls") or []
        if not isinstance(tool_calls, list):
            tool_calls = []

        # --- CASO 1: El modelo NO pide más herramientas, genera respuesta final ---
        if not tool_calls:
            texto_final = mensaje_modelo.get("content", "")
            expulsado = memoria_c.agregar_mensaje("assistant", texto_final)
            if expulsado:
                consolidar_mensaje_expulsado(expulsado)
                
            print(f"\nRespuesta Final:\n{texto_final}\n")
            return texto_final

        # --- CASO 2: El modelo solicita ejecutar una o más herramientas ---
        print(f"   [Iteración {iteracion + 1}] El modelo quiere usar {len(tool_calls)} herramienta(s)")
        
        # Registramos la intención del asistente con las tool_calls en la memoria
        expulsado = memoria_c.agregar_mensaje(
            role="assistant", 
            content=mensaje_modelo.get("content", "") or "", 
            tool_calls=tool_calls
        )
        if expulsado:
            consolidar_mensaje_expulsado(expulsado)

        # Ejecutamos secuencialmente cada herramienta solicitada en este paso
        for tool_call in tool_calls:
            nombre_tool = tool_call["function"]["name"]
            print(f"   -> Ejecutando herramienta: {nombre_tool}")
            
            resultado = ejecutar_tool(tool_call)
            
            # Guardamos el resultado de la herramienta en la memoria
            expulsado = memoria_c.agregar_mensaje(
                role="tool", 
                content=resultado, 
                name=nombre_tool
            )
            if expulsado:
                consolidar_mensaje_expulsado(expulsado)

        # Incrementamos el contador y el bucle continuará, obligando al modelo a evaluar 
        # los nuevos resultados de las herramientas en la siguiente iteración.
        iteracion += 1

    # Si llega al límite de seguridad
    error_msg = "Se ha alcanzado el límite máximo de ejecución de herramientas consecutivas."
    print(f"\n⚠️ {error_msg}\n")
    return error_msg


def guardar_sesion(nombre=None, metadata=None, **kwargs):
    """
    Cristaliza (guarda) la memoria actual en un archivo JSON 
    dentro de la carpeta predeterminada 'memorias'.
    
    Soporta argumentos adicionales como 'metadata' para evitar 
    errores de compatibilidad con main.py al cerrar el programa.
    """
    # Si en el futuro quieres hacer algo con la metadata, puedes añadirla aquí
    ruta = cristalizar(memoria_c, memoria_m, nombre=nombre)
    print(f"💾 Sesión guardada con éxito en: {ruta}")
    return ruta


def cargar_sesion(nombre_archivo):
    """Carga la memoria desde un archivo JSON en la carpeta predeterminada."""
    datos = cargar_memoria(nombre_archivo)
    if datos:
        # Restauramos la memoria a corto plazo
        memoria_c.vaciar()
        for msg in datos.get("memoria_corta", []):
            memoria_c.agregar_mensaje(
                role=msg["role"],
                content=msg["content"],
                tool_calls=msg.get("tool_calls"),
                name=msg.get("name")
            )
        
        # Restauramos la memoria a medio plazo
        datos_m = datos.get("memoria_medio", {})
        memoria_m.resumenes_episodicos = datos_m.get("resumenes", [])
        
        # Reconstruir el diccionario de hechos desde la lista guardada
        hechos_lista = datos_m.get("hechos", [])
        memoria_m.hechos_clave = dict(hechos_lista)
        
        print(f"🔌 Sesión '{nombre_archivo}' cargada con éxito.")