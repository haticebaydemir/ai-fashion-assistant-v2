@echo off
echo ========================================
echo AI Fashion Assistant - Frontend Setup
echo ========================================
echo.

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

REM Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [2/3] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo.
    echo ========================================
    echo IMPORTANT: Please edit .env file and set:
    echo - VITE_API_URL (Backend API URL, default: http://localhost:8000/api)
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
echo To start the frontend:
echo Run: run_frontend.bat
echo.
pause
