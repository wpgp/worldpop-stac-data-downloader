@echo off
REM WorldPop STAC Data Downloader - Build Script
REM This batch file builds the executable automatically for beta release

echo ================================================
echo   WorldPop STAC Data Downloader - Beta Builder
echo ================================================
echo.
echo This script will:
echo  - Check Python installation
echo  - Install required dependencies
echo  - Build standalone executable
echo  - Create ready-to-use .exe file
echo.
echo BETA VERSION NOTICE:
echo The resulting executable will NOT be digitally signed.
echo This is normal for beta software and may trigger antivirus warnings.
echo.
pause

REM Change to the script directory
cd /d "%~dp0"

REM Check if Python is available
echo [1/4] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8+ from https://python.org
    echo During installation, make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

python --version
echo OK - Python found
echo.

REM Check if main.py exists
echo [2/4] Checking application files...
if not exist "main.py" (
    echo ERROR: main.py not found in current directory
    echo Please run this script from the application root directory
    echo.
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found
    echo This file is required for dependency installation
    echo.
    pause
    exit /b 1
)

echo OK - Application files found
echo.

REM Install dependencies
echo [3/4] Installing dependencies...
echo This may take a few minutes on first run...
echo.

python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt

REM Check critical dependencies
python -c "import tkinter; print('OK - GUI framework available')" 2>nul
if %errorlevel% neq 0 (
    echo ERROR: Tkinter not available - required for GUI
    echo Please install tkinter or use a different Python distribution
    echo.
    pause
    exit /b 1
)

python -c "import requests; print('OK - HTTP client available')" 2>nul
python -c "import PIL; print('OK - Image processing available')" 2>nul

echo.
echo Dependencies installation completed
echo.

REM Build executable
echo [4/4] Building executable...
echo This will take several minutes - please wait...
echo.

python build_exe.py

REM Check if build was successful
if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo           BUILD COMPLETED SUCCESSFULLY!
    echo ================================================
    echo.

    if exist "dist\WorldPop_STAC_Data_Downloader.exe" (
        for %%F in ("dist\WorldPop_STAC_Data_Downloader.exe") do set size=%%~zF
        set /a size_mb=!size! / 1048576

        echo Executable created: WorldPop_STAC_Data_Downloader.exe
        echo Location: %CD%\dist\
        echo Size: approximately !size_mb! MB
        echo.
        echo IMPORTANT BETA NOTES:
        echo - This executable is NOT digitally signed
        echo - Your antivirus may show warnings (this is normal)
        echo - The software is safe - you built it yourself
        echo - Report any issues for improvement
        echo.

        set /p open_folder="Open the dist folder now? (y/n): "
        if /i "!open_folder!"=="y" (
            explorer dist
        )
    ) else (
        echo WARNING: Executable file not found in expected location
        echo Build may have completed but file location is different
    )
    
) else (
    echo.
    echo ================================================
    echo              BUILD FAILED!
    echo ================================================
    echo.
    echo Common solutions:
    echo  1. Make sure Python 3.8+ is installed
    echo  2. Check internet connection for dependency downloads
    echo  3. Run as administrator if permission errors occur
    echo  4. Ensure antivirus is not blocking the build process
    echo.
    echo Try running: pip install -r requirements.txt
    echo Then run this script again.
    echo.
)

echo.
echo Build process finished. Press any key to exit.
pause >nul