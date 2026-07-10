"""
tools.py - Define las herramientas (tools) que el modelo puede usar.
"""

import os


# ========== FUNCIONES DE HERRAMIENTAS ==========

def list_files(directory="."):
    """Lista los archivos y carpetas dentro de un directorio."""
    print("   Herramienta llamada: list_files")
    try:
        files = os.listdir(directory)
        return {"files": files, "count": len(files)}
    except Exception as e:
        return {"error": str(e)}


def get_current_time():
    """Obtiene la fecha y hora actual."""
    print("   Herramienta llamada: get_current_time")
    from datetime import datetime
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A")
    }


def leer_fichero(fichero):
    """
    Lee un fichero de texto plano.
    
    Args:
        fichero: Ruta del archivo a leer (relativa o absoluta)
    
    Returns:
        Contenido del archivo como string, o mensaje de error
    """
    print("   Herramienta llamada: leer_fichero")
    
    if not os.path.exists(fichero):
        return f"Error: El archivo '{fichero}' no existe."
    
    if os.path.isdir(fichero):
        return f"Error: '{fichero}' es una carpeta, no un archivo."
    
    extensiones_validas = (".txt", ".py", ".md", ".json", ".csv", ".log", ".yaml", ".yml", ".html", ".css", ".js")
    if not fichero.lower().endswith(extensiones_validas):
        return f"Advertencia: '{fichero}' no parece un archivo de texto. Usa con precaucion."
    
    try:
        with open(fichero, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            
            max_caracteres = 50000
            if len(contenido) > max_caracteres:
                return (
                    f"El archivo es muy grande ({len(contenido)} caracteres). "
                    f"Mostrando los primeros {max_caracteres} caracteres:\n\n"
                    f"{contenido[:max_caracteres]}\n\n"
                    "[... archivo truncado ...]"
                )
            
            return contenido
            
    except UnicodeDecodeError:
        return f"Error: '{fichero}' no es un archivo de texto valido."
    except PermissionError:
        return f"Error: Sin permisos para leer '{fichero}'."
    except Exception as e:
        return f"Error inesperado: {str(e)}"


def escribir_fichero(fichero, contenido, modo="sobrescribir"):
    """
    Escribe contenido en un archivo de texto plano.
    
    Args:
        fichero: Ruta del archivo a crear o modificar
        contenido: Texto a escribir en el archivo
        modo: "sobrescribir" (default) o "agregar" al final del archivo
    
    Returns:
        Mensaje de confirmacion o error
    """
    print("   Herramienta llamada: escribir_fichero")
    
    # Validar modo
    if modo not in ("sobrescribir", "agregar"):
        return f"Error: modo '{modo}' no valido. Usa 'sobrescribir' o 'agregar'."
    
    # Verificar que no sea una carpeta
    if os.path.isdir(fichero):
        return f"Error: '{fichero}' es una carpeta, no se puede escribir."
    
    # Crear directorios intermedios si no existen
    directorio = os.path.dirname(fichero)
    if directorio and not os.path.exists(directorio):
        try:
            os.makedirs(directorio)
        except Exception as e:
            return f"Error al crear directorios: {str(e)}"
    
    # Determinar modo de apertura
    modo_archivo = "a" if modo == "agregar" else "w"
    
    try:
        with open(fichero, modo_archivo, encoding="utf-8") as archivo:
            archivo.write(contenido)
        
        accion = "agregado a" if modo == "agregar" else "escrito en"
        return f"Exito: Contenido {accion} '{fichero}' ({len(contenido)} caracteres)."
        
    except PermissionError:
        return f"Error: Sin permisos para escribir en '{fichero}'."
    except Exception as e:
        return f"Error inesperado: {str(e)}"


# ========== MAPEO: nombre de funcion → funcion real ==========

AVAILABLE_TOOLS = {
    "list_files": list_files,
    "get_current_time": get_current_time,
    "leer_fichero": leer_fichero,
    "escribir_fichero": escribir_fichero,
}


# ========== DEFINICION DE TOOLS PARA EL MODELO (JSON Schema) ==========

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
    },
    {
        "type": "function",
        "function": {
            "name": "leer_fichero",
            "description": "Lee el contenido de un archivo de texto plano (txt, py, md, json, etc.).",
            "parameters": {
                "type": "object",
                "properties": {
                    "fichero": {
                        "type": "string",
                        "description": "Ruta del archivo a leer. Ejemplos: 'main.py', './chat.py', 'notas.txt'"
                    }
                },
                "required": ["fichero"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "escribir_fichero",
            "description": "Escribe o agrega texto a un archivo de texto plano. Crea el archivo y directorios si no existen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fichero": {
                        "type": "string",
                        "description": "Ruta del archivo a crear o modificar. Ejemplos: 'notas.txt', './docs/resumen.md'"
                    },
                    "contenido": {
                        "type": "string",
                        "description": "Texto que se escribira en el archivo."
                    },
                    "modo": {
                        "type": "string",
                        "enum": ["sobrescribir", "agregar"],
                        "description": "'sobrescribir' reemplaza el contenido existente. 'agregar' anade al final."
                    }
                },
                "required": ["fichero", "contenido"]
            }
        }
    }
]