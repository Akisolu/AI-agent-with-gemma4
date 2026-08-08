# 🤖 Local AI Agent with Gemma 4 (Function Calling & Persistence)

*🇪🇸 [Leer en español](README.es.md)*

An interactive artificial intelligence agent developed in Python that runs **100% locally** using **Ollama** and the **Gemma4:e2b** model.

The system natively implements **Tool Use / Function Calling** via JSON schemas, manages **persistent short- and mid-term memory**, and includes an automated timers system for deferred tool execution.

---

## ✨ Key Features

* **🔒 100% Local & Private Execution:** Built on the local **Ollama** API (compatible with `gemma4:e2b`).
* **🛠️ Dynamic Function Calling / Tool Use:**
  * **File System:** Modular reading, writing, creation, deletion, and listing of files and folders.
  * **Web / API Integration:** Real-time lookup of the official dollar price (BCV) via an external API.
  * **Timers System:** Creation of asynchronous background timers (`timer.py`) to trigger notifications or tasks after a time interval.
* **🧠 Persistent Memory:**
  * **Short-Term Memory:** Maintains the context of the current conversation.
  * **Mid-Term Memory:** Persistent storage of key data to remember important information across sessions.
* **⚡ Latency and Performance Measurement:** Real-time monitoring of model response times per interaction.

---

## 🛠️ Technologies Used

* **Language:** Python 3.14
* **LLM Engine:** Ollama (`ollama-python`)
* **HTTP Requests:** `requests`
* **Schema Format:** JSON Schema for tool definition and invocation.

---

## 📂 Architecture and Code Structure

```text
├── main.py              # Main interaction loop (REPL) and performance measurement
├── chat.py              # Chat engine, Function Calling parsing and tool dispatch
├── memory.py            # Context window manager for short/mid-term memory
├── tools.py             # Native function implementations (Files, Dollar API, Timers)
├── timer.py             # Asynchronous execution of timers in background threads
├── tools_esquema.json   # Formal JSON Schema definitions for available tools
└── dependencias.txt     # Project dependencies
```

## 🚀 Installation and Usage Guide
### Prerequisites
* Have [Ollama](https://ollama.com/) installed and running on your system.
* Download the desired model (for example, `gemma4:e2b`):
> [!NOTE]  
> **About models:**  
> This project used `gemma4:e2b`, however any Ollama model with tool-use capability should work; you may need to edit `chat.py` at line `51` and change the model name manually.

### Installation Steps
1. Clone the repository:
```bash
    git clone https://github.com/Aki-new/agente-de-IA-con-gemma4.git
    cd agente-de-IA-con-gemma4
```
2. Create and activate a virtual environment:
   
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
3. Install dependencies:
```bash
    pip install -r dependencias.txt
```
4. Run the agent
```bash
    python main.py
```

## 📝 Special Agent Commands
During the interactive conversation you can use the following commands in the terminal:
* `salir` / `exit`: End the current session.
* `limpiar memoria`: Clear the current session history from the database.
* `memoria`: Show the messages currently stored in the context.
