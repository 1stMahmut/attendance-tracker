import cv2, pickle, pandas as pd
from pathlib import Path
from datetime import datetime
import face_recognition
from deepface import DeepFace
import tkinter as tk
from tkinter import ttk, messagebox


def enroll_person(name, n_samples=5):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): print("Error: Could not open camera"); return []
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    encodings = []
    print(f"Capturing {n_samples} samples for {name}. Press SPACE to capture, ESC to quit.")
    
    while len(encodings) < n_samples:
        ret, frame = cap.read()
        if not ret: break
        cv2.imshow('Enrollment', frame)
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:
            face_locs = face_recognition.face_locations(frame)
            if len(face_locs) == 1:
                enc = face_recognition.face_encodings(frame, face_locs)[0]
                encodings.append(enc)
                print(f"Captured {len(encodings)}/{n_samples}")
            else: print(f"Found {len(face_locs)} faces, need exactly 1")
        elif key == 27: break
    
    cap.release()
    cv2.destroyAllWindows()
    return encodings

def save_enrollments(enrollments, path='enrollments.pkl'):
    with open(path, 'wb') as f: pickle.dump(enrollments, f)
    print(f"Saved {len(enrollments)} enrollments to {path}")

def load_enrollments(path='enrollments.pkl'):
    if not Path(path).exists(): return {}
    with open(path, 'rb') as f: return pickle.load(f)

