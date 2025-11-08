# Troubleshooting Guide

## Common Issues and Solutions

### 1. Qt Platform Plugin Error ✅ FIXED

**Error Message**:
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb"
This application failed to start because no Qt platform plugin could be initialized.
```

**Cause**: Conflict between OpenCV's bundled Qt and PyQt5

**Solution**: Use `opencv-python-headless` instead of `opencv-python`

```bash
source my_env/bin/activate
pip uninstall opencv-python
pip install opencv-python-headless
```

**Status**: ✅ Already fixed in the code (attendance_app.py lines 7-9)

---

### 2. TensorFlow GPU Warnings (Informational)

**Message**:
```
Could not find cuda drivers on your machine, GPU will not be used.
```

**Is this a problem?** NO - This is just informational

**Explanation**: TensorFlow is letting you know it will use CPU instead of GPU. The app works perfectly fine on CPU.

**If you want to silence these warnings**:
```bash
export TF_CPP_MIN_LOG_LEVEL=2
python attendance_app.py
```

Or add to the start of `attendance_app.py`:
```python
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
```

---

### 3. Camera Not Opening

**Symptoms**: Black screen in video preview, error message about camera

**Solutions**:

**A. Camera already in use**
```bash
# Check what's using the camera
lsof /dev/video0

# Close other applications (Cheese, Firefox with camera, etc.)
```

**B. Wrong camera index**

Edit `attendance_app.py` line where CameraThread is created:
```python
# Change from 0 to 1 or 2
self.camera_thread = CameraThread(camera_index=1)  # Try different numbers
```

**C. Camera permissions**
```bash
# Check if you have permission
ls -l /dev/video0

# Add yourself to video group
sudo usermod -a -G video $USER
# Then log out and log back in
```

**D. No camera detected**
```bash
# List video devices
v4l2-ctl --list-devices

# Install v4l-utils if needed
sudo apt install v4l-utils
```

---

### 4. Face Not Detected

**Symptoms**: No bounding box appears, "Position your face" message

**Solutions**:

1. **Improve Lighting**
   - Ensure face is well-lit
   - Avoid backlighting
   - Turn on room lights

2. **Camera Position**
   - Face camera directly
   - Keep face centered in frame
   - Stay 1-3 feet from camera

3. **Remove Obstructions**
   - Remove sunglasses
   - Push hair away from face
   - Ensure full face is visible

4. **Check Camera Focus**
   - Clean camera lens
   - Adjust camera angle
   - Move to better lit area

---

### 5. Slow Performance / Lag

**Symptoms**: Low FPS, choppy video, UI freezes

**Solutions**:

**A. Increase frame skip** (worker_threads.py line 77):
```python
self.process_every_n_frames = 5  # Change from 3 to 5 or higher
```

**B. Reduce camera resolution** (worker_threads.py lines 34-35):
```python
self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)   # Lower from 640
self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Lower from 480
```

**C. Reduce enrolled users**
- Delete unused enrollments
- Recognition is faster with fewer people

**D. Close other applications**
- Free up CPU and RAM
- Close browser, heavy applications

---

### 6. Emotion Detection Slow

**Symptoms**: "waiting..." stays for long time, emotions not detected

**Solutions**:

**A. Normal behavior**: First 3 seconds show "waiting..." - this is expected

**B. If it takes longer than 5 seconds**:

Edit `worker_threads.py` to disable emotion detection temporarily:
```python
# Comment out emotion detection in LiveRecognitionTab
# self.parent_app.emotion_thread.add_task(...)
```

**C. Use lighter emotion model**:
- DeepFace is CPU-intensive
- Consider using alternative emotion detection
- Or accept slower performance

---

### 7. ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'PyQt5'`

**Solution**:
```bash
source my_env/bin/activate  # Ensure venv is activated
pip install PyQt5 matplotlib seaborn openpyxl
```

**Verify installation**:
```bash
python -c "import PyQt5; print('PyQt5 OK')"
python -c "import cv2; print('OpenCV OK')"
python -c "import face_recognition; print('Face Recognition OK')"
```

