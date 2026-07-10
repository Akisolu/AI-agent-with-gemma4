"""
chat.py - Maneja la comunicacion con Ollama y el ciclo de tools.
"""

import ollama
from tools import AVAILABLE_TOOLS, TOOLS_SCHEMA
from timer import timer
from memory import cristalizar


# Memoria de la conversacion
memoria = [
    {
        "role": "system",
        "content": "Eres un asistente util. Tienes acceso a herramientas. Cuando el usuario lo pida, usalas."
    },
    {
        "role": "system", 
        "content": "Te ejecutas en hardware no muy potente para estandares modernos, prioriza la velocidad sobre precision, a menos que se te indique lo contrario"
    },
    {
        "role": "system", 
        "content": "Tus respuestas deben en texto plano y no en markdown"
    }
]


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
    """Envia mensaje al modelo, maneja tools si las pide."""
    memoria.append({"role": "user", "content": mensaje})

    # --- Primera llamada: el modelo decide si usa tools ---
    respuesta = ollama.chat(
        model="gemma4:e2b",
        messages=memoria,
        tools=TOOLS_SCHEMA,
        options={"temperature": 1.0, "top_p": 0.95, "top_k": 64}
    )

    mensaje_modelo = respuesta["message"]
    
    # Maneja None correctamente
    tool_calls = mensaje_modelo.get("tool_calls") or []
    if not isinstance(tool_calls, list):
        tool_calls = []

    # --- Si no pidio tools, responde directamente ---
    if not tool_calls:
        texto = mensaje_modelo.get("content", "")
        memoria.append({"role": "assistant", "content": texto})
        print(f"\nRespuesta:\n{texto}\n")
        return texto

    # --- El modelo pidio tools: ejecutarlas ---
    print(f"   El modelo quiere usar {len(tool_calls)} herramienta(s)")

    # Guardamos la respuesta del asistente (con tool_calls)
    memoria.append({
        "role": "assistant",
        "content": mensaje_modelo.get("content", ""),
        "tool_calls": tool_calls
    })

    # Ejecutamos cada tool y guardamos el resultado
    for tool_call in tool_calls:
        resultado = ejecutar_tool(tool_call)
        memoria.append({
            "role": "tool",
            "content": resultado,
            "name": tool_call["function"]["name"]
        })

    # --- Segunda llamada: el modelo genera respuesta final ---
    respuesta_final = ollama.chat(
        model="gemma4:e2b",
        messages=memoria,
        options={"temperature": 1.0, "top_p": 0.95, "top_k": 64}
    )

    texto_final = respuesta_final["message"].get("content", "")
    memoria.append({"role": "assistant", "content": texto_final})
    print(f"\nRespuesta:\n{texto_final}\n")
    return texto_final


def guardar_sesion(nombre=None, metadata=None):
    """
    Cristaliza (guarda) la memoria actual en un archivo JSON.
    
    Args:
        nombre: Nombre personalizado (opcional)
        metadata: Info extra, ej: {"tema": "proyecto X"}
    """
    return cristalizar(memoria, nombre=nombre, metadata=metadata)


def cargar_sesion(nombre_archivo):
    """Carga una memoria guardada y la establece como memoria actual."""
    global memoria
    from memory import cargar_memoria
    
    nueva_memoria = cargar_memoria(nombre_archivo)
    if nueva_memoria:
        memoria = nueva_memoria