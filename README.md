# 🤖 Agente de IA Local con Gemma 4 (Function Calling & Persistencia)

Un agente de inteligencia artificial interactivo desarrollado en Python que se ejecuta **100% en local** utilizando **Ollama** y el modelo **Gemma4:e2b**. 

El sistema implementa de forma nativa la capacidad de **Tool Use / Function Calling** mediante esquemas JSON, gestión de **memoria persistente** a corto y mediano plazo, y un sistema automatizado de temporizadores (*timers*) para la ejecución diferida de herramientas.

---

## ✨ Características Principales

* **🔒 Ejecución 100% Local & Privada:** Desarrollado sobre la API local de **Ollama** (compatible con `gemma4:e2b`).
* **🛠️ Function Calling / Tool Use Dinámico:**
  * **Sistema de Archivos:** Lectura, escritura, creación, eliminación y listado modular de archivos y carpetas.
  * **Integración Web / APIs:** Consulta en tiempo real del precio del dólar oficial (BCV) mediante consumo de API externa.
  * **Sistema de Temporizadores:** Creación de *timers* asíncronos en segundo plano (`timer.py`) para ejecutar avisos o tareas tras un intervalo de tiempo.
* **🧠 Memoria Persistente:**
  * **Memoria a Corto Plazo:** Mantenimiento del contexto de la conversación actual.
  * **Memoria a Mediano Plazo:** Almacenamiento persistente de datos clave para recordar información importante entre distintas sesiones.
* **⚡ Medición de Latencia y Rendimiento:** Monitoreo en tiempo real del tiempo de respuesta del modelo por cada interacción.

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.14
* **Motor LLM:** Ollama (`ollama-python`)
* **Peticiones HTTP:** `requests`
* **Formato de Esquemas:** JSON Schema para definición e invocación de herramientas.

---

## 📂 Arquitectura y Estructura del Código

```text
├── main.py              # Bucle principal de interacción (REPL) y medición de rendimiento
├── chat.py              # Motor del chat, parsing de Function Calling y despacho de herramientas
├── memory.py            # Gestor de ventana de contexto para memoria a corto/mediano plazo
├── tools.py             # Implementación nativa de funciones (Archivos, API Dólar, Timers)
├── timer.py             # Ejecución asíncrona de temporizadores en hilos secundarios
├── tools_esquema.json   # Definición formal en JSON Schema de las herramientas disponibles
└── dependencias.txt     # Dependencias del proyecto
```

## 🚀 Guía de Instalación y Uso
### Prerrequisitos
* Tener [Ollama](https://ollama.com/) instalado y ejecutándose en tu sistema.
* Descargar el modelo deseado (por ejemplo `gemma4:e2b`):
> [!NOTE]  
> **Sobre los modelos:**  
> En este proyecto se uso `gemma4:e2b`, sin embargo cualquier modelo de ollama con la capacidad de usar `tools` deberia funcionar, solo necesitaria ir a `chat.py` linea `51` y cambiar manualmente el nombre del modelo

### Pasos de Instalación
1. Clonar el repositorio:
```bash
    git clone https://github.com/Aki-new/agente-de-IA-con-gemma4.git
    cd agente-de-IA-con-gemma4
```
2. Crear y activar el entorno virtual:
   
   * Windows:
     ```bash
         python -m venv .venv
         .venv\Scripts\activate
     ```
   * Linux / macOS:
     ```bash
        python3 -m venv .venv
        source .venv/bin/activate
     ```
3. Instalar dependencias:
```bash
    pip install -r dependencias.txt
```
4. Ejecutar el agente
```bash
    python main.py
```

## 📝 Comandos Especiales del Agente
Durante la conversación interactiva puedes usar los siguientes comandos en la terminal:
* `salir` / `exit`: Finaliza la sesión actual.
* `limpiar memoria`: Borra el historial de la sesión actual de la base de datos.
* `memoria`: Muestra los mensajes almacenados actualmente en el contexto.
