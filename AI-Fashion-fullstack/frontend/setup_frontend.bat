@echo off
echo.
echo ========================================
echo AI Fashion Frontend Setup - Windows
echo ========================================
echo.

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js not found!
    echo Please install Node.js from: https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Node.js found
echo.

echo Installing dependencies...
call npm install

if errorlevel 1 (
    echo.
    echo [WARNING] npm install failed, trying with --legacy-peer-deps
    call npm install --legacy-peer-deps
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure backend is running (http://localhost:8000)
echo 2. Run: run_frontend.bat
echo.

pause
