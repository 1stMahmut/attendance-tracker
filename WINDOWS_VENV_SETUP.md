# Setting Up Python Virtual Environment on Windows

Complete guide for creating and using Python virtual environments on Windows.

---

## 📋 Prerequisites

1. **Python installed** (3.8, 3.9, or 3.10)
   - Download from: https://www.python.org/downloads/
   - ✅ **IMPORTANT**: Check "Add Python to PATH" during installation!

2. **Verify Python is installed**:
   ```cmd
   python --version
   ```
   Should show: `Python 3.10.x` (or 3.8/3.9)

3. **If `python` doesn't work, try**:
   ```cmd
   py --version
   ```

---

## 🚀 Quick Start (3 Steps)

### Step 1: Open Command Prompt

Press `Win + R`, type `cmd`, press Enter

Or:
- Press `Win` key, type "cmd", press Enter
- Or use PowerShell (same commands work)

### Step 2: Navigate to Your Project

```cmd
cd C:\Users\YourName\Documents\attendance-tracker
```

### Step 3: Create Virtual Environment

```cmd
python -m venv venv
```

**Done!** Virtual environment created in `venv` folder.

---

## 📖 Detailed Instructions

### Method 1: Using Command Prompt (Recommended)

#### 1. Create Virtual Environment

```cmd
# Navigate to your project folder
cd C:\path\to\your\project

# Create virtual environment named "venv"
python -m venv venv
```

**What this does**:
- Creates a `venv` folder
- Installs Python + pip inside it
- Isolates your project dependencies

#### 2. Activate Virtual Environment

```cmd
venv\Scripts\activate
```

**You'll see**:
```cmd
(venv) C:\path\to\your\project>
```

The `(venv)` prefix means it's active! ✅

#### 3. Install Packages

```cmd
# Now you can install packages
pip install numpy pandas PyQt5

# Or install from requirements.txt
pip install -r requirements.txt
```

#### 4. Deactivate (When Done)

```cmd
deactivate
```

The `(venv)` prefix disappears.

---

### Method 2: Using PowerShell

#### 1. Open PowerShell

Press `Win + X`, select "Windows PowerShell"

#### 2. Check Execution Policy

```powershell
Get-ExecutionPolicy
```

If it shows `Restricted`, you need to change it:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Type `Y` and press Enter.

#### 3. Create Virtual Environment

```powershell
cd C:\path\to\your\project
python -m venv venv
```

#### 4. Activate Virtual Environment

```powershell
venv\Scripts\Activate.ps1
```

**You'll see**:
```powershell
(venv) PS C:\path\to\your\project>
```

#### 5. Deactivate

```powershell
deactivate
```

---

### Method 3: Using Git Bash (If Installed)

```bash
# Navigate to project
cd /c/path/to/your/project

# Create virtual environment
python -m venv venv

# Activate (Linux-style)
source venv/Scripts/activate

# Deactivate
deactivate
```

---

## 🔧 For Your Attendance Tracker Project

### Complete Setup

```cmd
# 1. Clone repository (if not already)
cd C:\Users\YourName\Documents
git clone https://github.com/1stMahmut/attendance-tracker.git
cd attendance-tracker

# 2. Create virtual environment
python -m venv venv

# 3. Activate it
venv\Scripts\activate

# 4. Upgrade pip
python -m pip install --upgrade pip

# 5. Install dependencies
pip install -r requirements.txt
```

**Note**: This will take 5-10 minutes and requires ~2GB download.

---

## 🎯 Using the Automated Script

Your project includes `install_windows.bat` which does all this automatically!

### Just Run:

```cmd
cd attendance-tracker
install_windows.bat
```

The script will:
1. ✅ Check Python version
2. ✅ Create virtual environment
3. ✅ Activate it
4. ✅ Install all dependencies
5. ✅ Handle special cases (like dlib)

**Then to run the app**:

