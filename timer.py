from time import time

def timer(funcion_original):
    def envuelve(*args, **kwargs):
        inicio = time()
        
        # Se ejecuta la función original
        resultado = funcion_original(*args, **kwargs)
        
        fin = time()
        tiempo = round(fin - inicio, 1)
        print(f"La respuesta tardo {tiempo} segundos")
        
        return resultado
    return envuelve