# Face Recognition Attendance System

A modern desktop application for attendance tracking using face recognition and emotion detection, built with PyQt5.

## Features

- **Real-time Face Recognition**: Identify enrolled individuals using webcam
- **Emotion Detection**: Detect and log emotional state during attendance
- **User Enrollment**: Easy interface to enroll new people with multiple face samples
- **Attendance Records**: View, filter, and export attendance data (CSV/Excel)
- **Analytics Dashboard**: Visual charts showing attendance trends and emotion distribution
- **Multi-threaded Architecture**: Smooth performance with background processing
- **Modern UI**: Clean, intuitive PyQt5 interface with tabbed navigation

## Installation

### 1. Ensure you have Python 3.8-3.10 installed

```bash
python3 --version
```

### 2. Activate your virtual environment

```bash
source my_env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**Note**: If you encounter issues installing `dlib`, you may need to install CMake first:

```bash
sudo apt-get install cmake  # On Ubuntu/Debian
# or
brew install cmake  # On macOS
```

## Usage

### Running the Application

```bash
python attendance_app.py
```

### User Interface Guide

#### 1. Live Recognition Tab

**Purpose**: Real-time face recognition and attendance logging

**How to use**:
1. Click "Start Recognition" to begin monitoring
2. Face detection will automatically identify enrolled individuals
3. After 3 seconds of recognition, emotion will be detected
4. Attendance is automatically logged once per person per day
5. View recent attendance in the right panel

**Features**:
- Green bounding boxes around recognized faces
- Real-time emotion display
- Status indicators (enrolled count, logged today)
- Recent attendance log

#### 2. Enrollment Tab

**Purpose**: Register new people in the system

**How to enroll someone**:
1. Enter the person's name in the "Name" field
2. Set the number of samples to capture (3-10, recommended: 5)
3. Click "Start Enrollment"
4. Position the person's face clearly in the camera view
5. Press SPACE key or "Capture Sample" button when face is detected
6. Repeat until all samples are captured
7. Enrollment completes automatically

**Features**:
- Live preview with face detection indicator
- Progress bar showing capture progress
- List of enrolled people with sample counts
- Delete enrolled users

**Tips**:
- Capture samples from different angles
- Ensure good lighting
- Keep face clearly visible
- Avoid shadows or obstructions

#### 3. Records Tab

**Purpose**: View and manage attendance history

**Features**:
- **Date Range Filter**: Select start and end dates
- **Name Filter**: Search by person's name
- **Export**: Save filtered data to CSV or Excel
- **Statistics**: View total record count

**How to filter records**:
1. Set "From" and "To" dates
2. Optionally enter a name to filter by
3. Click "Apply Filter"
4. Export results using CSV or Excel buttons

#### 4. Dashboard Tab

**Purpose**: Visual analytics and statistics

**Charts**:
- **Daily Attendance Trend**: Line graph showing attendance over time
- **Emotion Distribution**: Pie chart of detected emotions

**Statistics**:
- Total records count
- Unique people count
- Today's attendance count
- Most common emotion

Click "Refresh Dashboard" to update with latest data.

## File Structure

```
attendance/
├── attendance_app.py       # Main PyQt5 application
├── worker_threads.py       # Background processing threads
├── attedance.py           # Original terminal version (backup)
├── enrollments.pkl        # Stored face encodings
├── attendance.csv         # Attendance records
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Technical Details

### Architecture

The application uses a multi-threaded architecture for optimal performance:

- **CameraThread**: Captures video frames from webcam
- **FaceRecognitionThread**: Processes frames for face recognition
- **EmotionDetectionThread**: Detects emotions asynchronously
- **EnrollmentThread**: Handles face sample capture during enrollment

### Data Storage

- **enrollments.pkl**: Binary file storing face encodings using pickle
- **attendance.csv**: CSV file with columns: Name, Emotion, Timestamp

### Recognition Process

1. Frame captured from camera (30 FPS)
2. Face detection using `face_recognition` library (every 3rd frame)
3. Face encoding compared against enrolled encodings
4. If match found (within tolerance), person identified
5. After 3 seconds, emotion detected using DeepFace
6. Attendance logged to CSV (once per person per day)

### Performance Optimizations

- Frame processing limited to every 3rd frame
- Face recognition runs in separate thread
- Emotion detection queued asynchronously
- Pre-computed average face encodings

## Troubleshooting

### Camera not opening
- Check if camera is already in use by another application
- Verify camera permissions
- Try changing camera index in code (default is 0)

### Face not detected
- Ensure adequate lighting
- Move closer to camera
- Remove obstructions (glasses, masks if applicable)

### Slow performance
- Reduce number of enrolled people
- Increase `process_every_n_frames` in worker_threads.py
- Close other resource-intensive applications

### Installation errors

**dlib installation fails**:
```bash
# Install build dependencies
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
```

**TensorFlow/DeepFace issues**:
```bash
# Use CPU-only version if needed
pip uninstall tensorflow
pip install tensorflow-cpu
```

## Comparison: New vs Old Version

### Old Version (attedance.py - Tkinter)
- Basic Tkinter UI
- Single-threaded (UI freezes during processing)
- Limited features
- Performance issues
- Image display bug (line 197-198)
- Enrollment incomplete

### New Version (attendance_app.py - PyQt5)
- Modern, professional UI
- Multi-threaded architecture
- Comprehensive features (dashboard, export, analytics)
- Smooth performance
- Bug-free implementation
- Complete enrollment workflow

## Advanced Configuration

### Adjust Face Recognition Tolerance

In `attendance_app.py`, line where `set_enrollments` is called:

```python
self.face_recognition_thread.set_enrollments(self.enrollments, tolerance=0.6)
```

- Lower value (0.4-0.5): More strict matching, fewer false positives
- Higher value (0.6-0.7): More lenient matching, more false positives

### Change Processing Frame Rate

In `worker_threads.py`, `FaceRecognitionThread` class:

```python
self.process_every_n_frames = 3  # Process every 3rd frame
```

Increase this number for better performance on slower systems.

### Change Camera Resolution

In `worker_threads.py`, `CameraThread.run()`:

```python
self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Width
self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Height
```

## Future Enhancements

Potential improvements:
- SQLite database instead of CSV
- Multiple camera support
- Face anti-spoofing detection
- Cloud sync for attendance data
- Email notifications
- Mobile app companion
- Dark/light theme toggle
- Admin authentication

## License

This project is for educational and internal use.

## Credits

Built using:
- **face_recognition** - Face detection and recognition
- **DeepFace** - Emotion detection
- **PyQt5** - GUI framework
- **OpenCV** - Computer vision
- **pandas** - Data management
- **matplotlib** - Visualization
