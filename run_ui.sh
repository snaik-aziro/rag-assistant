#!/bin/bash
# Run the Release Dashboard AI Assistant web UI

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV_PATH="$PROJECT_ROOT/.venv"
PORT="${PORT:-5002}"

cd "$PROJECT_ROOT"

PYTHON_BIN="${PYTHON_BIN:-python3}"

if [ ! -d "$VENV_PATH" ]; then
  echo "🐍 Creating Python virtual environment..."
  "$PYTHON_BIN" -m venv "$VENV_PATH"
  "$VENV_PATH/bin/pip" install --upgrade pip
  "$VENV_PATH/bin/pip" install -r requirements.txt
fi

echo "🔍 Checking Ollama service..."
if ! curl -sf "http://localhost:11434/api/tags" >/dev/null 2>&1; then
  cat <<'EOF'
⚠️  Ollama does not appear to be running.
   Start it in another terminal with:
     ollama serve
EOF
  exit 1
fi

echo "🚀 Starting Release Dashboard AI Assistant..."
echo "📱 Open http://localhost:${PORT} in your browser"
echo ""

"$VENV_PATH/bin/python" src/app.py --host 0.0.0.0 --port "$PORT"
