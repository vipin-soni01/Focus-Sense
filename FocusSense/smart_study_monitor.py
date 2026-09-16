"""
SMART STUDY MONITOR
=====================================================================
A webcam-based study monitor that watches for two independent states:

  1. DROWSY      -> eyes closed for too long (Eye Aspect Ratio / EAR)
  2. DISTRACTED  -> head turned/tilted away from the screen for too long
                     (head-pose yaw/pitch from MediaPipe's face transform)

Each state has its own audio alert, cooldown, and "hold" period so
status doesn't flicker on brief blinks or quick head movements.

--------------------------------------------------------------------
FOLDER STRUCTURE (all files must sit in the same folder):

    smart_study_monitor.py     <- this script
    face_landmarker.task       <- auto-downloaded on first run
    uth_jaa.wav                <- drowsy alert sound
    focus_alert.wav            <- distraction alert sound

--------------------------------------------------------------------
CONTROLS:
    q  ->  quit and show a session summary in the terminal
=====================================================================
"""

import os
import math
import time
import urllib.request

import cv2
import numpy as np
import mediapipe as mp
import winsound
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision


# Folder this script lives in -- model and sound files are expected here
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


# =====================================================================
# CONFIG -- tune these values to fit your face, camera, and preferences
# =====================================================================

# --- Files ---
MODEL_PATH = os.path.join(BASE_PATH, "face_landmarker.task")
MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/"
    "face_landmarker/float16/1/face_landmarker.task"
)
DROWSY_SOUND_PATH = os.path.join(BASE_PATH, "get_up.wav")
FOCUS_SOUND_PATH = os.path.join(BASE_PATH, "stay_focused.wav")

# --- Drowsiness detection (EAR) ---
EAR_THRESHOLD = 0.21            # below this = eyes considered "closed"
DROWSY_CONSEC_FRAMES = 20       # consecutive low-EAR frames to confirm drowsiness
DROWSY_HOLD_SECONDS = 2.5       # how long "DROWSY" stays on screen after eyes reopen
DROWSY_ALERT_COOLDOWN = 4.0     # min seconds between repeated drowsy alerts

# --- Distraction detection (head pose) ---
YAW_THRESHOLD = 25              # degrees of left/right turn allowed
PITCH_THRESHOLD = 20            # degrees of up/down tilt allowed
DISTRACTED_CONSEC_FRAMES = 25   # consecutive off-angle frames to confirm distraction
DISTRACTED_HOLD_SECONDS = 2.5   # how long "DISTRACTED" stays on screen
FOCUS_ALERT_COOLDOWN = 4.0      # min seconds between repeated distraction alerts

# --- MediaPipe Face Mesh landmark indices for each eye (p1..p6 around the eye) ---
LEFT_EYE = [362, 385, 387, 263, 373, 380]
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

WINDOW_NAME = "Smart Study Monitor"


# =====================================================================
# SETUP HELPERS
# =====================================================================

def ensure_model_downloaded():
    """Downloads the MediaPipe face landmark model if not already present."""
    if os.path.exists(MODEL_PATH):
        return
    print("Model file not found locally. Downloading face_landmarker.task ...")
    try:
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
        print("Download complete.")
    except Exception as e:
        print(f"FAILED to download model: {e}")
        print(f"Check your internet connection, or download manually from:\n{MODEL_URL}")
        input("Press Enter to exit...")
        exit()


def create_landmarker():
    """Creates and returns a configured MediaPipe FaceLandmarker (VIDEO mode)."""
    options = mp_vision.FaceLandmarkerOptions(
        base_options=mp_python.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=mp_vision.RunningMode.VIDEO,
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        output_facial_transformation_matrixes=True,  # needed for head pose
    )
    return mp_vision.FaceLandmarker.create_from_options(options)


def check_sound_files():
    """Checks which alert sound files exist and warns if missing."""
    drowsy_ok = os.path.exists(DROWSY_SOUND_PATH)
    focus_ok = os.path.exists(FOCUS_SOUND_PATH)
    if not drowsy_ok:
        print(f"WARNING: '{DROWSY_SOUND_PATH}' not found. Drowsy alert disabled.")
    if not focus_ok:
        print(f"WARNING: '{FOCUS_SOUND_PATH}' not found. Distraction alert disabled.")
    return drowsy_ok, focus_ok


def play_sound(path):
    """Plays a .wav file asynchronously (non-blocking) using the built-in winsound module."""
    winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC)


# =====================================================================
# DETECTION MATH
# =====================================================================

