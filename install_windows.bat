@echo off
REM Windows Installation Script for Face Recognition Attendance System
REM This script sets up the application on Windows

echo ==========================================
echo Face Recognition Attendance System
echo Windows Installation Script
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8, 3.9, or 3.10 from:
    echo https://www.python.org/downloads/
    echo.
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check Python version
python -c "import sys; exit(0 if (3,8) <= sys.version_info[:2] <= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python version must be 3.8, 3.9, or 3.10
    echo Your version:
    python --version
    echo.
    echo Please install a compatible Python version from:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo Python version is compatible!
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        echo.
        echo Try running: python -m pip install --upgrade pip
        echo.
        pause
        exit /b 1
    )
    echo Virtual environment created successfully!
) else (
    echo Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
echo This may take 5-10 minutes depending on your internet connection...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip

REM Install dlib - this is the tricky one for Windows
echo.
echo Installing dlib (this may take a while)...
echo If this fails, see WINDOWS_SETUP.md for alternative installation methods
echo.

pip install dlib==20.0.0
if errorlevel 1 (
    echo.
    echo WARNING: dlib installation failed with pip
    echo Trying alternative: installing pre-built wheel...
    echo.
    pip install https://github.com/jloh02/dlib/releases/download/v19.22/dlib-19.22.99-cp310-cp310-win_amd64.whl
    if errorlevel 1 (
        echo.
        echo ERROR: Could not install dlib
        echo.
        echo Please see WINDOWS_SETUP.md for manual installation instructions
        echo OR download pre-built wheel from:
        echo https://github.com/z-mahmud22/Dlib_Windows_Python3.x
        echo.
        pause
        exit /b 1
    )
)

echo.
echo Installing other dependencies...
echo.

REM Install core packages
pip install opencv-python-headless==4.12.0.88
pip install face-recognition==1.3.0
pip install numpy==2.2.6
pip install pandas==2.3.3
pip install PyQt5==5.15.11

REM Install visualization packages
pip install matplotlib==3.9.4
pip install seaborn==0.13.2

REM Install export packages
pip install openpyxl==3.1.5
pip install reportlab==4.2.5

REM Install Pillow
pip install Pillow==12.0.0

REM Install DeepFace and TensorFlow
echo.
echo Installing DeepFace and TensorFlow (this is large, ~500MB)...
echo.
pip install tensorflow==2.20.0
pip install deepface==0.0.95

echo.
echo ==========================================
echo Installation Complete!
echo ==========================================
echo.
echo To run the application:
echo   1. Double-click run_app.bat
echo      OR
echo   2. Run: run_app.bat
echo.
echo For first-time use, please read:
echo   - START_HERE.txt
echo   - WINDOWS_SETUP.md
echo.
pause
