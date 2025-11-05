#!/usr/bin/env python3
"""
Setup script for Local LLM Chatbot
Handles installation of Ollama and Python dependencies
"""

import os
import sys
import platform
import subprocess
import urllib.request
import json
from pathlib import Path

def run_command(command, description=""):
    """Run a shell command and return success status"""
    try:
        print(f"🔄 {description}")
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ Done")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    requirements_file = Path(__file__).parent / "requirements.txt"
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False

    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def detect_os():
    """Detect the operating system"""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    elif system == "windows":
        return "windows"
    else:
        return "unknown"

def install_ollama():
    """Install Ollama based on the operating system"""
    os_type = detect_os()

    if os_type == "unknown":
        print("❌ Unsupported operating system")
        return False

    print(f"🔄 Installing Ollama for {os_type}...")

    try:
        if os_type == "macos":
            # Install Ollama on macOS
            return run_command(
                "brew install ollama",
                "Installing Ollama via Homebrew"
            )

        elif os_type == "linux":
            # Install Ollama on Linux
            return run_command(
                "curl -fsSL https://ollama.ai/install.sh | sh",
                "Installing Ollama via official installer"
            )

        elif os_type == "windows":
            print("📝 For Windows, please download and install Ollama manually from:")
            print("   https://ollama.ai/download")
            print("   After installation, run this setup again.")
            return True  # Don't fail, just inform user

    except Exception as e:
        print(f"❌ Error installing Ollama: {e}")
        return False

def check_ollama_installed():
    """Check if Ollama is installed"""
    try:
        subprocess.run(["ollama", "--version"], capture_output=True, check=True)
        print("✅ Ollama is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def create_desktop_shortcut():
    """Create a desktop shortcut (optional)"""
    try:
        os_type = detect_os()
        script_path = Path(__file__).parent / "src" / "chatbot.py"

        if os_type == "macos":
            # Create an alias on macOS desktop
            desktop_path = Path.home() / "Desktop" / "LocalChatbot.command"
            with open(desktop_path, 'w') as f:
                f.write(f"#!/bin/bash\ncd {script_path.parent.parent}\n{sys.executable} {script_path}\n")
            desktop_path.chmod(0o755)
            print(f"✅ Desktop shortcut created: {desktop_path}")

        elif os_type == "linux":
            # Create desktop entry on Linux
            desktop_entry = f"""[Desktop Entry]
Name=Local LLM Chatbot
Exec={sys.executable} {script_path}
Icon=terminal
Type=Application
Categories=Utility;
"""
            desktop_path = Path.home() / ".local" / "share" / "applications" / "local-chatbot.desktop"
            desktop_path.parent.mkdir(parents=True, exist_ok=True)
            with open(desktop_path, 'w') as f:
                f.write(desktop_entry)
            print(f"✅ Desktop entry created: {desktop_path}")

    except Exception as e:
        print(f"⚠️ Could not create desktop shortcut: {e}")

def main():
    """Main setup function"""
    print("🚀 Setting up Local LLM Chatbot\n")

    # Check Python version
    if not check_python_version():
        return False

    # Install Python dependencies
    if not install_python_dependencies():
        return False

    # Check if Ollama is installed
    if not check_ollama_installed():
        print("\n📦 Ollama not found. Installing...")
        if not install_ollama():
            print("❌ Failed to install Ollama. Please install it manually.")
            return False
    else:
        print("✅ Ollama is already installed")

    # Create desktop shortcut
    create_desktop_shortcut()

    print("\n🎉 Setup complete!")
    print("\n📚 Next steps:")
    print("1. Start Ollama service: ollama serve")
    print("2. Run the chatbot: python src/chatbot.py")
    print("3. For help: python src/chatbot.py --help")

    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
