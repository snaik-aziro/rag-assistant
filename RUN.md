# Release Dashboard AI Assistant — Quick Run Guide

## 1. Prerequisites

- macOS or Linux terminal (Windows WSL works too)
- Python 3.9+ available as `python3`
- [Ollama](https://ollama.ai/download) installed (`ollama --version` should work)

## 2. Start Ollama (LLM runtime)

In a dedicated terminal:

```bash
ollama serve
```

Keep this terminal running in the background.

If you have not already downloaded the model, run once:

```bash
ollama pull llama2
```

You can replace `llama2` with any other model from the Ollama library.

## 3. Launch the Web UI

In a new terminal (macOS/Linux):

```bash
cd /Users/sagar.naik/Desktop/local-llm
./run_ui.sh
```

On Windows (PowerShell or Command Prompt):

```powershell
cd C:\Users\sagar.naik\Desktop\local-llm
run_ui_windows.bat
```

What the scripts do:

1. Creates a local virtual environment in `.venv` (if missing)
2. Installs `requirements.txt`
3. Verifies Ollama is reachable on `http://localhost:11434`
4. Starts the Flask web server on port `5002`

Open http://localhost:5002 in your browser to use the assistant.

> Tip: set a different port by exporting `PORT`, e.g. `PORT=6000 ./run_ui.sh`.

## 4. Terminal Chatbot (optional)

If you prefer the CLI experience:

```bash
source .venv/bin/activate
python src/chatbot.py
```

Use `/quit` to exit, `/model <name>` to switch models, and `/clear` to reset history.

## 5. Stopping the Services

- Stop the web UI: `Ctrl+C` in the terminal running `run_ui.sh`
- Stop Ollama: `Ctrl+C` in the terminal running `ollama serve`

---

Need help? Check `README.md` for full documentation or run `python src/app.py --help` for advanced options.