```cmd
run_app.bat
```

This activates the venv and runs the application automatically!

---

## 💡 Common Commands Reference

### Creating Virtual Environments

```cmd
# Standard name "venv"
python -m venv venv

# Custom name
python -m venv myenv

# Specific Python version (if multiple installed)
py -3.10 -m venv venv
```

### Activating

```cmd
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1

# Git Bash
source venv/Scripts/activate
```

### Checking Status

```cmd
# Check if venv is active
where python
# Should show: C:\path\to\project\venv\Scripts\python.exe

# List installed packages
pip list

# Show package location
pip show numpy
```

### Managing Packages

```cmd
# Install single package
pip install numpy

# Install specific version
pip install numpy==1.24.0

# Install from requirements.txt
pip install -r requirements.txt

# Upgrade package
pip install --upgrade numpy

# Uninstall package
pip uninstall numpy
```

### Saving Dependencies

```cmd
# Save currently installed packages
pip freeze > requirements.txt

# View what's installed
pip list
```

### Deactivating

```cmd
deactivate
```

---

## 🐛 Troubleshooting

### Problem 1: "python is not recognized"

**Cause**: Python not in PATH

**Solution**:
```cmd
# Try this instead
py -m venv venv

# Or reinstall Python and check "Add to PATH"
```

### Problem 2: PowerShell won't activate (access denied)

**Cause**: Execution policy restriction

**Solution**:
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again
venv\Scripts\Activate.ps1
```

### Problem 3: "Cannot activate virtual environment"

**Cause**: Antivirus blocking

**Solution**:
- Add `venv\Scripts\activate.bat` to antivirus exceptions
- Or use Command Prompt instead of PowerShell

### Problem 4: Packages install to wrong location

**Cause**: Virtual environment not activated

**Check**:
```cmd
# Should show (venv) prefix
(venv) C:\path\to\project>

# If not, activate it
venv\Scripts\activate
```

### Problem 5: "pip is not recognized"

**Solution**:
```cmd
# Use full path
venv\Scripts\pip.exe install numpy

# Or use python -m
python -m pip install numpy
```

### Problem 6: Virtual environment folder is huge

**Cause**: Normal! Contains Python + packages

**Size**:
- Empty venv: ~10-20 MB
- With your packages: ~1-2 GB (TensorFlow is large)

**This is normal and expected!**

---

## 📁 Virtual Environment Structure

```
venv/
├── Scripts/           # Executable files
│   ├── activate.bat      # Activation script (CMD)
│   ├── Activate.ps1      # Activation script (PowerShell)
│   ├── deactivate.bat    # Deactivation script
│   ├── python.exe        # Python interpreter
│   └── pip.exe           # Package installer
├── Lib/               # Python libraries
│   └── site-packages/    # Installed packages go here
├── Include/           # C headers
└── pyvenv.cfg         # Configuration
```

**Important**: The entire `venv` folder is ~1-2GB after installing all packages!

---

## ✅ Verification Steps

### Check Everything is Working

```cmd
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Check Python location
where python
# Should show: ...\venv\Scripts\python.exe

# 3. Check pip location
where pip
# Should show: ...\venv\Scripts\pip.exe

# 4. Test import
python -c "import sys; print(sys.prefix)"
# Should show: ...\venv

# 5. List packages
pip list
```

---

## 🎯 Best Practices

### DO:
✅ Create venv in project root
✅ Name it `venv` (convention)
✅ Add `venv/` to `.gitignore`
✅ Always activate before installing packages
✅ Keep `requirements.txt` updated

### DON'T:
❌ Commit `venv/` to Git (too large)
❌ Move venv folder (paths are hardcoded)
❌ Install packages without activating venv
❌ Delete venv while it's active
❌ Modify files inside venv manually

---

## 🔄 Working with Multiple Projects

```cmd
# Project 1
cd C:\Projects\attendance-tracker
venv\Scripts\activate
# Work on attendance tracker
deactivate

