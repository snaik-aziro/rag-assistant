@echo off
REM Run the Release Dashboard AI Assistant web UI on Windows

setlocal enabledelayedexpansion

set "PROJECT_ROOT=%~dp0"
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"
cd /d "%PROJECT_ROOT%"

if "%PORT%"=="" (
    set "PORT=5002"
)

set "PYTHON_BIN=py"
if not "%PYTHON_BIN%"=="" (
    REM allow overriding PYTHON_BIN via environment variable
)

set "VENV_PATH=%PROJECT_ROOT%\.venv"
set "PIP_PATH=%VENV_PATH%\Scripts\pip.exe"
set "PY_PATH=%VENV_PATH%\Scripts\python.exe"

if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo 🐍 Creating Python virtual environment...
    "%PYTHON_BIN%" -3 -m venv "%VENV_PATH%"
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment.
        exit /b 1
    )
    "%PIP_PATH%" install --upgrade pip
    "%PIP_PATH%" install -r requirements.txt
)

echo 🔍 Checking Ollama service...
curl --silent --fail http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo(
    echo ⚠️  Ollama does not appear to be running.
    echo     Start it in another terminal with:
    echo       ollama serve
    echo(
    exit /b 1
)

echo 🚀 Starting Release Dashboard AI Assistant...
echo 📱 Open http://localhost:%PORT% in your browser
echo(

"%PY_PATH%" src\app.py --host 0.0.0.0 --port %PORT%

endlocal