---

### 8. Enrollment Not Saving

**Symptoms**: Enrollment completes but person not in list

**Solutions**:

**A. Check file permissions**:
```bash
ls -l enrollments.pkl
# Should be writable by you
```

**B. Check disk space**:
```bash
df -h .
```

**C. Manual verification**:
```python
import pickle
with open('enrollments.pkl', 'rb') as f:
    data = pickle.load(f)
    print(data.keys())  # Should show enrolled names
```

---

### 9. Attendance Not Logging

**Symptoms**: Person recognized but not appearing in attendance.csv

**Solutions**:

**A. Check if already logged today**
- Attendance logs only once per person per day
- Check Records tab to see if already logged

**B. Check CSV file**:
```bash
cat attendance.csv
# Verify recent entries
```

**C. Check file permissions**:
```bash
ls -l attendance.csv
touch attendance.csv  # Should work without error
```

---

### 10. Application Crashes on Startup

**Full error check**:
```bash
source my_env/bin/activate
python attendance_app.py
# Copy the full error message
```

**Common causes**:

**A. Missing dependencies**:
```bash
pip install -r requirements.txt
```

**B. Python version incompatible**:
```bash
python --version  # Should be 3.8, 3.9, or 3.10
```

**C. Corrupted pickle file**:
```bash
# Backup and reset
mv enrollments.pkl enrollments_backup.pkl
# App will create new empty file
```

---

### 11. Threading Error

**Error**: `QObject::moveToThread: Current thread is not the object's thread`

**Status**: This might appear but shouldn't prevent app from working

**If it causes crashes**:

Edit `attendance_app.py` to ensure threads start after UI is ready:
```python
def showEvent(self, event):
    super().showEvent(event)
    if not hasattr(self, '_threads_started'):
        self.start_threads()
        self._threads_started = True
```

---

### 12. Export to Excel Fails

**Error**: Issues when clicking "Export to Excel"

**Solution**:
```bash
pip install openpyxl
```

**Alternative**: Use CSV export instead
- CSV works everywhere
- Can open in Excel, LibreOffice, Google Sheets

---

## Getting More Help

### Debug Mode

Run with debug output:
```bash
python -u attendance_app.py 2>&1 | tee debug.log
```

This creates `debug.log` with all output for troubleshooting.

### Check System Info

```bash
echo "Python: $(python --version)"
echo "Qt: $(python -c 'from PyQt5.QtCore import QT_VERSION_STR; print(QT_VERSION_STR)')"
echo "OpenCV: $(python -c 'import cv2; print(cv2.__version__)')"
echo "Cameras: $(ls /dev/video* 2>/dev/null || echo 'None found')"
```

### Fallback to Terminal Version

If PyQt5 version has persistent issues, use the original:
```bash
python attedance.py
```

The terminal version still works and uses the same data files.

---

## Prevention Tips

1. **Always activate virtual environment**:
   ```bash
   source my_env/bin/activate
   ```

2. **Keep dependencies updated**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --upgrade
   ```

3. **Backup your data regularly**:
   ```bash
   cp enrollments.pkl enrollments_backup_$(date +%Y%m%d).pkl
   cp attendance.csv attendance_backup_$(date +%Y%m%d).csv
   ```

4. **Test camera before running**:
   ```bash
   # Quick camera test
   python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera FAIL'); cap.release()"
   ```

5. **Monitor resource usage**:
   ```bash
   # While app is running
   top  # Check CPU and memory
   ```

---

## Still Having Issues?

1. Review `README.md` for detailed setup instructions
2. Check `CODE_ANALYSIS.md` for technical details
3. Review the error message carefully
4. Try the terminal version as fallback
5. Check if your system meets requirements:
   - Python 3.8-3.10
   - Working webcam
   - 4GB+ RAM recommended
   - Ubuntu/Debian/Pop!_OS Linux

---

**Most issues are resolved by**:
1. Ensuring virtual environment is activated
2. Using `opencv-python-headless` instead of `opencv-python`
3. Having proper camera permissions
4. Good lighting for face detection
