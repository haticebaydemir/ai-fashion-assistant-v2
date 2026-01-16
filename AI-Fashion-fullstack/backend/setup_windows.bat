@echo off
echo ========================================
echo AI Fashion Assistant - Backend Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [4/5] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo.
    echo ========================================
    echo IMPORTANT: Please edit .env file and set:
    echo - MONGODB_URL (MongoDB connection string)
    echo - SECRET_KEY (Generate using: python -c "import secrets; print(secrets.token_urlsafe(32))")
    echo - GROQ_API_KEY (Your GROQ API key)
    echo ========================================
    echo.
    pause
) else (
    echo .env file already exists, skipping...
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the backend server:
echo 1. Make sure MongoDB is running
echo 2. Run: run_backend.bat
echo.
pause
