@echo off
REM ========================================
REM AI Fashion Backend - Start Server
REM ========================================

echo.
echo ========================================
echo Starting AI Fashion Backend Server
echo ========================================
echo.

REM Activate virtual environment
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Please run setup_backend.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

REM Check .env exists
if not exist .env (
    echo [ERROR] .env file not found!
    echo Please run setup_backend.bat first
    pause
    exit /b 1
)

REM Start server
echo Starting server on http://localhost:8000
echo.
echo Press CTRL+C to stop the server
echo.
echo ========================================
echo.

python main.py

pause