def euclidean(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def eye_aspect_ratio(landmarks, eye_indices, frame_w, frame_h):
    """Calculates EAR for one eye. Returns (ear_value, pixel_points)."""
    pts = [(landmarks[i].x * frame_w, landmarks[i].y * frame_h) for i in eye_indices]
    p1, p2, p3, p4, p5, p6 = pts
    vertical = euclidean(p2, p6) + euclidean(p3, p5)
    horizontal = euclidean(p1, p4)
    ear = vertical / (2.0 * horizontal)
    return ear, pts


def rotation_matrix_to_euler_angles(R):
    """Converts a 3x3 rotation matrix into yaw/pitch/roll in degrees."""
    sy = math.sqrt(R[0, 0] ** 2 + R[1, 0] ** 2)
    singular = sy < 1e-6

    if not singular:
        pitch = math.atan2(-R[2, 0], sy)
        yaw = math.atan2(R[1, 0], R[0, 0])
        roll = math.atan2(R[2, 1], R[2, 2])
    else:
        pitch = math.atan2(-R[2, 0], sy)
        yaw = 0
        roll = math.atan2(-R[1, 2], R[1, 1])

    return math.degrees(yaw), math.degrees(pitch), math.degrees(roll)


# =====================================================================
# STATE TRACKER -- holds all the "live" detection state across frames
# =====================================================================

class MonitorState:
    def __init__(self):
        # Drowsiness
        self.closed_frame_counter = 0
        self.last_drowsy_time = 0.0
        self.last_drowsy_alert_time = 0.0
        self.drowsy_alert_count = 0

        # Distraction
        self.distracted_frame_counter = 0
        self.last_distracted_time = 0.0
        self.last_focus_alert_time = 0.0
        self.distracted_alert_count = 0

        # Session
        self.session_start = time.time()

    def update_drowsiness(self, avg_ear, now, sound_available):
        if avg_ear < EAR_THRESHOLD:
            self.closed_frame_counter += 1
        else:
            self.closed_frame_counter = 0

        if self.closed_frame_counter >= DROWSY_CONSEC_FRAMES:
            self.last_drowsy_time = now
            if sound_available and (now - self.last_drowsy_alert_time) > DROWSY_ALERT_COOLDOWN:
                play_sound(DROWSY_SOUND_PATH)
                self.last_drowsy_alert_time = now
                self.drowsy_alert_count += 1

        is_drowsy = (now - self.last_drowsy_time) < DROWSY_HOLD_SECONDS
        return "DROWSY - Wake up!" if is_drowsy else "AWAKE", is_drowsy

    def update_distraction(self, yaw, pitch, now, sound_available):
        off_angle = abs(yaw) > YAW_THRESHOLD or abs(pitch) > PITCH_THRESHOLD

        if off_angle:
            self.distracted_frame_counter += 1
        else:
            self.distracted_frame_counter = 0

        if self.distracted_frame_counter >= DISTRACTED_CONSEC_FRAMES:
            self.last_distracted_time = now
            if sound_available and (now - self.last_focus_alert_time) > FOCUS_ALERT_COOLDOWN:
                play_sound(FOCUS_SOUND_PATH)
                self.last_focus_alert_time = now
                self.distracted_alert_count += 1

        is_distracted = (now - self.last_distracted_time) < DISTRACTED_HOLD_SECONDS
        return ("DISTRACTED - Focus on your book!" if is_distracted else "FOCUSED"), is_distracted

    def print_summary(self):
        duration_min = (time.time() - self.session_start) / 60.0
        print("\n" + "=" * 50)
        print("SESSION SUMMARY")
        print("=" * 50)
        print(f"Session duration:        {duration_min:.1f} minutes")
        print(f"Drowsiness alerts:       {self.drowsy_alert_count}")
        print(f"Distraction alerts:      {self.distracted_alert_count}")
        print("=" * 50)


# =====================================================================
# MAIN LOOP
# =====================================================================

def main():
    ensure_model_downloaded()
    landmarker = create_landmarker()
    drowsy_sound_available, focus_sound_available = check_sound_files()
    state = MonitorState()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not access the webcam.")
        input("Press Enter to exit...")
        return

    print("Webcam started. Press 'q' to quit.\n")
    frame_timestamp_ms = 0

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame from camera.")
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        frame_timestamp_ms += 33
        result = landmarker.detect_for_video(mp_image, frame_timestamp_ms)

        h, w, _ = frame.shape
        now = time.time()

        eye_text, eye_color = "No face detected", (0, 0, 255)
        focus_text, focus_color = "", (0, 255, 0)

        if result.face_landmarks:
            landmarks = result.face_landmarks[0]

            # ---- Drowsiness ----
            left_ear, left_pts = eye_aspect_ratio(landmarks, LEFT_EYE, w, h)
            right_ear, right_pts = eye_aspect_ratio(landmarks, RIGHT_EYE, w, h)
            avg_ear = (left_ear + right_ear) / 2.0

            for pt in left_pts + right_pts:
                cv2.circle(frame, (int(pt[0]), int(pt[1])), 2, (255, 255, 0), -1)

            eye_text, is_drowsy = state.update_drowsiness(avg_ear, now, drowsy_sound_available)
            eye_color = (0, 0, 255) if is_drowsy else (0, 255, 0)

            cv2.putText(frame, f"EAR: {avg_ear:.3f}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            # ---- Distraction ----
            if result.facial_transformation_matrixes:
                matrix = result.facial_transformation_matrixes[0]
                R = np.array(matrix)[:3, :3]
                yaw, pitch, _roll = rotation_matrix_to_euler_angles(R)

                focus_text, is_distracted = state.update_distraction(
                    yaw, pitch, now, focus_sound_available
                )
                focus_color = (0, 165, 255) if is_distracted else (0, 255, 0)

                cv2.putText(frame, f"Yaw: {yaw:.1f}  Pitch: {pitch:.1f}", (20, 110),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # ---- Draw status overlay ----
        cv2.putText(frame, eye_text, (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, eye_color, 2)
        if focus_text:
            cv2.putText(frame, focus_text, (20, 150),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, focus_color, 2)

        cv2.imshow(WINDOW_NAME, frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    state.print_summary()


if __name__ == "__main__":
    main()                    