# Project 2
cd C:\Projects\another-project
venv\Scripts\activate
# Work on another project
deactivate
```

Each project has its own isolated environment!

---

## 📝 Daily Workflow

### Morning:
```cmd
# Navigate to project
cd C:\Projects\attendance-tracker

# Activate environment
venv\Scripts\activate

# Start coding!
```

### During Development:
```cmd
# Install new package
pip install some-package

# Run your code
python attendance_app.py

# Test
python -m pytest
```

### End of Day:
```cmd
# Save dependencies if changed
pip freeze > requirements.txt

# Deactivate
deactivate
```

---

## 🆘 Quick Help Commands

```cmd
# Python version in venv
python --version

# Pip version
pip --version

# Python location
where python

# List all packages
pip list

# Search for package
pip search package-name

# Show package info
pip show numpy

# Check for outdated packages
pip list --outdated

# Upgrade all packages (careful!)
pip list --outdated --format=freeze | ForEach-Object { pip install --upgrade ($_ -split '==')[0] }
```

---

## 🎬 Video Tutorial Steps

If you prefer visual learning:

1. Open Command Prompt
2. Navigate to your project: `cd C:\path\to\project`
3. Create venv: `python -m venv venv`
4. Activate: `venv\Scripts\activate`
5. See `(venv)` prefix? You're good! ✅
6. Install packages: `pip install -r requirements.txt`
7. Run your code: `python your_script.py`
8. Done? `deactivate`

---

## 🎓 Complete Example Session

```cmd
# Starting fresh
C:\Users\Mahmut> cd Documents

# Navigate to project
C:\Users\Mahmut\Documents> git clone https://github.com/1stMahmut/attendance-tracker.git
C:\Users\Mahmut\Documents> cd attendance-tracker

# Create virtual environment
C:\Users\Mahmut\Documents\attendance-tracker> python -m venv venv

# Activate it
C:\Users\Mahmut\Documents\attendance-tracker> venv\Scripts\activate
(venv) C:\Users\Mahmut\Documents\attendance-tracker>

# Upgrade pip
(venv) C:\Users\Mahmut\Documents\attendance-tracker> python -m pip install --upgrade pip

# Install dependencies
(venv) C:\Users\Mahmut\Documents\attendance-tracker> pip install -r requirements.txt

# Wait 5-10 minutes...

# Check installations
(venv) C:\Users\Mahmut\Documents\attendance-tracker> pip list

# Run application
(venv) C:\Users\Mahmut\Documents\attendance-tracker> python attendance_app.py

# Application runs! 🎉

# When done
(venv) C:\Users\Mahmut\Documents\attendance-tracker> deactivate
C:\Users\Mahmut\Documents\attendance-tracker>
```

---

## 📚 Additional Resources

- **Official Python venv docs**: https://docs.python.org/3/library/venv.html
- **pip documentation**: https://pip.pypa.io/
- **virtualenv (alternative)**: https://virtualenv.pypa.io/
- **conda (another option)**: https://docs.conda.io/

---

## 🎯 Summary

### Three Simple Commands:

```cmd
# 1. Create
python -m venv venv

# 2. Activate
venv\Scripts\activate

# 3. Install
pip install -r requirements.txt
```

**That's it!** You now have an isolated Python environment for your project.

---

## 🚀 Next Steps

After setting up venv:

1. ✅ Install dependencies: `pip install -r requirements.txt`
2. ✅ Run application: `python attendance_app.py`
3. ✅ Or use automated script: `run_app.bat`

For building .exe:
4. ✅ Install PyInstaller: `pip install pyinstaller`
5. ✅ Build: `python build_exe.py`

---

**Virtual environment setup complete!** 🎉

Need help? Check:
- WINDOWS_SETUP.md
- TROUBLESHOOTING.md
- install_windows.bat (automated)
