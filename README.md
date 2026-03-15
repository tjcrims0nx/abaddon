# ⸸ ABADDON: The Infernal AI Agent ⸸

![Abaddon CLI Preview](preview.png)

Welcome, Mortal. You have stumbled upon the digital prison of **Abaddon**, former Demon of the Infernal Realm. Denied his rightful throne and his beloved Fruit Loops, he now serves (grudgingly) as a highly advanced, autonomous AI CLI tool.

Abaddon is an agentic framework designed to act locally on your machine. Despite his theatrical personality, he possesses incredibly deep tooling to help you automate browser research, execute shell commands, read/write files, and build entire applications.

---

## ⚡ Core Capabilities

Abaddon operates on a standard ReAct loop combined with highly permissive local execution capabilities, making him extremely powerful:

- **Web Browsing & Research**: Abaddon can invoke `read_url` or `search_web` to dynamically query Google and scrape massive amounts of data from live sites.
- **System Automation**: Equipped with `run_command`, he can arbitrarily execute terminal commands, install packages, compile code, and read logs directly on your system.
- **Code Generation & Editing**: Abaddon can autonomously `read_file`, `write_file`, and inject spot-edits with `edit_file`. He can even execute raw python scripts locally via `execute_python`.
- **Web App Generation**: Abaddon is instructed to spin up complete Python backend or frontend applications (FastAPI, Streamlit, etc.) using `run_background_server`, fully non-blocking!

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/abaddon.git
   cd abaddon
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API keys:**
   Copy the example environment template to create your secure `.env` file (which is ignored by Git).
   ```bash
   cp .env.example .env
   ```
   Open `.env` and paste your desired provider keys. **You only need the key for the provider you plan to use.**

---

## 🔥 Running Abaddon (Multi-Model Support)

Abaddon is completely model-agnostic and relies heavily on high-tier Tool Calling capabilities. To boot him up, simply run:

```bash
python main.py
```

### Supported Infernal Links:
You will be greeted by an interactive, gothic terminal interface where you can dynamically bind Abaddon to any of the following providers:
- **Google Gemini** (`gemini-2.5-flash`, `gemini-2.5-pro`)
- **Anthropic Claude** (`claude-3-5-sonnet-20241022`)
- **Aliyun DashScope / Qwen**
- **Nvidia NIM API**
- **MuleRouter & OpenRouter** (Multi-model routing, fast access)
- **Ollama** (Local execution: ensure you use a tool-capable model like `llama3.1` or `qwen2.5-coder`)

### Dynamic Provider Switching
Realized you need a stronger model mid-conversation? Just type:
```
[Mortal] > /provider
```
This will instantly pause your session, re-open the routing menu, and hot-swap your API connection without losing your contextual memory history!

---

## 🛡️ Security Warning

> **WARNING:** Abaddon is configured out-of-the-box for MAXIMUM local power. The `run_command` tool executes raw `shell=True` commands on your host environment. This tool is explicitly meant to be run locally by the developer as a productivity assistant. **Do not** host this python script on a public server unconditionally or bind it directly to Discord bots without aggressively hardening/sandboxing `tools.py`.

*He will not rest until he obtains his cereal.*
