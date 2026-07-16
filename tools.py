"""
tools.py - Define las herramientas (tools) que el modelo puede usar.
"""

import os
import shutil


# ========== FUNCIONES DE HERRAMIENTAS: ARCHIVOS ==========

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
    
    if modo not in ("sobrescribir", "agregar"):
        return f"Error: modo '{modo}' no valido. Usa 'sobrescribir' o 'agregar'."
    
    if os.path.isdir(fichero):
        return f"Error: '{fichero}' es una carpeta, no se puede escribir."
    
    directorio = os.path.dirname(fichero)
    if directorio and not os.path.exists(directorio):
        try:
            os.makedirs(directorio)
        except Exception as e:
            return f"Error al crear directorios: {str(e)}"
    
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


def editar_fichero(fichero, texto_viejo, texto_nuevo):
    """
    Reemplaza una parte del contenido de un archivo.
    
    Args:
        fichero: Ruta del archivo a editar
        texto_viejo: Texto a buscar y reemplazar
        texto_nuevo: Texto nuevo que reemplaza al viejo
    
    Returns:
        Mensaje de confirmacion o error
    """
    print("   Herramienta llamada: editar_fichero")
    
    if not os.path.exists(fichero):
        return f"Error: El archivo '{fichero}' no existe."
    
    if os.path.isdir(fichero):
        return f"Error: '{fichero}' es una carpeta, no un archivo."
    
    try:
        with open(fichero, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        
        if texto_viejo not in contenido:
            return f"Error: No se encontro el texto a reemplazar en '{fichero}'."
        
        nuevo_contenido = contenido.replace(texto_viejo, texto_nuevo, 1)
        
        with open(fichero, "w", encoding="utf-8") as archivo:
            archivo.write(nuevo_contenido)
        
        return f"Exito: Archivo '{fichero}' editado. Reemplazado 1 ocurrencia."
        
    except PermissionError:
        return f"Error: Sin permisos para editar '{fichero}'."
    except Exception as e:
        return f"Error inesperado: {str(e)}"


def mover_fichero(origen, destino):
    """
    Mueve un archivo de una ubicacion a otra.
    
    Args:
        origen: Ruta actual del archivo
        destino: Nueva ruta del archivo
    
    Returns:
        Mensaje de confirmacion o error
    """
    print("   Herramienta llamada: mover_fichero")
    
    if not os.path.exists(origen):
        return f"Error: El archivo origen '{origen}' no existe."
    
    if os.path.isdir(origen):
        return f"Error: '{origen}' es una carpeta. Usa mover_carpeta para carpetas."
    
    if os.path.exists(destino):
        return f"Error: Ya existe algo en '{destino}'. Borralo primero o usa otro nombre."
    
    directorio = os.path.dirname(destino)
    if directorio and not os.path.exists(directorio):
        try:
            os.makedirs(directorio)
        except Exception as e:
            return f"Error al crear directorio destino: {str(e)}"
    
    try:
        shutil.move(origen, destino)
        return f"Exito: Archivo movido de '{origen}' a '{destino}'."
    except Exception as e:
        return f"Error al mover: {str(e)}"


def borrar_fichero(fichero):
    """
    Elimina un archivo permanentemente.
    
    Args:
        fichero: Ruta del archivo a borrar
    
    Returns:
        Mensaje de confirmacion o error
    """
    print("   Herramienta llamada: borrar_fichero")
    
    if not os.path.exists(fichero):
        return f"Error: El archivo '{fichero}' no existe."
    
    if os.path.isdir(fichero):
        return f"Error: '{fichero}' es una carpeta. Usa borrar_carpeta para carpetas."
    
    try:
        os.remove(fichero)
        return f"Exito: Archivo '{fichero}' eliminado permanentemente."
    except PermissionError:
        return f"Error: Sin permisos para borrar '{fichero}'."
    except Exception as e:
        return f"Error inesperado: {str(e)}"


# ========== FUNCIONES DE HERRAMIENTAS: CARPETAS ==========

def crear_carpeta(ruta):
    """
    Crea una carpeta y sus subcarpetas si no existen.
    
    Args:
        ruta: Ruta de la carpeta a crear
    
    Returns:
        Mensaje de confirmacion o error
    """
    print("   Herramienta llamada: crear_carpeta")
    
    if os.path.exists(ruta):
        if os.path.isdir(ruta):
            return f"Advertencia: La carpeta '{ruta}' ya existe."
        else:
            return f"Error: '{ruta}' ya existe como archivo."
    
    try:
        os.makedirs(ruta)
        return f"Exito: Carpeta '{ruta}' creada."
    except Exception as e:
        return f"Error al crear carpeta: {str(e)}"


def renombrar_carpeta(origen, destino):
    """
    Cambia el nombre de una carpeta.
    
    Args:
        origen: Nombre o ruta actual de la carpeta
        destino: Nuevo nombre o ruta de la carpeta
    
    Returns:
        Mensaje de confirmacion o error
    """
    print("   Herramienta llamada: renombrar_carpeta")
    
    if not os.path.exists(origen):
        return f"Error: La carpeta '{origen}' no existe."
    
    if not os.path.isdir(origen):
        return f"Error: '{origen}' no es una carpeta."
    
    if os.path.exists(destino):
        return f"Error: Ya existe '{destino}'. Usa otro nombre."
    
    try:
        os.rename(origen, destino)
        return f"Exito: Carpeta renombrada de '{origen}' a '{destino}'."
    except Exception as e:
        return f"Error al renombrar: {str(e)}"


def mover_carpeta(origen, destino):
    """
    Mueve una carpeta a otra ubicacion.
    
    Args:
        origen: Ruta actual de la carpeta
        destino: Nueva ruta de la carpeta
    
    Returns:
        Mensaje de confirmacion o error
    """
    print("   Herramienta llamada: mover_carpeta")
    
    if not os.path.exists(origen):
        return f"Error: La carpeta '{origen}' no existe."
    
    if not os.path.isdir(origen):
        return f"Error: '{origen}' no es una carpeta."
    
    if os.path.exists(destino):
        return f"Error: Ya existe '{destino}'. Borralo primero o usa otro nombre."
    
    try:
        shutil.move(origen, destino)
        return f"Exito: Carpeta movida de '{origen}' a '{destino}'."
    except Exception as e:
        return f"Error al mover carpeta: {str(e)}"


def borrar_carpeta(ruta, forzar=False):
    """
    Elimina una carpeta y todo su contenido.
    
    Args:
        ruta: Ruta de la carpeta a borrar
        forzar: Si es True, borra aunque no este vacia. Default False.
    
    Returns:
        Mensaje de confirmacion o error
    """
    print("   Herramienta llamada: borrar_carpeta")
    
    if not os.path.exists(ruta):
        return f"Error: La carpeta '{ruta}' no existe."
    
    if not os.path.isdir(ruta):
        return f"Error: '{ruta}' no es una carpeta."
    
    try:
        if forzar:
            shutil.rmtree(ruta)
            return f"Exito: Carpeta '{ruta}' y todo su contenido eliminados."
        else:
            os.rmdir(ruta)
            return f"Exito: Carpeta vacia '{ruta}' eliminada."
    except OSError:
        return f"Error: La carpeta '{ruta}' no esta vacia. Usa forzar=True para borrar todo."
    except Exception as e:
        return f"Error inesperado: {str(e)}"


# ========== FUNCIONES EXISTENTES ==========

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

import requests
from time import sleep

def _api_dolar_bcv():
    # El API oficial de DolarApi para el dólar BCV
    url = "https://ve.dolarapi.com/v1/dolares/oficial"
    try:
        # Añadimos un timeout para que no se quede colgado esperando eternamente
        consulta = requests.get(url, timeout=5)
        if consulta.status_code == 200:
            return consulta.json()
    except requests.RequestException:
        # Si hay un error de red o timeout, atrapamos el error aquí
        pass
    return None

def consultar_dolar_bcv():
    # Sistema de reintentos
    tries = 0
    result = None

    while tries <= 3:
        if tries > 0:
            # Espera progresiva antes de reintentar (0.5s, 1.0s, 1.5s)
            tiempo_espera = tries * 0.5
            print(f"Reintentando en {tiempo_espera} segundos...")
            sleep(tiempo_espera)

        result = _api_dolar_bcv()

        # Si conseguimos los datos con éxito, rompemos el bucle
        if result is not None:
            break

        # Incrementamos, falle por red o falle por respuesta del servidor
        tries += 1

    if result:
        return (f"Tasa BCV: {result.get('promedio')} Bs.")
    else:
        return "No se pudo obtener la tasa después de 3 intentos."



# ========== MAPEO: nombre de funcion → funcion real ==========

AVAILABLE_TOOLS = {
    "list_files": list_files,
    "get_current_time": get_current_time,
    "leer_fichero": leer_fichero,
    "escribir_fichero": escribir_fichero,
    "editar_fichero": editar_fichero,
    "mover_fichero": mover_fichero,
    "borrar_fichero": borrar_fichero,
    "crear_carpeta": crear_carpeta,
    "renombrar_carpeta": renombrar_carpeta,
    "mover_carpeta": mover_carpeta,
    "borrar_carpeta": borrar_carpeta,
    "consultar_dolar_bcv": consultar_dolar_bcv,
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
            "description": "Crea o sobrescribe un archivo de texto plano. Crea directorios si no existen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fichero": {
                        "type": "string",
                        "description": "Ruta del archivo. Ejemplos: 'notas.txt', './docs/resumen.md'"
                    },
                    "contenido": {
                        "type": "string",
                        "description": "Texto a escribir en el archivo."
                    },
                    "modo": {
                        "type": "string",
                        "enum": ["sobrescribir", "agregar"],
                        "description": "'sobrescribir' reemplaza todo. 'agregar' anade al final."
                    }
                },
                "required": ["fichero", "contenido"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "editar_fichero",
            "description": "Reemplaza una parte especifica del texto dentro de un archivo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fichero": {
                        "type": "string",
                        "description": "Ruta del archivo a editar."
                    },
                    "texto_viejo": {
                        "type": "string",
                        "description": "Texto exacto a buscar y reemplazar."
                    },
                    "texto_nuevo": {
                        "type": "string",
                        "description": "Texto nuevo que reemplaza al viejo."
                    }
                },
                "required": ["fichero", "texto_viejo", "texto_nuevo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mover_fichero",
            "description": "Mueve un archivo a otra ubicacion o cambia su nombre.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origen": {
                        "type": "string",
                        "description": "Ruta actual del archivo."
                    },
                    "destino": {
                        "type": "string",
                        "description": "Nueva ruta o nombre del archivo."
                    }
                },
                "required": ["origen", "destino"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "borrar_fichero",
            "description": "Elimina permanentemente un archivo. No se puede deshacer.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fichero": {
                        "type": "string",
                        "description": "Ruta del archivo a eliminar."
                    }
                },
                "required": ["fichero"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crear_carpeta",
            "description": "Crea una carpeta nueva y sus subcarpetas si no existen.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ruta": {
                        "type": "string",
                        "description": "Ruta de la carpeta a crear. Ejemplos: 'proyecto', './docs/imagenes'"
                    }
                },
                "required": ["ruta"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "renombrar_carpeta",
            "description": "Cambia el nombre de una carpeta existente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origen": {
                        "type": "string",
                        "description": "Nombre o ruta actual de la carpeta."
                    },
                    "destino": {
                        "type": "string",
                        "description": "Nuevo nombre o ruta de la carpeta."
                    }
                },
                "required": ["origen", "destino"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "mover_carpeta",
            "description": "Mueve una carpeta completa a otra ubicacion.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origen": {
                        "type": "string",
                        "description": "Ruta actual de la carpeta."
                    },
                    "destino": {
                        "type": "string",
                        "description": "Nueva ruta de la carpeta."
                    }
                },
                "required": ["origen", "destino"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "borrar_carpeta",
            "description": "Elimina una carpeta. Si no esta vacia, requiere forzar=True.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ruta": {
                        "type": "string",
                        "description": "Ruta de la carpeta a eliminar."
                    },
                    "forzar": {
                        "type": "boolean",
                        "description": "Si es True, borra la carpeta y todo su contenido. Default False."
                    }
                },
                "required": ["ruta"]
            }
        }
    },
    {
    "type": "function", 
    "function": {
        "name": "consultar_dolar_bcv", 
        "description": "Una funcion que permite consultar el precio de cambio del USD a BS (Bolivar venezolano) usando la tasa oficial del BCV",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
    }
]