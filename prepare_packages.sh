#!/bin/bash

# Script to prepare deployment packages for Windows client
# Run this on Linux to package files for transfer to Windows

echo "=========================================="
echo "Preparing Windows Deployment Packages"
echo "=========================================="
echo ""

# Create temporary packaging directory
PACKAGE_DIR="windows_packages"
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

echo "Step 1: Creating source package for Windows build..."
echo ""

# Package 1: Source files for building .exe on Windows
SOURCE_PKG="$PACKAGE_DIR/AttendanceSystem_Source"
mkdir -p "$SOURCE_PKG"

# Copy Python source files
cp attendance_app.py "$SOURCE_PKG/"
cp worker_threads.py "$SOURCE_PKG/"
cp requirements.txt "$SOURCE_PKG/"

# Copy Windows scripts
cp install_windows.bat "$SOURCE_PKG/"
cp run_app.bat "$SOURCE_PKG/"
cp build_exe.py "$SOURCE_PKG/"

# Copy documentation
cp START_HERE.txt "$SOURCE_PKG/"
cp WINDOWS_SETUP.md "$SOURCE_PKG/"
cp DEPLOYMENT_GUIDE.md "$SOURCE_PKG/"
cp README.md "$SOURCE_PKG/"
cp TROUBLESHOOTING.md "$SOURCE_PKG/"

# Create data directory
mkdir -p "$SOURCE_PKG/data"
echo "Place enrollments.pkl and attendance.csv here" > "$SOURCE_PKG/data/README.txt"

echo "✓ Source package created"
echo ""

echo "Step 2: Creating package WITH your enrolled data..."
echo ""

# Package 2: With existing data
DATA_PKG="$PACKAGE_DIR/Package_WithData"
mkdir -p "$DATA_PKG/data"

cp START_HERE.txt "$DATA_PKG/"

# Copy data files if they exist
if [ -f "enrollments.pkl" ]; then
    cp enrollments.pkl "$DATA_PKG/data/"
    echo "  ✓ Copied enrollments.pkl"
else
    echo "  ⚠ enrollments.pkl not found - will create empty"
fi

if [ -f "attendance.csv" ]; then
    cp attendance.csv "$DATA_PKG/data/"
    echo "  ✓ Copied attendance.csv"
else
    echo "  ⚠ attendance.csv not found - will create empty"
fi

cat > "$DATA_PKG/INSTRUCTIONS.txt" << 'EOF'
================================================================================
PACKAGE WITH EXISTING DATA
================================================================================

This package includes the enrolled people and attendance records.

TO COMPLETE THIS PACKAGE:
1. Build AttendanceSystem.exe on Windows (see DEPLOYMENT_GUIDE.md)
2. Copy AttendanceSystem.exe into this folder
3. ZIP this folder
4. Send to client

FOLDER STRUCTURE SHOULD BE:
  Package_WithData/
    ├── AttendanceSystem.exe  <-- YOU ADD THIS
    ├── START_HERE.txt
    ├── INSTRUCTIONS.txt (this file)
    └── data/
        ├── enrollments.pkl
        └── attendance.csv

CLIENT USAGE:
1. Extract ZIP
2. Double-click AttendanceSystem.exe
3. All enrolled people ready to use!
================================================================================
EOF

echo "✓ Package with data created"
echo ""

echo "Step 3: Creating FRESH/EMPTY package..."
echo ""

# Package 3: Fresh start
FRESH_PKG="$PACKAGE_DIR/Package_Fresh"
mkdir -p "$FRESH_PKG/data"

cp START_HERE.txt "$FRESH_PKG/"

cat > "$FRESH_PKG/INSTRUCTIONS.txt" << 'EOF'
================================================================================
FRESH/EMPTY PACKAGE
================================================================================

This package starts with NO enrolled people.
Client will enroll their own users.

TO COMPLETE THIS PACKAGE:
1. Build AttendanceSystem.exe on Windows (see DEPLOYMENT_GUIDE.md)
2. Copy AttendanceSystem.exe into this folder
3. ZIP this folder
4. Send to client

FOLDER STRUCTURE SHOULD BE:
  Package_Fresh/
    ├── AttendanceSystem.exe  <-- YOU ADD THIS
    ├── START_HERE.txt
    ├── INSTRUCTIONS.txt (this file)
    └── data/ (empty folder)

CLIENT USAGE:
1. Extract ZIP
2. Double-click AttendanceSystem.exe
3. Go to Enrollment tab
4. Enroll people one by one
================================================================================
EOF

echo "✓ Fresh package created"
echo ""

echo "Step 4: Creating complete documentation package..."
echo ""

# Package 4: All documentation
DOCS_PKG="$PACKAGE_DIR/Documentation"
mkdir -p "$DOCS_PKG"

cp START_HERE.txt "$DOCS_PKG/"
cp WINDOWS_SETUP.md "$DOCS_PKG/"
cp DEPLOYMENT_GUIDE.md "$DOCS_PKG/"
cp README.md "$DOCS_PKG/"
cp TROUBLESHOOTING.md "$DOCS_PKG/"
cp QUICKSTART.md "$DOCS_PKG/"
cp CODE_ANALYSIS.md "$DOCS_PKG/"

echo "✓ Documentation package created"
echo ""

echo "Step 5: Creating archive files..."
echo ""

cd "$PACKAGE_DIR"

# Create ZIP archives (using zip if available, tar.gz otherwise)
if command -v zip &> /dev/null; then
    echo "Using ZIP compression..."
    zip -r AttendanceSystem_Source.zip AttendanceSystem_Source/ > /dev/null
    zip -r Package_WithData.zip Package_WithData/ > /dev/null
    zip -r Package_Fresh.zip Package_Fresh/ > /dev/null
    zip -r Documentation.zip Documentation/ > /dev/null
    echo "  ✓ ZIP archives created"
else
    echo "Using TAR.GZ compression..."
    tar -czf AttendanceSystem_Source.tar.gz AttendanceSystem_Source/
    tar -czf Package_WithData.tar.gz Package_WithData/
    tar -czf Package_Fresh.tar.gz Package_Fresh/
    tar -czf Documentation.tar.gz Documentation/
    echo "  ✓ TAR.GZ archives created"
fi

cd ..

echo ""
echo "=========================================="
echo "PACKAGING COMPLETE!"
echo "=========================================="
echo ""
echo "Created packages in: $PACKAGE_DIR/"
echo ""
ls -lh "$PACKAGE_DIR"/*.{zip,tar.gz} 2>/dev/null || ls -lh "$PACKAGE_DIR"/
echo ""
echo "NEXT STEPS:"
echo ""
echo "1. TRANSFER TO WINDOWS MACHINE:"
echo "   - Copy AttendanceSystem_Source.zip/tar.gz to Windows PC"
echo "   - Extract it there"
echo ""
echo "2. BUILD .EXE ON WINDOWS:"
echo "   - Follow DEPLOYMENT_GUIDE.md"
echo "   - Run: install_windows.bat"
echo "   - Run: python build_exe.py"
echo "   - Result: dist/AttendanceSystem.exe"
echo ""
echo "3. COMPLETE PACKAGES:"
echo "   - Copy AttendanceSystem.exe to Package_WithData/"
echo "   - OR copy to Package_Fresh/"
echo "   - ZIP the package"
echo ""
echo "4. SEND TO CLIENT:"
echo "   - Upload ZIP to Google Drive/Dropbox"
echo "   - Send download link to client"
echo "   - Include START_HERE.txt instructions"
echo ""
echo "See DEPLOYMENT_GUIDE.md for complete instructions"
echo "=========================================="
