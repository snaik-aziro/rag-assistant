# 🤖 Local LLM Chatbot with RAG

A powerful chatbot that runs completely offline using local Large Language Models via Ollama with **RAG (Retrieval-Augmented Generation)** capabilities. Features both a beautiful web UI and terminal interface!

## ✨ Features

- **RAG Pipeline**: Uses lightweight vector store vector database to retrieve relevant context from conversations
- **Offline Operation**: Runs completely without internet after setup
- **Modern Web UI**: Beautiful, magical-looking web interface with animations and effects
- **Terminal Interface**: Rich terminal-based interface with colorful output
- **Multiple Models**: Support for various Ollama models (Llama, Mistral, etc.)
- **Conversation History**: Maintains context across conversations
- **Error Handling**: Robust error handling for network and model issues
- **Model Switching**: Switch between different models during conversation
- **Auto-Setup**: Automated installation of dependencies and Ollama

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Internet connection for initial setup (to download models)

### Installation

1. **Clone or download this repository**
   ```bash
   cd /path/to/local-llm
   ```

2. **Run the automated setup**
   ```bash
   python setup.py
   ```

   This will:
   - Install Python dependencies
   - Install Ollama (if not already installed)
   - Set up the environment

3. **Start the chatbot**

   **Web UI (Recommended):**
   ```bash
   python src/app.py
   # or
   ./run_ui.sh
   ```
   Then open http://localhost:5002 in your browser

   **Terminal Interface:**
   ```bash
   python src/chatbot.py
   ```

## 📖 Usage

### Web UI (Recommended)

The modern web interface provides a beautiful, magical experience:

1. **Start the web server:**
   ```bash
   python src/app.py
   ```

2. **Open your browser:**
   Navigate to http://localhost:5002

3. **Features:**
   - ✨ Beautiful animated background with gradient orbs
   - 💬 Real-time chat with typing indicators
   - 🎨 Modern dark theme with glowing effects
   - 📱 Fully responsive design
   - 🔍 RAG-powered context retrieval
   - 🧠 Status indicators for connection and model info
   - ⌨️ Keyboard shortcuts (Enter to send, Shift+Enter for new line)

### Terminal Interface

Once the chatbot is running, you can:

- **Chat normally**: Just type your message and press Enter
- **Clear history**: Type `/clear` to reset conversation history
- **Switch models**: Type `/model <model_name>` to change models
- **Exit**: Type `/quit` or `/exit` to close the chatbot

### Command Line Options

```bash
python src/chatbot.py [options]

Options:
  --model MODEL    Model name to use (default: llama2)
  --host HOST      Ollama host URL (default: http://localhost:11434)
  --help           Show help message
```

### Examples

```bash
# Use default llama2 model
python src/chatbot.py

# Use Mistral model
python src/chatbot.py --model mistral

# Use custom Ollama host
python src/chatbot.py --host http://192.168.1.100:11434
```

## 🔧 Manual Setup (Alternative)

If the automated setup doesn't work, you can set up manually:

### 1. Install Ollama

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

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Pull Models

```bash
# Pull popular models
ollama pull llama2
ollama pull mistral
ollama pull codellama
```

## 📋 Available Models

Popular models you can use:

- `llama2` - Meta's Llama 2 (default)
- `mistral` - Mistral 7B
- `codellama` - Code Llama for programming
- `llama2:13b` - Larger Llama 2 model
- `vicuna` - LMSYS Vicuna
- `orca-mini` - Microsoft Orca Mini

See [Ollama Library](https://ollama.ai/library) for all available models.

## 🏗️ Project Structure

```
local-llm/
├── src/
│   └── chatbot.py          # Main chatbot application
├── docs/                   # Documentation (future use)
├── requirements.txt        # Python dependencies
├── setup.py               # Automated setup script
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

You can set these environment variables:

- `OLLAMA_HOST` - Ollama server URL (default: http://localhost:11434)

### Model Configuration

Models are automatically downloaded when first used. You can pre-download models:

```bash
ollama pull llama2
ollama pull mistral
# etc.
```

## 🐛 Troubleshooting

### Common Issues

**"Ollama service not running"**
```bash
# Start Ollama service
ollama serve
```

**"Model not found"**
```bash
# Pull the model manually
ollama pull llama2
```

**"Connection refused"**
- Make sure Ollama is running: `ollama serve`
- Check if the host/port is correct

**"Python dependencies missing"**
```bash
pip install -r requirements.txt
```

### Getting Help

1. Check the terminal output for error messages
2. Ensure Ollama is installed and running
3. Verify your Python version (3.7+)
4. Try running with a different model

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) - For providing the local LLM runtime
- [Rich](https://github.com/Textualize/rich) - For the beautiful terminal interface
- [Colorama](https://github.com/tartley/colorama) - For cross-platform colored terminal output

---

**Happy chatting offline! 🤖✨**
