"""
main.py - Interfaz de usuario por consola.
"""

from chat import chat
import os


SALIDA = ("salir", "exit", "quit", "bye")


def main():
    os.system("cls")
    print("=" * 50)
    print("  Chat con Gemma 4 + Tools")
    print("=" * 50)
    print("Ejemplos de uso:")
    print("  - 'Muestra los archivos de esta carpeta'")
    print("  - '¿Qué hora es?'")
    print("  - 'salir' para terminar")
    print("=" * 50)
    print()

    while True:
        user_input = input("Tu: ").strip()

        if not user_input:
            continue

        if user_input.lower() in SALIDA:
            print("Hasta luego")
            break

        chat(user_input)


if __name__ == "__main__":
    main()