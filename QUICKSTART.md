# Quick Start Guide

## 🚀 Fastest Way to Get Started

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Install Ollama
**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from [ollama.ai](https://ollama.ai/download)

### Step 3: Start Ollama Service
```bash
ollama serve
```
Keep this terminal open, or run it in the background.

### Step 4: Pull a Model (First Time Only)
```bash
ollama pull llama2
```
This downloads the model (~4GB). You only need to do this once.

### Step 5: Run the Chatbot
```bash
python src/chatbot.py
```

Or use the convenient script:
```bash
./run.sh
```

## 💡 Usage Tips

- **Type your message** and press Enter to chat
- **Type `/clear`** to reset conversation history
- **Type `/model <name>`** to switch models (e.g., `/model mistral`)
- **Type `/quit`** or `/exit`** to exit
- **Press Ctrl+C** to interrupt and exit

## 🔧 Troubleshooting

### "Ollama service not running"
Make sure Ollama is running in another terminal:
```bash
ollama serve
```

### "Model not found"
Pull the model first:
```bash
ollama pull llama2
```

### "Connection refused"
- Check if Ollama is running: `ps aux | grep ollama`
- Try restarting Ollama: `pkill ollama && ollama serve`

## 📚 Popular Models

- `llama2` - Default, good general purpose
- `mistral` - Fast and efficient
- `codellama` - Great for programming
- `llama2:13b` - Larger, more capable

See all models at: https://ollama.ai/library

---

**That's it! You're ready to chat offline! 🤖**
