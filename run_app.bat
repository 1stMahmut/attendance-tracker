@echo off
REM Windows Launcher for Face Recognition Attendance System

REM Set window title
title Face Recognition Attendance System

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo.
    echo Please run install_windows.bat first to set up the application.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Set environment variables to reduce TensorFlow warnings
set TF_CPP_MIN_LOG_LEVEL=2
set TF_ENABLE_ONEDNN_OPTS=0

REM Clear screen for cleaner startup
cls

echo ==========================================
echo Face Recognition Attendance System
echo ==========================================
echo.
echo Starting application...
echo.
echo NOTE: The first startup may take 30-60 seconds
echo       as DeepFace downloads emotion detection models.
echo.
echo You can close this window or press Ctrl+C to exit.
echo ==========================================
echo.

REM Run the application
python attendance_app.py

REM If application exits with error, pause to show error message
if errorlevel 1 (
    echo.
    echo ==========================================
    echo Application exited with an error
    echo ==========================================
    echo.
    echo Please check the error message above.
    echo.
    echo Common solutions:
    echo   1. Ensure webcam is connected and not in use
    echo   2. Check TROUBLESHOOTING.md for help
    echo   3. Try reinstalling: run install_windows.bat
    echo.
    pause
)
