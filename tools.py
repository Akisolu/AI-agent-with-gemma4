"""
tools.py - Define las herramientas (tools) que el modelo puede usar.
Cada herramienta es una función Python + su definición en formato JSON Schema.
"""

import os


# ========== FUNCIONES DE HERRAMIENTAS ==========

def list_files(directory="."):
    """Lista los archivos de una carpeta."""
    print("    Herramienta llamada: list_files")
    try:
        files = os.listdir(directory)
        return {"files": files, "count": len(files)}
    except Exception as e:
        return {"error": str(e)}


def get_current_time():
    """Obtiene la fecha y hora actual."""
    print("    Herramienta llamada: get_current_time")
    from datetime import datetime
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A")
    }


# ========== MAPEO: nombre de función → función real ==========

AVAILABLE_TOOLS = {
    "list_files": list_files,
    "get_current_time": get_current_time,
}


# ========== DEFINICIÓN DE TOOLS PARA EL MODELO (JSON Schema) ==========

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lista los archivos y carpetas dentro de un directorio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Ruta del directorio. Por defecto es el directorio actual."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Obtiene la fecha y hora actual del sistema.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]