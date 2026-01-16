@echo off
echo.
echo ========================================
echo Starting AI Fashion Frontend
echo ========================================
echo.

if not exist node_modules (
    echo [ERROR] node_modules not found!
    echo Please run setup_frontend.bat first
    pause
    exit /b 1
)

echo Starting development server...
echo.
echo Frontend will open at: http://localhost:5173
echo Press CTRL+C to stop
echo.

call npm run dev

pause
