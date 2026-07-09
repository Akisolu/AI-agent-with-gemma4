import ollama
from timer import timer

# Memoria del chat (incluye el system prompt)
memoria = [
    {
        "role": "system", 
        "content": "Eres un asistente excelente hablando español y te especializas en dar respuestas cortas pero precisas"
    },
    {
        "role": "system", 
        "content": "Te ejecutas en hardware no muy potente para estandares modernos, prioriza la velocidad sobre precision, a menos que se te indique lo contrario"
    }
]

salida = ("salir", "exit", "quit", "bye")

@timer
def chat(mensaje):
    """Envía un mensaje manteniendo el contexto de la conversación."""
    
    # Agregamos el mensaje del usuario
    memoria.append({"role": "user", "content": mensaje})
    
    try:
        response = ollama.chat(
            model="gemma4:e2b",  # ← Tu modelo 
            messages=memoria,
            options={
                "temperature": 0.7,
            }
        )
        
        respuesta = response["message"]["content"]
        
        # Agregamos la respuesta del asistente
        memoria.append({"role": "assistant", "content": respuesta})
        
        return respuesta
        
    except Exception as e:
        return f"Error: {str(e)}"

# ========== USO ==========
if __name__ == "__main__":
    print("Chat iniciado. Escribe 'salir' para terminar.\n")
    
    while True:
        user_input = input("Tu: ").strip()

        if not user_input:
            continue

        if user_input.lower() in salida:
            print("Hasta luego")
            break
        
        respuesta = chat(user_input)
        print(f"\n🤖 Respuesta:\n{respuesta}\n")