#!/bin/bash

# Simple launcher for Face Recognition Attendance System

echo "=========================================="
echo "Face Recognition Attendance System"
echo "=========================================="
echo ""

# Activate virtual environment
if [ ! -d "my_env" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please ensure you're in the attendance directory"
    exit 1
fi

echo "Activating virtual environment..."
source my_env/bin/activate

# Suppress TensorFlow warnings (optional)
export TF_CPP_MIN_LOG_LEVEL=2

echo "Starting application..."
echo ""
echo "Note: You can close this with Ctrl+C or by closing the application window"
echo ""

# Run the application
python attendance_app.py

echo ""
echo "Application closed."
