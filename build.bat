@echo off
REM WorldPop STAC Browser - Build Script
REM This batch file builds the executable automatically

echo ================================================
echo    WorldPop STAC Browser - Executable Builder
echo ================================================
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo ✓ Python found
echo.

REM Check if PIL/Pillow is installed
echo Checking dependencies...
python -c "import PIL; print('✓ Pillow/PIL found')" 2>nul
if %errorlevel% neq 0 (
    echo Pillow/PIL not found - installing...
    python -m pip install Pillow >nul 2>&1
    python -c "import PIL; print('✓ Pillow/PIL installed successfully')" 2>nul
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install Pillow
        echo Please install manually: pip install Pillow
        pause
        exit /b 1
    )
)

python -c "import tkinter; print('✓ Tkinter found')" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Tkinter not found - required for GUI
    echo Please install tkinter or use a different Python distribution
    pause
    exit /b 1
)

python -c "import requests; print('✓ Requests found')" 2>nul
if %errorlevel% neq 0 (
    echo Requests not found - installing...
    python -m pip install requests >nul 2>&1
    python -c "import requests; print('✓ Requests installed successfully')" 2>nul
)

echo ✓ All dependencies checked
echo.

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found in current directory
    echo Please run this script from the application root directory
    pause
    exit /b 1
)

echo ✓ Application files found
echo.

REM Run the build script
echo Starting build process...
echo.
python build_exe.py

REM Check if build was successful
if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo           BUILD COMPLETED SUCCESSFULLY!
    echo ================================================
    echo.
    echo The executable is ready in the 'dist' folder:
    echo   - WorldPop_STAC_Data_Downloader.exe
    echo.
    
    REM Ask if user wants to open the dist folder
    set /p open_folder="Open the dist folder? (y/n): "
    if /i "%open_folder%"=="y" (
        explorer dist
    )
    
) else (
    echo.
    echo ================================================
    echo              BUILD FAILED!
    echo ================================================
    echo.
    echo Please check the error messages above and:
    echo   1. Install missing dependencies: pip install -r requirements.txt
    echo   2. Make sure all files are present
    echo   3. Check Python version (3.8+ required)
    echo.
)

echo.
echo Press any key to exit...
pause >nul