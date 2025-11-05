#!/bin/bash
# Run the web UI for the RAG Chatbot

cd "$(dirname "$0")"
echo "🚀 Starting RAG Chatbot Web UI..."
echo "📱 Open http://localhost:5002 in your browser"
echo ""
python3 src/app.py

