#!/bin/bash

# Installation script for Face Recognition Attendance System

echo "=========================================="
echo "Face Recognition Attendance System Setup"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Activating virtual environment..."
    source my_env/bin/activate
else
    echo "Virtual environment already activated"
fi

echo ""
echo "Installing dependencies..."
echo ""

# Install PyQt5 and GUI dependencies
pip install PyQt5==5.15.11

# Install matplotlib for charts
pip install matplotlib==3.9.4
pip install seaborn==0.13.2

# Install Excel export support
pip install openpyxl==3.1.5

# The other dependencies should already be installed from your terminal version
# But we'll ensure they're up to date

echo ""
echo "Verifying existing installations..."

# Important: Use opencv-python-headless to avoid Qt conflicts with PyQt5
echo "Installing opencv-python-headless (avoiding Qt conflicts)..."
pip uninstall -y opencv-python 2>/dev/null || true
pip install opencv-python-headless==4.12.0.88

# Install/upgrade other dependencies
pip install --upgrade pandas numpy face-recognition deepface

echo ""
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "  python attendance_app.py"
echo ""
echo "For the old terminal version:"
echo "  python attedance.py"
echo ""
