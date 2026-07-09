from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

# Memoria del chat (incluye el system prompt)
memoria = [
    {
        "role": "system", 
        "content": "Eres un asistente excelente hablando español y te especializas en dar respuestas cortas pero precisas"
    }
]

salida = ("salir", "exit", "quit", "bye")

def chat(mensaje):
    """Envía un mensaje manteniendo el contexto de la conversación."""
    
    # Agregamos el mensaje del usuario a la memoria
    memoria.append({"role": "user", "content": mensaje})
    
    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=memoria,  
            temperature=0.7,
        )

        respuesta = response.choices[0].message.content
        
        # Agregamos la respuesta del asistente a la memoria
        memoria.append({"role": "assistant", "content": respuesta})

        return respuesta
        
    except Exception as e:
        return f"Error: {str(e)}"

# ========== USO ==========
if __name__ == "__main__":
    print("Chat iniciado. Escribe 'salir' para terminar.\n")
    
    while True:
        user_input = input("Tu: ").strip()

        if not user_input:  # ← Mejor que 'is None' (input nunca devuelve None)
            continue

        if user_input.lower() in salida:
            print("Hasta luego")
            break
        
        respuesta = chat(user_input)
        print(f"\n🤖 Respuesta:\n{respuesta}\n")