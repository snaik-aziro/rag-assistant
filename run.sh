#!/bin/bash
# Simple run script for Local LLM Chatbot

cd "$(dirname "$0")"
python3 src/chatbot.py "$@"
