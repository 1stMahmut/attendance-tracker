"""
Worker threads for background processing to keep UI responsive
"""
from PyQt5.QtCore import QThread, pyqtSignal
import cv2
import numpy as np
import face_recognition
from deepface import DeepFace
from datetime import datetime
import time


class CameraThread(QThread):
    """Thread for capturing video frames from camera"""
    frame_ready = pyqtSignal(np.ndarray)

    def __init__(self, camera_index=0):
        super().__init__()
        self.camera_index = camera_index
        self.running = False
        self.cap = None

    def run(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            print(f"Error: Could not open camera {self.camera_index}")
            return

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.running = True

        while self.running:
            ret, frame = self.cap.read()
            if ret:
                self.frame_ready.emit(frame)
            time.sleep(0.01)  # ~100 FPS max

    def stop(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.quit()
        self.wait()


class FaceRecognitionThread(QThread):
    """Thread for processing face recognition on frames"""
    faces_detected = pyqtSignal(list, list, list)  # locations, names, confidences

    def __init__(self):
        super().__init__()
        self.running = False
        self.frame = None
        self.known_encodings = []
        self.known_names = []
        self.tolerance = 0.6
        self.process_every_n_frames = 3  # Process every 3rd frame for performance
        self.frame_count = 0

    def set_enrollments(self, enrollments, tolerance=0.6):
        """Update known faces from enrollments dictionary"""
        self.known_names = list(enrollments.keys())
        # Average all encodings for each person
        self.known_encodings = [
            np.mean(enrollments[name], axis=0)
            for name in self.known_names
        ]
        self.tolerance = tolerance

    def set_frame(self, frame):
        """Update frame to process"""
        self.frame = frame

    def run(self):
        self.running = True

        while self.running:
            if self.frame is not None:
                self.frame_count += 1

                # Only process every Nth frame for performance
                if self.frame_count % self.process_every_n_frames == 0:
                    try:
                        # Detect faces in frame
                        face_locations = face_recognition.face_locations(self.frame)

                        if face_locations:
                            face_encodings = face_recognition.face_encodings(
                                self.frame, face_locations
                            )

                            names = []
                            confidences = []

                            for face_encoding in face_encodings:
                                if self.known_encodings:
                                    # Compare face to known faces
                                    distances = face_recognition.face_distance(
                                        self.known_encodings, face_encoding
                                    )

                                    min_distance = np.min(distances)

                                    if min_distance <= self.tolerance:
                                        best_match_index = np.argmin(distances)
                                        name = self.known_names[best_match_index]
                                        confidence = 1 - min_distance
                                    else:
                                        name = "Unknown"
                                        confidence = 0.0
                                else:
                                    name = "Unknown"
                                    confidence = 0.0

                                names.append(name)
                                confidences.append(confidence)

                            self.faces_detected.emit(face_locations, names, confidences)
                        else:
                            self.faces_detected.emit([], [], [])

                    except Exception as e:
                        print(f"Error in face recognition: {e}")

            time.sleep(0.03)  # ~30 Hz processing rate

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class EmotionDetectionThread(QThread):
    """Thread for detecting emotions in face regions"""
    emotion_detected = pyqtSignal(str, str)  # name, emotion

    def __init__(self):
        super().__init__()
        self.running = False
        self.tasks = []  # Queue of (frame, face_location, name) tuples

    def add_task(self, frame, face_location, name):
        """Add emotion detection task"""
        self.tasks.append((frame, face_location, name))

    def run(self):
        self.running = True

        while self.running:
            if self.tasks:
                frame, face_location, name = self.tasks.pop(0)

                try:
                    top, right, bottom, left = face_location
                    face_img = frame[top:bottom, left:right]

                    # Skip if face region is too small
                    if face_img.shape[0] < 48 or face_img.shape[1] < 48:
                        continue

                    result = DeepFace.analyze(
                        face_img,
                        actions=['emotion'],
                        enforce_detection=False,
                        silent=True
                    )

                    if isinstance(result, list):
                        emotion = result[0]['dominant_emotion']
                    else:
                        emotion = result['dominant_emotion']

                    self.emotion_detected.emit(name, emotion)

                except Exception as e:
                    print(f"Error detecting emotion: {e}")
                    self.emotion_detected.emit(name, "unknown")

            time.sleep(0.1)

    def stop(self):
        self.running = False
        self.tasks.clear()
        self.quit()
        self.wait()


class EnrollmentThread(QThread):
    """Thread for enrolling new faces"""
    progress_update = pyqtSignal(int, int)  # current, total
    face_detected = pyqtSignal(bool)  # True if exactly 1 face detected
    encoding_captured = pyqtSignal(np.ndarray)  # face encoding
    enrollment_complete = pyqtSignal(list)  # all encodings

    def __init__(self, target_samples=5):
        super().__init__()
        self.frame = None
        self.encodings = []
        self.target_samples = target_samples
        self.capture_flag = False

    def set_frame(self, frame):
        self.frame = frame

    def capture_sample(self):
        """Signal to capture a sample from current frame"""
        self.capture_flag = True

    def reset(self):
        """Reset for new enrollment"""
        self.encodings = []
        self.capture_flag = False

    def run(self):
        while len(self.encodings) < self.target_samples:
            if self.frame is not None:
                try:
                    face_locations = face_recognition.face_locations(self.frame)

                    # Emit whether exactly 1 face is detected
                    self.face_detected.emit(len(face_locations) == 1)

                    # If capture requested and exactly 1 face
                    if self.capture_flag and len(face_locations) == 1:
                        face_encodings = face_recognition.face_encodings(
                            self.frame, face_locations
                        )

                        if face_encodings:
                            encoding = face_encodings[0]
                            self.encodings.append(encoding)
                            self.encoding_captured.emit(encoding)
                            self.progress_update.emit(
                                len(self.encodings),
                                self.target_samples
                            )

                        self.capture_flag = False

                except Exception as e:
                    print(f"Error in enrollment: {e}")

            time.sleep(0.05)

        self.enrollment_complete.emit(self.encodings)
