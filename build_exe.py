"""
PyInstaller Build Script for Windows Executable
Run this on a Windows machine to create AttendanceSystem.exe

Requirements:
    pip install pyinstaller

Usage:
    python build_exe.py

Output:
    dist/AttendanceSystem.exe (~500MB standalone executable)
"""

import PyInstaller.__main__
import sys
import os

def build_exe():
    """Build standalone Windows executable"""

    print("=" * 60)
    print("Building Attendance System Executable for Windows")
    print("=" * 60)
    print()
    print("This will take 5-10 minutes...")
    print("Output will be in: dist/AttendanceSystem.exe")
    print()

    # PyInstaller arguments
    args = [
        'attendance_app.py',  # Main script

        # Output options
        '--name=AttendanceSystem',
        '--onefile',  # Single executable
        '--windowed',  # No console window (GUI only)

        # Icon (optional - add if you have an .ico file)
        # '--icon=icon.ico',

        # Include necessary data files and modules
        '--hidden-import=sklearn.utils._cython_blas',
        '--hidden-import=sklearn.neighbors.typedefs',
        '--hidden-import=sklearn.neighbors.quad_tree',
        '--hidden-import=sklearn.tree._utils',
        '--hidden-import=PIL._tkinter_finder',
        '--hidden-import=deepface',
        '--hidden-import=deepface.DeepFace',
        '--hidden-import=deepface.basemodels',
        '--hidden-import=deepface.commons',
        '--hidden-import=deepface.detectors',
        '--hidden-import=deepface.extendedmodels',
        '--hidden-import=retina_face',
        '--hidden-import=mtcnn',

        # Collect data for DeepFace (emotion models will auto-download)
        '--collect-all=deepface',
        '--collect-all=retina_face',
        '--collect-all=mtcnn',

        # Collect face_recognition models
        '--collect-all=face_recognition_models',

        # Collect matplotlib backends
        '--collect-all=matplotlib',

        # Add package data
        '--copy-metadata=deepface',
        '--copy-metadata=tensorflow',
        '--copy-metadata=keras',

        # Exclude unnecessary packages to reduce size
        '--exclude-module=test',
        '--exclude-module=unittest',
        '--exclude-module=distutils',

        # Clean build
        '--clean',

        # Show progress
        '--noconfirm',

        # Optimization
        '--optimize=2',
    ]

    # Run PyInstaller
    PyInstaller.__main__.run(args)

    print()
    print("=" * 60)
    print("Build Complete!")
    print("=" * 60)
    print()
    print("Executable location: dist/AttendanceSystem.exe")
    print()
    print("IMPORTANT: Test the executable before distributing:")
    print("  1. Copy AttendanceSystem.exe to a clean Windows machine")
    print("  2. Create a 'data' folder next to the .exe")
    print("  3. Run AttendanceSystem.exe")
    print("  4. Test enrollment and recognition")
    print()
    print("Package for client:")
    print("  AttendanceSystem/")
    print("    ├── AttendanceSystem.exe")
    print("    ├── START_HERE.txt")
    print("    ├── User_Guide.pdf")
    print("    └── data/ (folder for enrollments and attendance)")
    print()
    print("File size: ~400-600 MB (includes TensorFlow)")
    print()


if __name__ == '__main__':
    # Check if running on Windows
    if sys.platform != 'win32':
        print("WARNING: This build script should be run on Windows")
        print("         to create a Windows executable.")
        print()
        print("Options:")
        print("  1. Run this script on a Windows machine")
        print("  2. Use a Windows VM (VirtualBox, VMware)")
        print("  3. Use GitHub Actions with Windows runner")
        print("  4. Use cloud Windows instance")
        print()
        response = input("Do you want to continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(0)

    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("ERROR: PyInstaller is not installed")
        print()
        print("Install it with:")
        print("  pip install pyinstaller")
        print()
        sys.exit(1)

    build_exe()
