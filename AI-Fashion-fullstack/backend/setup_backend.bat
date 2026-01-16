@echo off
REM ========================================
REM AI Fashion Backend - Windows Setup
REM ========================================

echo.
echo ========================================
echo AI Fashion Backend Setup - Windows
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.10 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Create virtual environment
echo [1/5] Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)
echo.

REM Activate virtual environment
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo [3/5] Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo [4/5] Installing dependencies (this may take 5-10 minutes)...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Check .env file
echo [5/5] Checking configuration...
if not exist .env (
    echo [WARNING] .env file not found!
    echo.
    echo Creating .env from template...
    copy .env.example .env >nul 2>&1
    echo.
    echo IMPORTANT: Edit .env file and add:
    echo   - MONGODB_URL (MongoDB connection string)
    echo   - SECRET_KEY (JWT secret key)
    echo   - GROQ_API_KEY (for chat functionality)
    echo.
    echo Opening .env in notepad...
    timeout /t 2 >nul
    notepad .env
)
echo.

REM Success message
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy data files (run: copy_data.bat)
echo 2. Make sure MongoDB is running
echo 3. Edit .env if needed
echo 4. Run: run_backend.bat
echo.

pause