def recognize_faces(enrollments, tolerance=0.6):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): print("Error: Could not open camera"); return
    known_names = list(enrollments.keys())
    known_encodings = [sum(enrollments[n])/len(enrollments[n]) for n in known_names]
    logged = set()
    face_timers = {}


    
    while True:
        ret, frame = cap.read()
        if not ret: break
        face_locs = face_recognition.face_locations(frame)
        face_encs = face_recognition.face_encodings(frame, face_locs)
        current_time = datetime.now()
        
        for (top,right,bottom,left), face_enc in zip(face_locs, face_encs):
            matches = face_recognition.compare_faces(known_encodings, face_enc, tolerance)
            name = "Unknown"
            if True in matches: name = known_names[matches.index(True)]
            
            if name not in face_timers: face_timers[name] = current_time
            elapsed = (current_time - face_timers[name]).total_seconds()
            
            emotion = "waiting..." if elapsed < 3 else detect_emotion(frame, (top,right,bottom,left))
            if name != "Unknown" and name not in logged and elapsed >= 3: log_attendance(name, emotion); logged.add(name)
            cv2.rectangle(frame, (left,top), (right,bottom), (0,255,0), 2)
            cv2.putText(frame, f"{name} - {emotion}", (left,top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        
        cv2.imshow('Recognition', frame)
        if cv2.waitKey(1) & 0xFF == 27: break
    
    cap.release()
    cv2.destroyAllWindows()


def detect_emotion(frame, face_loc):
    top,right,bottom,left = face_loc
    face_img = frame[top:bottom, left:right]
    try:
        result = DeepFace.analyze(face_img, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion'] if isinstance(result, list) else result['dominant_emotion']
        return emotion
    except: return "unknown"
    
def log_attendance(name, emotion, csv_path='attendance.csv'):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {'Name': [name], 'Emotion': [emotion], 'Timestamp': [timestamp]}
    df = pd.DataFrame(data)
    if Path(csv_path).exists(): df.to_csv(csv_path, mode='a', header=False, index=False)
    else: df.to_csv(csv_path, index=False)
    print(f"Logged: {name} - {emotion} at {timestamp}")

def view_attendance(csv_path='attendance.csv'):
    if not Path(csv_path).exists(): print("No attendance records found"); return
    df = pd.read_csv(csv_path)
    print("\n=== Attendance Records ===")
    print(df.to_string(index=False))
    print(f"\nTotal records: {len(df)}")

class AttendanceUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Face Attendance System")
        self.root.geometry("900x700")
        self.enrollments = load_enrollments()
        self.cap = cv2.VideoCapture(0)
        self.mode = 'preview'
        self.enroll_name = None
        self.enroll_samples = []
        self.enroll_target = 3
        self.face_timers = {}
        self.logged = set()

        
        top_frame = ttk.Frame(self.root)
        top_frame.pack(pady=10)
        self.status_label = ttk.Label(top_frame, text=f"Mode: Preview | Enrolled: {len(self.enrollments)} people", font=('Arial', 12))
        self.status_label.pack()
        
        self.canvas = tk.Canvas(self.root, width=640, height=480, bg='black')
        self.canvas.pack(pady=10)
        
        self.message_label = ttk.Label(self.root, text="", font=('Arial', 10), foreground='blue')
        self.message_label.pack()
        
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Enroll Person", command=self.enroll_mode).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Start Recognition", command=self.recognize_mode).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Attendance", command=self.view).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Exit", command=self.exit).pack(side=tk.LEFT, padx=5)
        
        self.show_frame()
    
    def update_status(self): self.status_label.config(text=f"Mode: {self.mode.title()} | Enrolled: {len(self.enrollments)} people")
    
    def show_message(self, msg): self.message_label.config(text=msg); self.root.after(3000, lambda: self.message_label.config(text=""))
    
    def enroll_mode(self):
        self.enroll_name = tk.simpledialog.askstring("Enroll", "Enter person's name:")
        if self.enroll_name: self.mode = 'enroll'; self.enroll_samples = []; self.update_status(); self.show_message(f"Enrolling {self.enroll_name}. Press SPACE to capture ({len(self.enroll_samples)}/{self.enroll_target})")

    
    def recognize_mode(self): self.mode = 'recognize'; self.face_timers = {}; self.logged = set(); self.update_status(); self.show_message("Recognition started")

    
    def view(self): view_attendance()
    
    def exit(self): self.cap.release(); self.root.quit()

    def show_frame(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                if self.mode == 'enroll' and self.enroll_name:
                    face_locs = face_recognition.face_locations(frame)
                    if len(face_locs) == 1:
                        top,right,bottom,left = face_locs[0]
                        cv2.rectangle(frame, (left,top), (right,bottom), (0,255,0), 2)
                        cv2.putText(frame, f"Samples: {len(self.enroll_samples)}/{self.enroll_target}", (left,top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                    elif len(face_locs) > 1: cv2.putText(frame, "Multiple faces detected!", (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                elif self.mode == 'recognize':
                    face_locs = face_recognition.face_locations(frame)
                    face_encs = face_recognition.face_encodings(frame, face_locs)
                    known_names = list(self.enrollments.keys())
                    known_encodings = [sum(self.enrollments[n])/len(self.enrollments[n]) for n in known_names]
                    current_time = datetime.now()
                    
                    for (top,right,bottom,left), face_enc in zip(face_locs, face_encs):
                        matches = face_recognition.compare_faces(known_encodings, face_enc, 0.6)
                        name = known_names[matches.index(True)] if True in matches else "Unknown"
                        
                        if name not in self.face_timers: self.face_timers[name] = current_time
                        elapsed = (current_time - self.face_timers[name]).total_seconds()
                        
                        if elapsed < 3: text = f"{name} - {int(3-elapsed)}s"
                        else:
                            emotion = detect_emotion(frame, (top,right,bottom,left))
                            text = f"{name} - {emotion}"
                            if name != "Unknown" and name not in self.logged: log_attendance(name, emotion); self.logged.add(name); self.show_message(f"Logged: {name} - {emotion}")
                        
                        cv2.rectangle(frame, (left,top), (right,bottom), (0,255,0), 2)
                        cv2.putText(frame, text, (left,top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (640, 480))
                from PIL import Image, ImageTk
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
                self.canvas.imgtk = img
            self.root.after(10, self.show_frame)
    
    def run(self): self.root.mainloop()




if __name__ == '__main__':
    from tkinter import simpledialog
    ui = AttendanceUI()
    ui.run()
