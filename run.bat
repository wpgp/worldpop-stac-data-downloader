@echo off
REM WorldPop STAC Data Downloader - Quick Run Script
REM This runs the application directly from source code

echo ================================================
echo    WorldPop STAC Data Downloader (Beta)
echo ================================================
echo.
echo Starting application from source code...
echo.

REM Change to script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not found in PATH
    echo.
    echo To fix this:
    echo 1. Install Python 3.8+ from https://python.org
    echo 2. During installation, check "Add Python to PATH"
    echo 3. Restart your computer after installation
    echo 4. Try running this script again
    echo.
    echo Alternatively, use build.bat to create a standalone executable.
    echo.
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found
    echo Please run this script from the application directory
    echo.
    pause
    exit /b 1
)

REM Check basic dependencies
echo Checking dependencies...
python -c "import tkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: tkinter not available
    echo This is required for the GUI interface
    echo.
    pause
    exit /b 1
)

python -c "import requests" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing requests library...
    python -m pip install requests >nul 2>&1
)

python -c "import PIL" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Pillow library...
    python -m pip install Pillow >nul 2>&1
)

echo Dependencies OK
echo.
echo Launching WorldPop STAC Data Downloader...
echo.

REM Run the application
python main.py

REM Check exit code
if %errorlevel% neq 0 (
    echo.
    echo Application exited with an error.
    echo.
    echo Common solutions:
    echo 1. Run: pip install -r requirements.txt
    echo 2. Check internet connection
    echo 3. Try building executable with build.bat instead
    echo.
)

echo.
echo Application closed. Press any key to exit.
pause >nul
