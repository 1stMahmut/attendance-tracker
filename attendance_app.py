"""
Modern PyQt5-based Attendance System with Face Recognition and Emotion Detection
"""
import os
import sys

# Fix Qt plugin conflicts between OpenCV and PyQt5
os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = ""
os.environ.pop("QT_QPA_PLATFORM", None)

import cv2
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QLineEdit, QMessageBox, QProgressBar, QFrame, QGroupBox,
    QComboBox, QDateEdit, QFileDialog, QSpinBox, QCheckBox
)
from PyQt5.QtCore import Qt, QTimer, QDate, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap, QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from worker_threads import (
    CameraThread, FaceRecognitionThread,
    EmotionDetectionThread, EnrollmentThread
)


class LiveRecognitionTab(QWidget):
    """Tab for live face recognition and attendance logging"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.current_frame = None
        self.face_timers = {}
        self.logged_today = set()
        self.recognition_active = False

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Left side - Video feed
        left_layout = QVBoxLayout()

        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setMaximumSize(640, 480)
        self.video_label.setStyleSheet("border: 2px solid #3498db; background-color: black;")
        self.video_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.video_label)

        # Control buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start Recognition")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        self.start_btn.clicked.connect(self.start_recognition)

        self.stop_btn = QPushButton("Stop Recognition")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_recognition)
        self.stop_btn.setEnabled(False)

        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        left_layout.addLayout(btn_layout)

        # Right side - Status and recent logs
        right_layout = QVBoxLayout()

        # Status group
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()

        self.status_enrolled = QLabel("Enrolled: 0 people")
        self.status_enrolled.setFont(QFont('Arial', 12))
        self.status_logged = QLabel("Logged Today: 0")
        self.status_logged.setFont(QFont('Arial', 12))
        self.status_mode = QLabel("Mode: Idle")
        self.status_mode.setFont(QFont('Arial', 12, QFont.Bold))

        status_layout.addWidget(self.status_enrolled)
        status_layout.addWidget(self.status_logged)
        status_layout.addWidget(self.status_mode)
        status_group.setLayout(status_layout)
        right_layout.addWidget(status_group)

        # Recent attendance logs
        logs_group = QGroupBox("Recent Attendance")
        logs_layout = QVBoxLayout()

        self.recent_table = QTableWidget()
        self.recent_table.setColumnCount(3)
        self.recent_table.setHorizontalHeaderLabels(["Name", "Emotion", "Time"])
        self.recent_table.setColumnWidth(0, 120)
        self.recent_table.setColumnWidth(1, 100)
        self.recent_table.setColumnWidth(2, 150)
        logs_layout.addWidget(self.recent_table)

        logs_group.setLayout(logs_layout)
        right_layout.addWidget(logs_group)

        layout.addLayout(left_layout, 2)
        layout.addLayout(right_layout, 1)
        self.setLayout(layout)

    def update_frame(self, frame):
        """Update video display with annotations"""
        self.current_frame = frame.copy()

    def update_video_display(self, face_locations, names, confidences):
        """Draw bounding boxes and labels on video"""
        if self.current_frame is None:
            return

        frame = self.current_frame.copy()

        for (top, right, bottom, left), name, confidence in zip(
            face_locations, names, confidences
        ):
            # Draw rectangle
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

            # Get emotion if available
            emotion = self.face_timers.get(name, {}).get('emotion', 'waiting...')

            # Draw label
            label = f"{name} - {emotion}"
            if confidence > 0:
                label += f" ({confidence:.0%})"

            cv2.putText(
                frame, label, (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
            )

        # Convert to Qt format
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)

        self.video_label.setPixmap(pixmap)

    def start_recognition(self):
        """Start recognition mode"""
        self.recognition_active = True
        self.face_timers = {}
        self.logged_today = set()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_mode.setText("Mode: Recognition Active")
        self.status_mode.setStyleSheet("color: #27ae60;")

    def stop_recognition(self):
        """Stop recognition mode"""
        self.recognition_active = False
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_mode.setText("Mode: Idle")
        self.status_mode.setStyleSheet("color: #95a5a6;")

    def update_status(self, enrolled_count):
        """Update status display"""
        self.status_enrolled.setText(f"Enrolled: {enrolled_count} people")
        self.status_logged.setText(f"Logged Today: {len(self.logged_today)}")

    def handle_face_detected(self, face_locations, names, confidences):
        """Handle recognized faces"""
        if not self.recognition_active:
            self.update_video_display(face_locations, names, confidences)
            return

        current_time = datetime.now()

        for idx, (name, confidence) in enumerate(zip(names, confidences)):
            if name == "Unknown":
                continue

            # Initialize timer if new face
            if name not in self.face_timers:
                self.face_timers[name] = {
                    'first_seen': current_time,
                    'emotion': 'waiting...',
                    'emotion_requested': False
                }

            # Calculate elapsed time
            elapsed = (current_time - self.face_timers[name]['first_seen']).total_seconds()

            # Request emotion after 3 seconds
            if elapsed >= 3 and not self.face_timers[name]['emotion_requested']:
                self.face_timers[name]['emotion_requested'] = True
                if self.parent_app and self.current_frame is not None:
                    face_loc = face_locations[idx]
                    self.parent_app.emotion_thread.add_task(
                        self.current_frame, face_loc, name
                    )

        self.update_video_display(face_locations, names, confidences)

    def handle_emotion_detected(self, name, emotion):
        """Handle emotion detection result"""
        if name in self.face_timers:
            self.face_timers[name]['emotion'] = emotion

            # Log attendance if not logged today
            if name not in self.logged_today:
                self.log_attendance(name, emotion)
                self.logged_today.add(name)

    def log_attendance(self, name, emotion):
        """Log attendance to CSV"""
        csv_path = 'attendance.csv'
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        data = {
            'Name': [name],
            'Emotion': [emotion],
            'Timestamp': [timestamp]
        }
        df = pd.DataFrame(data)

        if Path(csv_path).exists():
            df.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_path, index=False)

        # Update recent table
        self.add_to_recent_table(name, emotion, timestamp)
        self.update_status(
            len(self.parent_app.enrollments) if self.parent_app else 0
        )

        # Show notification
        QMessageBox.information(
            self, "Attendance Logged",
            f"{name} marked present with {emotion} emotion"
        )

    def add_to_recent_table(self, name, emotion, timestamp):
        """Add entry to recent attendance table"""
        row_position = 0
        self.recent_table.insertRow(row_position)
        self.recent_table.setItem(row_position, 0, QTableWidgetItem(name))
        self.recent_table.setItem(row_position, 1, QTableWidgetItem(emotion))
        self.recent_table.setItem(row_position, 2, QTableWidgetItem(timestamp))

        # Keep only last 10 entries
        if self.recent_table.rowCount() > 10:
            self.recent_table.removeRow(10)


class EnrollmentTab(QWidget):
    """Tab for enrolling new people"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.current_frame = None
        self.enrollment_active = False
        self.current_name = None
        self.captured_encodings = []

        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()

        # Left - Video and controls
        left_layout = QVBoxLayout()

        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setMaximumSize(640, 480)
        self.video_label.setStyleSheet("border: 2px solid #9b59b6; background-color: black;")
        self.video_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.video_label)

        # Enrollment controls
        enroll_group = QGroupBox("Enroll New Person")
        enroll_layout = QVBoxLayout()

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter person's name")
        name_layout.addWidget(self.name_input)
        enroll_layout.addLayout(name_layout)

        samples_layout = QHBoxLayout()
        samples_layout.addWidget(QLabel("Samples:"))
        self.samples_spin = QSpinBox()
        self.samples_spin.setMinimum(3)
        self.samples_spin.setMaximum(10)
        self.samples_spin.setValue(5)
        samples_layout.addWidget(self.samples_spin)
        samples_layout.addStretch()
        enroll_layout.addLayout(samples_layout)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        enroll_layout.addWidget(self.progress_bar)

        btn_layout = QHBoxLayout()
        self.start_enroll_btn = QPushButton("Start Enrollment")
        self.start_enroll_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.start_enroll_btn.clicked.connect(self.start_enrollment)

        self.capture_btn = QPushButton("Capture Sample (SPACE)")
        self.capture_btn.setEnabled(False)
        self.capture_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.capture_btn.clicked.connect(self.capture_sample)

        btn_layout.addWidget(self.start_enroll_btn)
        btn_layout.addWidget(self.capture_btn)
        enroll_layout.addLayout(btn_layout)

        self.status_label = QLabel("Ready to enroll")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont('Arial', 10))
        enroll_layout.addWidget(self.status_label)

        enroll_group.setLayout(enroll_layout)
        left_layout.addWidget(enroll_group)

        # Right - Enrolled people list
        right_layout = QVBoxLayout()

        list_group = QGroupBox("Enrolled People")
        list_layout = QVBoxLayout()

        self.enrolled_table = QTableWidget()
        self.enrolled_table.setColumnCount(2)
        self.enrolled_table.setHorizontalHeaderLabels(["Name", "Samples"])
        self.enrolled_table.setColumnWidth(0, 200)
        self.enrolled_table.setColumnWidth(1, 80)
        list_layout.addWidget(self.enrolled_table)

        delete_btn = QPushButton("Delete Selected")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        delete_btn.clicked.connect(self.delete_selected)
        list_layout.addWidget(delete_btn)

        list_group.setLayout(list_layout)
        right_layout.addWidget(list_group)

        layout.addLayout(left_layout, 2)
        layout.addLayout(right_layout, 1)
        self.setLayout(layout)

    def update_frame(self, frame):
        """Update video display"""
        self.current_frame = frame.copy()

        if not self.enrollment_active:
            # Just display the frame
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.video_label.setPixmap(pixmap)

    def update_video_with_faces(self, face_detected):
        """Update video with face detection overlay"""
        if self.current_frame is None:
            return

        frame = self.current_frame.copy()

        # Simple face detection visualization
        if face_detected:
            cv2.putText(
                frame, "Face detected - Ready to capture",
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
            )
        else:
            cv2.putText(
                frame, "Position your face in the frame",
                (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2
            )

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qt_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.video_label.setPixmap(pixmap)

    def start_enrollment(self):
        """Start enrollment process"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a name")
            return

        if self.parent_app and name in self.parent_app.enrollments:
            reply = QMessageBox.question(
                self, "Confirm",
                f"{name} is already enrolled. Re-enroll?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.No:
                return

        self.current_name = name
        self.captured_encodings = []
        self.enrollment_active = True
        self.start_enroll_btn.setEnabled(False)
        self.capture_btn.setEnabled(True)
        self.name_input.setEnabled(False)
        self.samples_spin.setEnabled(False)
        self.progress_bar.setMaximum(self.samples_spin.value())
        self.progress_bar.setValue(0)
        self.status_label.setText(f"Enrolling {name}... Press SPACE or button to capture")

        # Start enrollment thread
        if self.parent_app:
            self.parent_app.start_enrollment_thread(self.samples_spin.value())

    def capture_sample(self):
        """Capture a face sample"""
        if self.parent_app and self.parent_app.enrollment_thread:
            self.parent_app.enrollment_thread.capture_sample()

    def update_progress(self, current, total):
        """Update progress bar"""
        self.progress_bar.setValue(current)
        self.status_label.setText(
            f"Captured {current}/{total} samples. Press SPACE or button for next."
        )

    def enrollment_complete(self, encodings):
        """Handle enrollment completion"""
        if self.parent_app:
            self.parent_app.enrollments[self.current_name] = encodings
            self.parent_app.save_enrollments()

        self.enrollment_active = False
        self.start_enroll_btn.setEnabled(True)
        self.capture_btn.setEnabled(False)
        self.name_input.setEnabled(True)
        self.name_input.clear()
        self.samples_spin.setEnabled(True)
        self.status_label.setText(
            f"Enrollment complete for {self.current_name}!"
        )

        self.refresh_enrolled_list()

        QMessageBox.information(
            self, "Success",
            f"{self.current_name} enrolled successfully with {len(encodings)} samples"
        )

    def refresh_enrolled_list(self):
        """Refresh the list of enrolled people"""
        self.enrolled_table.setRowCount(0)

        if self.parent_app:
            for name, encodings in self.parent_app.enrollments.items():
                row_position = self.enrolled_table.rowCount()
                self.enrolled_table.insertRow(row_position)
                self.enrolled_table.setItem(
                    row_position, 0, QTableWidgetItem(name)
                )
                self.enrolled_table.setItem(
                    row_position, 1, QTableWidgetItem(str(len(encodings)))
                )

    def delete_selected(self):
        """Delete selected enrolled person"""
        selected_rows = self.enrolled_table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "Error", "Please select a person to delete")
            return

        row = selected_rows[0].row()
        name = self.enrolled_table.item(row, 0).text()

        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Delete {name} from enrollments?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes and self.parent_app:
            if name in self.parent_app.enrollments:
                del self.parent_app.enrollments[name]
                self.parent_app.save_enrollments()
                self.refresh_enrolled_list()
                QMessageBox.information(self, "Success", f"{name} deleted")

    def keyPressEvent(self, event):
        """Handle key press for SPACE to capture"""
        if event.key() == Qt.Key_Space and self.enrollment_active:
            self.capture_sample()


class RecordsTab(QWidget):
    """Tab for viewing and managing attendance records"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Filter controls
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout()

        filter_layout.addWidget(QLabel("From:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        filter_layout.addWidget(self.date_from)

        filter_layout.addWidget(QLabel("To:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        filter_layout.addWidget(self.date_to)

        filter_layout.addWidget(QLabel("Name:"))
        self.name_filter = QLineEdit()
        self.name_filter.setPlaceholderText("Filter by name...")
        filter_layout.addWidget(self.name_filter)

        apply_btn = QPushButton("Apply Filter")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        apply_btn.clicked.connect(self.apply_filter)
        filter_layout.addWidget(apply_btn)

        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)

        # Records table
        self.records_table = QTableWidget()
        self.records_table.setColumnCount(3)
        self.records_table.setHorizontalHeaderLabels(["Name", "Emotion", "Timestamp"])
        self.records_table.setColumnWidth(0, 200)
        self.records_table.setColumnWidth(1, 150)
        self.records_table.setColumnWidth(2, 200)
        layout.addWidget(self.records_table)

        # Statistics
        stats_layout = QHBoxLayout()
        self.stats_label = QLabel("Total Records: 0")
        self.stats_label.setFont(QFont('Arial', 12))
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.addStretch()

        csv_btn = QPushButton("Export to CSV")
        csv_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        csv_btn.clicked.connect(self.export_csv)
        export_layout.addWidget(csv_btn)

        excel_btn = QPushButton("Export to Excel")
        excel_btn.setStyleSheet("""
            QPushButton {
                background-color: #16a085;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
        """)
        excel_btn.clicked.connect(self.export_excel)
        export_layout.addWidget(excel_btn)

        layout.addLayout(export_layout)
        self.setLayout(layout)

    def load_records(self):
        """Load attendance records from CSV"""
        csv_path = 'attendance.csv'
        if not Path(csv_path).exists():
            self.records_table.setRowCount(0)
            self.stats_label.setText("Total Records: 0")
            return

        df = pd.read_csv(csv_path)
        self.display_dataframe(df)

    def apply_filter(self):
        """Apply filters to records"""
        csv_path = 'attendance.csv'
        if not Path(csv_path).exists():
            return

        df = pd.read_csv(csv_path)

        # Date filter
        date_from = self.date_from.date().toPyDate()
        date_to = self.date_to.date().toPyDate()

        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df = df[
            (df['Timestamp'].dt.date >= date_from) &
            (df['Timestamp'].dt.date <= date_to)
        ]

        # Name filter
        name_filter = self.name_filter.text().strip()
        if name_filter:
            df = df[df['Name'].str.contains(name_filter, case=False, na=False)]

        self.display_dataframe(df)

    def display_dataframe(self, df):
        """Display dataframe in table"""
        self.records_table.setRowCount(len(df))

        for row_idx, row in df.iterrows():
            self.records_table.setItem(
                row_idx, 0, QTableWidgetItem(str(row['Name']))
            )
            self.records_table.setItem(
                row_idx, 1, QTableWidgetItem(str(row['Emotion']))
            )
            self.records_table.setItem(
                row_idx, 2, QTableWidgetItem(str(row['Timestamp']))
            )

        self.stats_label.setText(f"Total Records: {len(df)}")

    def export_csv(self):
        """Export filtered records to CSV"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", "", "CSV Files (*.csv)"
        )

        if filename:
            try:
                rows = []
                for row_idx in range(self.records_table.rowCount()):
                    row_data = [
                        self.records_table.item(row_idx, col).text()
                        for col in range(3)
                    ]
                    rows.append(row_data)

                df = pd.DataFrame(rows, columns=["Name", "Emotion", "Timestamp"])
                df.to_csv(filename, index=False)

                QMessageBox.information(
                    self, "Success",
                    f"Exported {len(df)} records to {filename}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")

    def export_excel(self):
        """Export filtered records to Excel"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export to Excel", "", "Excel Files (*.xlsx)"
        )

        if filename:
            try:
                rows = []
                for row_idx in range(self.records_table.rowCount()):
                    row_data = [
                        self.records_table.item(row_idx, col).text()
                        for col in range(3)
                    ]
                    rows.append(row_data)

                df = pd.DataFrame(rows, columns=["Name", "Emotion", "Timestamp"])
                df.to_excel(filename, index=False)

                QMessageBox.information(
                    self, "Success",
                    f"Exported {len(df)} records to {filename}"
                )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {e}")


class DashboardTab(QWidget):
    """Tab for attendance analytics and visualizations"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_app = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Refresh button
        refresh_btn = QPushButton("Refresh Dashboard")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_dashboard)
        layout.addWidget(refresh_btn)

        # Charts container
        charts_layout = QHBoxLayout()

        # Daily attendance chart
        self.daily_figure = Figure(figsize=(5, 4))
        self.daily_canvas = FigureCanvas(self.daily_figure)
        charts_layout.addWidget(self.daily_canvas)

        # Emotion distribution chart
        self.emotion_figure = Figure(figsize=(5, 4))
        self.emotion_canvas = FigureCanvas(self.emotion_figure)
        charts_layout.addWidget(self.emotion_canvas)

        layout.addLayout(charts_layout)

        # Statistics
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout()

        self.total_records_label = QLabel("Total Records: 0")
        self.unique_people_label = QLabel("Unique People: 0")
        self.today_count_label = QLabel("Today's Attendance: 0")
        self.most_common_emotion_label = QLabel("Most Common Emotion: N/A")

        stats_layout.addWidget(self.total_records_label)
        stats_layout.addWidget(self.unique_people_label)
        stats_layout.addWidget(self.today_count_label)
        stats_layout.addWidget(self.most_common_emotion_label)

        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        self.setLayout(layout)

    def refresh_dashboard(self):
        """Refresh dashboard with latest data"""
        csv_path = 'attendance.csv'
        if not Path(csv_path).exists():
            return

        df = pd.read_csv(csv_path)
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])

        # Update statistics
        self.total_records_label.setText(f"Total Records: {len(df)}")
        self.unique_people_label.setText(f"Unique People: {df['Name'].nunique()}")

        today = datetime.now().date()
        today_df = df[df['Timestamp'].dt.date == today]
        self.today_count_label.setText(f"Today's Attendance: {len(today_df)}")

        if not df.empty:
            most_common = df['Emotion'].mode()[0]
            self.most_common_emotion_label.setText(
                f"Most Common Emotion: {most_common}"
            )

        # Daily attendance chart
        self.daily_figure.clear()
        ax1 = self.daily_figure.add_subplot(111)

        df['Date'] = df['Timestamp'].dt.date
        daily_counts = df.groupby('Date').size()

        ax1.plot(daily_counts.index, daily_counts.values, marker='o', linewidth=2)
        ax1.set_title('Daily Attendance Trend')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Count')
        ax1.grid(True, alpha=0.3)
        self.daily_figure.autofmt_xdate()
        self.daily_canvas.draw()

        # Emotion distribution chart
        self.emotion_figure.clear()
        ax2 = self.emotion_figure.add_subplot(111)

        emotion_counts = df['Emotion'].value_counts()
        colors = plt.cm.Paired(range(len(emotion_counts)))

        ax2.pie(
            emotion_counts.values,
            labels=emotion_counts.index,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        ax2.set_title('Emotion Distribution')
        self.emotion_canvas.draw()


class AttendanceApp(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Face Recognition Attendance System")
        self.setGeometry(100, 100, 1200, 800)

        # Load enrollments
        self.enrollments = self.load_enrollments()

        # Initialize threads
        self.camera_thread = None
        self.face_recognition_thread = None
        self.emotion_thread = None
        self.enrollment_thread = None

        self.init_ui()
        self.start_threads()

    def init_ui(self):
        """Initialize UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Title
        title = QLabel("Face Recognition Attendance System")
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(title)

        # Tab widget
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #bdc3c7;
            }
            QTabBar::tab {
                background: #ecf0f1;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
        """)

        self.live_tab = LiveRecognitionTab(self)
        self.enrollment_tab = EnrollmentTab(self)
        self.records_tab = RecordsTab(self)
        self.dashboard_tab = DashboardTab(self)

        self.tabs.addTab(self.live_tab, "Live Recognition")
        self.tabs.addTab(self.enrollment_tab, "Enrollment")
        self.tabs.addTab(self.records_tab, "Records")
        self.tabs.addTab(self.dashboard_tab, "Dashboard")

        layout.addWidget(self.tabs)
        central_widget.setLayout(layout)

        # Initial updates
        self.live_tab.update_status(len(self.enrollments))
        self.enrollment_tab.refresh_enrolled_list()
        self.records_tab.load_records()

    def start_threads(self):
        """Start background worker threads"""
        # Camera thread
        self.camera_thread = CameraThread(camera_index=0)
        self.camera_thread.frame_ready.connect(self.handle_frame)
        self.camera_thread.start()

        # Face recognition thread
        self.face_recognition_thread = FaceRecognitionThread()
        self.face_recognition_thread.set_enrollments(self.enrollments)
        self.face_recognition_thread.faces_detected.connect(
            self.live_tab.handle_face_detected
        )
        self.face_recognition_thread.start()

        # Emotion detection thread
        self.emotion_thread = EmotionDetectionThread()
        self.emotion_thread.emotion_detected.connect(
            self.live_tab.handle_emotion_detected
        )
        self.emotion_thread.start()

    def start_enrollment_thread(self, target_samples):
        """Start enrollment thread"""
        if self.enrollment_thread:
            self.enrollment_thread.stop()

        self.enrollment_thread = EnrollmentThread(target_samples)
        self.enrollment_thread.progress_update.connect(
            self.enrollment_tab.update_progress
        )
        self.enrollment_thread.face_detected.connect(
            self.enrollment_tab.update_video_with_faces
        )
        self.enrollment_thread.enrollment_complete.connect(
            self.enrollment_tab.enrollment_complete
        )
        self.enrollment_thread.start()

    @pyqtSlot(np.ndarray)
    def handle_frame(self, frame):
        """Handle new frame from camera"""
        # Update displays
        self.live_tab.update_frame(frame)
        self.enrollment_tab.update_frame(frame)

        # Send to recognition thread if active
        if self.live_tab.recognition_active:
            self.face_recognition_thread.set_frame(frame)

        # Send to enrollment thread if active
        if self.enrollment_tab.enrollment_active and self.enrollment_thread:
            self.enrollment_thread.set_frame(frame)

    def load_enrollments(self):
        """Load enrollments from file"""
        path = 'enrollments.pkl'
        if not Path(path).exists():
            return {}

        with open(path, 'rb') as f:
            return pickle.load(f)

    def save_enrollments(self):
        """Save enrollments to file"""
        path = 'enrollments.pkl'
        with open(path, 'wb') as f:
            pickle.dump(self.enrollments, f)

        # Update face recognition thread
        if self.face_recognition_thread:
            self.face_recognition_thread.set_enrollments(self.enrollments)

    def closeEvent(self, event):
        """Clean up on close"""
        if self.camera_thread:
            self.camera_thread.stop()

        if self.face_recognition_thread:
            self.face_recognition_thread.stop()

        if self.emotion_thread:
            self.emotion_thread.stop()

        if self.enrollment_thread:
            self.enrollment_thread.stop()

        event.accept()


def main():
    app = QApplication(sys.argv)
    window = AttendanceApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
