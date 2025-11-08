# Quick Start Guide

## Installation (One-time setup)

```bash
# 1. Navigate to project directory
cd /home/mahmut/Documents/projects/attendance

# 2. Activate virtual environment
source my_env/bin/activate

# 3. Install new dependencies
./install_dependencies.sh
# OR manually:
pip install PyQt5 matplotlib seaborn openpyxl
```

## Running the Application

```bash
# Make sure virtual environment is activated
source my_env/bin/activate

# Run the modern PyQt5 app
python attendance_app.py
```

## First Time Usage

### Step 1: Enroll Yourself

1. Click on "Enrollment" tab
2. Enter your name in the "Name" field
3. Click "Start Enrollment"
4. Position your face in the camera view
5. When you see "Face detected", press SPACE or click "Capture Sample"
6. Repeat 5 times (or your chosen number of samples)
7. Wait for "Enrollment complete!" message

**Tips**:
- Look directly at camera
- Ensure good lighting
- Capture from slightly different angles
- Keep face clearly visible

### Step 2: Test Recognition

1. Click on "Live Recognition" tab
2. Click "Start Recognition" button
3. Show your face to the camera
4. Wait 3 seconds
5. You should see:
   - Green box around your face
   - Your name displayed
   - Emotion detected
   - Attendance logged automatically

### Step 3: View Records

1. Click on "Records" tab
2. See all attendance entries
3. Try filtering by date
4. Export to CSV or Excel if needed

### Step 4: Check Analytics

1. Click on "Dashboard" tab
2. Click "Refresh Dashboard"
3. View attendance trends and emotion distribution

## Common Issues

### Camera not working
```bash
# Check if camera is available
ls /dev/video*

# If camera is already in use, close other applications
```

### Dependencies missing
```bash
# Re-run installation
source my_env/bin/activate
./install_dependencies.sh

# Or manually:
pip install -r requirements.txt
```

### Qt Platform Plugin Error
```bash
# Fix: Use opencv-python-headless
pip uninstall opencv-python
pip install opencv-python-headless
```
**Note**: This is already fixed in the code!

### Application crashes
```bash
# Check Python version (should be 3.8-3.10)
python --version

# Reinstall PyQt5
pip uninstall PyQt5
pip install PyQt5==5.15.11
```

## Keyboard Shortcuts

- **SPACE**: Capture sample during enrollment
- **ESC**: (Future) Exit fullscreen

## Daily Usage Workflow

1. **Morning**:
   ```bash
   source my_env/bin/activate
   python attendance_app.py
   ```

2. **Start Recognition**:
   - Open "Live Recognition" tab
   - Click "Start Recognition"
   - Leave running

3. **People arrive**:
   - Face detected automatically
   - Attendance logged after 3 seconds
   - No manual intervention needed

4. **End of Day**:
   - Click "Records" tab
   - Filter by today's date
   - Export to Excel for reporting
   - Close application

## Comparison: Old vs New

| Feature | Old (attedance.py) | New (attendance_app.py) |
|---------|-------------------|------------------------|
| UI | Basic Tkinter | Modern PyQt5 |
| Performance | Slow, laggy | Fast, smooth |
| Enrollment | Manual/buggy | Automated workflow |
| Records | Console only | Filterable table |
| Export | CSV only | CSV + Excel |
| Analytics | None | Charts + stats |
| Threading | Single thread | Multi-threaded |

## File Locations

- **Enrollments**: `enrollments.pkl` (binary)
- **Attendance**: `attendance.csv` (text)
- **App**: `attendance_app.py` (main)
- **Threads**: `worker_threads.py` (background)
- **Old version**: `attedance.py` (backup)

## Getting Help

1. Check `README.md` for detailed documentation
2. Check `CODE_ANALYSIS.md` for technical details
3. Review error messages in terminal
4. Ensure camera permissions are granted

## Next Steps

After basic setup works:

1. **Enroll multiple people**
   - Have each person go through enrollment
   - Build your database

2. **Customize settings**
   - Adjust recognition tolerance
   - Change number of samples
   - Modify processing frame rate

3. **Export reports**
   - Daily attendance reports
   - Weekly summaries
   - Emotion analysis

4. **Backup data**
   ```bash
   cp enrollments.pkl enrollments_backup.pkl
   cp attendance.csv attendance_backup.csv
   ```

## Support

For issues or questions:
- Review troubleshooting in README.md
- Check CODE_ANALYSIS.md for bug fixes
- Verify all dependencies are installed

---

**Ready to start!** Run `python attendance_app.py` and begin enrolling users.
