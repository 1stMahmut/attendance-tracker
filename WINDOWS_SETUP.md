# Windows Setup Guide

Complete guide for installing and running the Face Recognition Attendance System on Windows.

## Two Installation Options

### Option 1: Standalone Executable (Recommended for Non-Technical Users)

**Easiest method** - No Python installation required!

1. **Download** the package: `AttendanceSystem_v1.0.zip`
2. **Extract** the ZIP file to any location (e.g., Desktop, Documents)
3. **Double-click** `AttendanceSystem.exe`
4. **Done!** The application opens ready to use

**Requirements**:
- Windows 10 or Windows 11
- Webcam (built-in or USB)
- 4GB RAM minimum (8GB recommended)
- 1GB free disk space

**First Run**:
- May take 30-60 seconds to start
- DeepFace will download emotion detection models (~50MB)
- Allow firewall/antivirus if prompted

---

### Option 2: Python Source Installation (For Technical Users or Development)

**For users who want to modify the code or prefer Python installation**

#### Step 1: Install Python

1. Download Python 3.8, 3.9, or 3.10 from [python.org](https://www.python.org/downloads/)
   - **Recommended**: Python 3.10.11
   - **Important**: Check "Add Python to PATH" during installation!

2. Verify installation:
   ```cmd
   python --version
   ```
   Should show: Python 3.10.x

#### Step 2: Install System Requirements

**Install CMake** (required for dlib):

Download and install CMake from: https://cmake.org/download/
- Choose: "Windows x64 Installer"
- Check "Add CMake to system PATH" during installation

**Install Visual C++ Build Tools** (required for dlib):

Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
- Run installer
- Select "Desktop development with C++"
- Install (this is large, ~6GB)

#### Step 3: Run Installation Script

1. Open Command Prompt (cmd) or PowerShell
2. Navigate to the attendance folder:
   ```cmd
   cd path\to\attendance
   ```
3. Run the installation script:
   ```cmd
   install_windows.bat
   ```
4. Wait 5-10 minutes for all dependencies to install

#### Step 4: Run the Application

Double-click `run_app.bat` or run:
```cmd
run_app.bat
```

---

## Troubleshooting Windows-Specific Issues

### Issue 1: dlib Installation Fails

**Error**: `Could not build wheels for dlib`

**Solution A** - Use pre-built wheel:
1. Download pre-built dlib wheel from:
   - https://github.com/z-mahmud22/Dlib_Windows_Python3.x
2. Choose your Python version (e.g., cp310 = Python 3.10)
3. Download the .whl file
4. Install:
   ```cmd
   pip install path\to\downloaded\dlib-XX.XX-cpXX-cpXX-win_amd64.whl
   ```

**Solution B** - Install Anaconda instead:
```cmd
conda install -c conda-forge dlib
```

---

### Issue 2: Camera Not Detected

**Windows uses different camera indexing than Linux**

**Solution 1** - Try different camera indices:

Edit `attendance_app.py`, line ~730:
```python
# Change camera_index from 0 to 1 or 2
self.camera_thread = CameraThread(camera_index=1)
```

**Solution 2** - Check Windows camera permissions:
1. Press Win+I (Settings)
2. Go to Privacy → Camera
3. Ensure "Allow apps to access your camera" is ON
4. Enable camera for desktop apps

**Solution 3** - Install camera drivers:
- Go to Device Manager
- Find "Cameras" or "Imaging devices"
- Right-click → Update driver

---

### Issue 3: Windows Defender / Antivirus Blocks Application

**Symptom**: Executable won't run, shows security warning

**Solution**:
1. Click "More info" on the warning
2. Click "Run anyway"

**For permanently allowing**:
1. Open Windows Security
2. Go to Virus & threat protection → Manage settings
3. Under "Exclusions", add the application folder

**Note**: This is normal for unsigned executables. The application is safe.

---

### Issue 4: "MSVCP140.dll is missing"

**Solution**: Install Visual C++ Redistributable
1. Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
2. Run installer
3. Restart computer
4. Try running application again

---

### Issue 5: Application Starts But Shows Black Screen

**Possible causes**:
1. Camera in use by another application
2. Wrong camera index
3. Camera driver issue

**Solutions**:
1. Close other applications using camera (Skype, Zoom, etc.)
2. Try different camera index (see Issue 2)
3. Restart computer
4. Check camera in Windows Camera app first

---

### Issue 6: Slow Performance on Windows

**Solution 1** - Reduce processing load:

Edit `worker_threads.py`, line 77:
```python
self.process_every_n_frames = 5  # Increase from 3 to 5 or 7
```

**Solution 2** - Lower camera resolution:

Edit `worker_threads.py`, lines 34-35:
```python
self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)   # Lower from 640
self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Lower from 480
```

**Solution 3** - Use TensorFlow CPU optimization:
```cmd
set TF_ENABLE_ONEDNN_OPTS=0
```
(Already set in run_app.bat)

---

### Issue 7: Excel Export Doesn't Work

**Error**: `ModuleNotFoundError: No module named 'openpyxl'`

**Solution**:
```cmd
venv\Scripts\activate
pip install openpyxl
```

**Alternative**: Use CSV export instead
- CSV works everywhere
- Open in Excel, Google Sheets, LibreOffice

---

### Issue 8: First Run Takes Very Long

**This is NORMAL on first run!**

**Why**: DeepFace downloads emotion detection models (~50MB)

**Expected time**: 30-60 seconds on first run

**After first run**: Starts in 3-5 seconds

**Models downloaded to**:
- `C:\Users\<YourName>\.deepface\weights\`

**If stuck**: Check internet connection

---

## Windows vs Linux Differences

| Aspect | Linux | Windows |
|--------|-------|---------|
| Camera device | `/dev/video0` | Index 0, 1, 2... |
| File paths | `/` (forward slash) | `\` (backslash) |
| Executable | `python script.py` | `python script.py` or `.exe` |
| Virtual env | `source venv/bin/activate` | `venv\Scripts\activate.bat` |
| dlib install | Usually works | Needs C++ compiler |
| Camera API | V4L2 | DirectShow |

**All handled automatically by the code** - just be aware of differences.

---

## System Requirements

### Minimum:
- Windows 10 (64-bit)
- Intel Core i3 or equivalent
- 4GB RAM
- Webcam (720p)
- 1GB free disk space
- Internet (for initial model downloads)

### Recommended:
- Windows 10/11 (64-bit)
- Intel Core i5 or better
- 8GB RAM
- Webcam (1080p)
- 2GB free disk space
- Internet connection

### For building .exe (developers only):
- All above requirements
- Python 3.8-3.10 installed
- Visual C++ Build Tools
- CMake
- 10GB free disk space (build files are large)

---

## Building the Executable (For Developers)

If you want to build the `.exe` yourself:

### Step 1: Install Prerequisites
```cmd
pip install pyinstaller
```

### Step 2: Run Build Script
```cmd
python build_exe.py
```

### Step 3: Wait
Build takes 5-10 minutes

### Step 4: Test
```cmd
cd dist
AttendanceSystem.exe
```

### Output:
- `dist/AttendanceSystem.exe` (~500MB)
- Single file, no installation needed

---

## Packaging for Distribution

### For Your Client:

1. **Create folder structure**:
   ```
   AttendanceSystem_v1.0/
   ├── AttendanceSystem.exe
   ├── START_HERE.txt
   ├── User_Guide.pdf
   └── data/
       ├── enrollments.pkl (optional: your data)
       └── attendance.csv (optional: your data)
   ```

2. **ZIP the folder**:
   - Right-click folder
   - Send to → Compressed (zipped) folder

3. **Send to client** via:
   - Email (if under 25MB)
   - Google Drive / Dropbox / OneDrive
   - USB drive
   - WeTransfer (free for files up to 2GB)

---

## Client Installation Instructions (Ultra-Simple)

**For non-technical clients**, provide these instructions:

1. Extract the ZIP file
2. Double-click `START_HERE.txt` and read it
3. Double-click `AttendanceSystem.exe`
4. If Windows shows security warning:
   - Click "More info"
   - Click "Run anyway"
5. Application opens - ready to use!

**First time setup**:
1. Go to "Enrollment" tab
2. Enter person's name
3. Click "Start Enrollment"
4. Press SPACE 5 times (when face shows)
5. Done - person enrolled!

**Daily use**:
1. Open application
2. Go to "Live Recognition" tab
3. Click "Start Recognition"
4. Leave it running - automatic attendance logging

---

## Support for Your Client

**Provide to client**:
1. START_HERE.txt (ultra-simple instructions)
2. User_Guide.pdf (detailed guide with screenshots)
3. Your contact info for support

**Common client questions**:
- "It shows a security warning" → Normal, click "Run anyway"
- "Camera not working" → Close other apps, try restarting
- "Face not detected" → Better lighting, face camera directly
- "Slow performance" → Close other apps, ensure 8GB RAM

---

## Remote Support Tips

If client has issues:

1. **Ask for screenshot** of error message
2. **Check basics**:
   - Windows version (Win+R → `winver`)
   - Camera working in Windows Camera app?
   - Antivirus blocking?
3. **Remote desktop** (if needed):
   - Windows Quick Assist
   - TeamViewer
   - AnyDesk

---

## Performance Optimization for Windows

### Best performance settings:

1. **Windows Power Plan**:
   - Control Panel → Power Options
   - Select "High performance"

2. **Close unnecessary apps**:
   - Especially: Chrome, video players, other camera apps

3. **Disable Windows visual effects**:
   - Right-click This PC → Properties
   - Advanced system settings
   - Performance → Settings → "Adjust for best performance"

4. **Dedicated graphics** (if available):
   - NVIDIA Control Panel → Manage 3D settings
   - Add AttendanceSystem.exe
   - Set to "High-performance NVIDIA processor"

---

## Updating the Application

**For .exe version**:
1. Download new version
2. Replace old AttendanceSystem.exe
3. Keep `data/` folder (your enrollments preserved)

**For Python version**:
1. Backup data: `data\enrollments.pkl` and `data\attendance.csv`
2. Download new version
3. Replace Python files
4. Restore data files
5. Re-run if dependencies changed: `install_windows.bat`

---

## Uninstallation

**Standalone .exe version**:
- Simply delete the folder - no registry entries, no hidden files

**Python version**:
1. Delete the application folder
2. Optional: Uninstall Python (if not used for other purposes)

**Models folder** (optional cleanup):
- Delete: `C:\Users\<YourName>\.deepface\`
- Removes downloaded emotion detection models

---

## Getting Help

1. Check `TROUBLESHOOTING.md`
2. Check this `WINDOWS_SETUP.md`
3. Check `README.md`
4. Contact developer (your contact info here)

---

## Additional Resources

- **DeepFace models**: https://github.com/serengil/deepface
- **Face recognition**: https://github.com/ageitgey/face_recognition
- **PyQt5 docs**: https://www.riverbankcomputing.com/static/Docs/PyQt5/
- **dlib Windows**: https://github.com/z-mahmud22/Dlib_Windows_Python3.x

---

**Windows installation complete! Your client should be ready to run the application.**
