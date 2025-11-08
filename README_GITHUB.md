# Face Recognition Attendance System

A modern, cross-platform desktop application for automated attendance tracking using face recognition and emotion detection.

![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

## 🎯 Features

- **Real-time Face Recognition** - Identify individuals using webcam with high accuracy
- **Emotion Detection** - Detect and log emotional state (happy, sad, angry, neutral, etc.)
- **Automatic Attendance Logging** - One-time daily attendance tracking per person
- **User Management** - Easy enrollment with multi-sample face capture
- **Rich Reporting** - View, filter, and export attendance records (CSV/Excel)
- **Analytics Dashboard** - Visual charts and statistics
- **Multi-threaded Architecture** - Smooth performance with background processing
- **Cross-platform** - Works on Linux and Windows

## 📸 Screenshots

### Live Recognition
Real-time face detection with emotion analysis and automatic attendance logging.

### Enrollment
Simple wizard to enroll new people with progress tracking.

### Records & Analytics
Comprehensive reporting with filtering, export, and visual analytics.

## 🚀 Quick Start

### Linux

```bash
# Clone repository
git clone https://github.com/yourusername/attendance-tracker.git
cd attendance-tracker

# Create virtual environment
python3 -m venv my_env
source my_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python attendance_app.py
```

### Windows

```cmd
# Clone repository
git clone https://github.com/yourusername/attendance-tracker.git
cd attendance-tracker

# Run installation script
install_windows.bat

# Launch application
run_app.bat
```

## 📋 Requirements

### System Requirements
- **OS**: Linux (Ubuntu, Pop!_OS, Debian) or Windows 10/11
- **Python**: 3.8, 3.9, or 3.10
- **Webcam**: Built-in or USB camera
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space

### Python Dependencies
- PyQt5 - Modern GUI framework
- opencv-python-headless - Computer vision
- face-recognition - Face detection and recognition
- deepface - Emotion detection
- pandas - Data management
- matplotlib - Visualization
- tensorflow - Deep learning backend

See `requirements.txt` for complete list.

## 📖 Documentation

### Quick Guides
- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[START_HERE.txt](START_HERE.txt)** - Ultra-simple client guide
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

### Platform-Specific
- **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** - Windows installation guide
- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Windows .exe deployment
- **[WINDOWS_DEPLOYMENT_SUMMARY.md](WINDOWS_DEPLOYMENT_SUMMARY.md)** - Quick deployment reference

### Technical
- **[CODE_ANALYSIS.md](CODE_ANALYSIS.md)** - Architecture and bug fixes
- **[README.md](README.md)** - Complete documentation

## 🎓 Usage

### 1. Enroll People

1. Open application
2. Go to **Enrollment** tab
3. Enter person's name
4. Click **Start Enrollment**
5. Press **SPACEBAR** 5 times to capture face samples
6. Done! Person enrolled

### 2. Start Recognition

1. Go to **Live Recognition** tab
2. Click **Start Recognition**
3. Automatic attendance tracking begins
4. Each enrolled person logged once per day

### 3. View Records

1. Go to **Records** tab
2. Filter by date range or name
3. Export to CSV or Excel
4. View statistics

### 4. Analytics

1. Go to **Dashboard** tab
2. Click **Refresh Dashboard**
3. View attendance trends and emotion distribution

## 🏗️ Architecture

### Multi-threaded Design

```
┌─────────────────────────────────────────┐
│          Main GUI Thread                │
│            (PyQt5)                      │
└─────────────────────────────────────────┘
           │         │         │
     ┌─────┴─┐   ┌──┴───┐   ┌┴──────┐
     │Camera │   │Face  │   │Emotion│
     │Thread │   │Recog │   │Thread │
     └───────┘   └──────┘   └───────┘
```

- **CameraThread**: 30 FPS video capture
- **FaceRecognitionThread**: Face detection (every 3rd frame)
- **EmotionDetectionThread**: Async emotion analysis
- **EnrollmentThread**: Dedicated enrollment processing

### Data Flow

```
Camera → Face Detection → Recognition → Emotion → Logging
                                                     ↓
                                            attendance.csv
```

## 🛠️ Development

### Project Structure

```
attendance-tracker/
├── attendance_app.py          # Main PyQt5 application
├── worker_threads.py          # Background processing threads
├── attedance.py              # Original terminal version (legacy)
├── requirements.txt          # Python dependencies
├── install_windows.bat       # Windows installation script
├── run_app.bat              # Windows launcher
├── build_exe.py             # PyInstaller build script
└── docs/                    # Documentation
    ├── QUICKSTART.md
    ├── WINDOWS_SETUP.md
    └── ...
```

### Building Windows Executable

```cmd
# On Windows machine
pip install pyinstaller
python build_exe.py

# Output: dist/AttendanceSystem.exe (~500MB)
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete instructions.

## 🐛 Known Issues & Solutions

### Qt Platform Plugin Error (Linux)
**Fixed**: Use `opencv-python-headless` instead of `opencv-python`

### dlib Installation Fails (Windows)
**Solution**: Use pre-built wheels from [Dlib Windows](https://github.com/z-mahmud22/Dlib_Windows_Python3.x)

### Camera Not Detected
**Solution**: Check camera permissions and try different camera indices

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more solutions.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project uses the following open-source libraries:

- **face_recognition** - MIT License
- **DeepFace** - MIT License
- **OpenCV** - Apache 2.0 License
- **PyQt5** - GPL v3 License
- **TensorFlow** - Apache 2.0 License

**Note**: PyQt5 is GPL licensed. For commercial use, consider PyQt5 commercial license or switch to PySide6 (LGPL).

## 🔒 Privacy & Data Protection

This application processes biometric data (face images). Users should:

- Obtain consent before enrolling individuals
- Comply with GDPR, CCPA, and local privacy laws
- Implement appropriate data security measures
- Provide clear privacy notices to end users

## 🙏 Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition) by Adam Geitgey
- [DeepFace](https://github.com/serengil/deepface) by Sefik Ilkin Serengil
- [OpenCV](https://opencv.org/)
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/)

## 📧 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/attendance-tracker/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/attendance-tracker/discussions)
- **Email**: your.email@example.com

## 🗺️ Roadmap

- [ ] SQLite database support (replace CSV)
- [ ] Multi-camera support
- [ ] Face anti-spoofing detection
- [ ] Cloud sync for attendance data
- [ ] Mobile app companion
- [ ] REST API for integration
- [ ] Docker deployment
- [ ] Raspberry Pi support

## ⭐ Star History

If you find this project useful, please consider giving it a star!

## 📊 Statistics

- **Lines of Code**: ~2,500
- **Files**: 20+
- **Dependencies**: 13
- **Documentation Pages**: 100+

---

**Made with ❤️ for automated attendance tracking**
