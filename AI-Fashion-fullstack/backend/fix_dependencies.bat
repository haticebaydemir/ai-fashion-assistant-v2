@echo off
REM ========================================
REM Fix Common Dependency Issues
REM ========================================

echo.
echo ========================================
echo Fixing Dependencies
echo ========================================
echo.

if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Please run setup_backend.bat first
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo [1/3] Fixing PyMongo/Motor compatibility...
pip uninstall -y motor pymongo
pip install pymongo==4.6.1
pip install motor==3.3.2

echo.
echo [2/3] Fixing NumPy version...
pip uninstall -y numpy
pip install "numpy<2"

echo.
echo [3/3] Verifying installations...
python -c "import motor; import pymongo; import numpy; print('✅ Motor:', motor.version); print('✅ PyMongo:', pymongo.__version__); print('✅ NumPy:', numpy.__version__)"

if errorlevel 1 (
    echo.
    echo [ERROR] Verification failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Dependencies Fixed!
echo ========================================
echo.
echo You can now run: run_backend.bat
echo.

pause
