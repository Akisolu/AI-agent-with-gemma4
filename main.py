"""
main.py - Interfaz de usuario por consola.
"""

from chat import chat, guardar_sesion, cargar_sesion
import os


SALIDA = ("salir", "exit", "quit", "bye")


def mostrar_ayuda():
    print("""
Comandos especiales:
  /guardar [nombre]     - Guarda la conversacion actual
  /cargar <nombre>      - Carga una conversacion guardada
  /ayuda                - Muestra esta ayuda
  salir                 - Termina el programa
""")


def main():
    os.system("cls")
    print("=" * 60)
    print("  Chat con Gemma 4 + Tools + Memoria Persistente")
    print("=" * 60)
    print("Escribe /ayuda para ver comandos especiales")
    print("=" * 60)
    print()

    while True:
        user_input = input("Tu: ").strip()

        if not user_input:
            continue

        # --- COMANDOS ESPECIALES ---
        if user_input.lower() == "/ayuda":
            mostrar_ayuda()
            continue

        if user_input.lower().startswith("/guardar"):
            partes = user_input.split(" ", 1)
            nombre = partes[1] if len(partes) > 1 else None
            ruta = guardar_sesion(nombre=nombre)
            print(f"Guardado en: {ruta}\n")
            continue

        if user_input.lower().startswith("/cargar"):
            partes = user_input.split(" ", 1)
            if len(partes) < 2:
                print("Uso: /cargar <nombre_archivo>\n")
                continue
            if cargar_sesion(partes[1]):
                print("Sesion cargada. Continuando conversacion...\n")
            continue

        # --- SALIR ---
        if user_input.lower() in SALIDA:
            print("Guardando sesion automaticamente...")
            guardar_sesion(metadata={"fin": "sesion_normal"})
            print("Hasta luego")
            break

        # --- CHAT NORMAL ---
        chat(user_input)


if __name__ == "__main__":
    main()