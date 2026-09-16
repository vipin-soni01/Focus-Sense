# 👁️ FocusSense

### Smart Study Monitoring & Drowsiness Detection System

FocusSense is a smart study monitoring system designed to help students maintain focus during study sessions. It uses your webcam and MediaPipe's face landmark tracking to watch two independent signs of lost focus in real time — **drowsy eyes** and **a distracted head pose** — and plays an audio alert when either is sustained for too long.

---

## 📌 Overview

Staying focused during long study sessions can be challenging, especially when fatigue and drowsiness begin to affect concentration.

**FocusSense** addresses this by using your webcam to continuously track facial landmarks while you study. It analyzes:

- How closed your eyes are (via **Eye Aspect Ratio**)
- Which way your head is turned or tilted (via **head-pose yaw/pitch**)

When either condition is sustained past a threshold, FocusSense plays a distinct audio alert to bring your attention back to your studies.

---

## ✨ Features

- 👁️ **Real-Time Eye Monitoring** — tracks eye landmarks through the webcam every frame.
- 📊 **Eye Aspect Ratio (EAR) Analysis** — a well-established geometric formula for detecting eye closure from landmark positions.
- 😴 **Drowsiness Detection** — flags sustained eye closure using a consecutive-frame counter, so a normal blink never triggers a false alert.
- 🙃 **Distraction Detection** — extracts yaw/pitch from MediaPipe's facial transformation matrix to detect when you've turned or tilted away from the screen.
- 🔊 **Independent Audio Alerts** — separate sounds and cooldowns for drowsiness vs. distraction, so alerts don't spam you.
- 🖥️ **Live On-Screen Overlay** — shows current status, EAR value, and yaw/pitch angles in real time.
- ⏳ **Hold Periods** — both states stay "active" briefly after the trigger clears, avoiding flicker.
- 📈 **Session Summary** — prints total duration and alert counts to the terminal when you quit.
- 🎓 **Student-Focused** — built specifically to support self-study and long learning sessions.

---

## 🧠 How It Works

```text
        ┌─────────────────┐
        │   Webcam Input  │
        └────────┬────────┘
                  │
                  ▼
        ┌─────────────────────────┐
        │ MediaPipe FaceLandmarker │
        │ (landmarks + transform)  │
        └────────┬─────────────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
┌───────────────┐   ┌─────────────────┐
│  Eye Landmarks │   │ Transformation  │
│  → EAR calc    │   │ Matrix → Yaw/   │
│                │   │ Pitch (Euler)   │
└───────┬────────┘   └────────┬────────┘
        │                     │
        ▼                     ▼
   EAR < threshold?      Yaw/Pitch >
   (N consec. frames)    threshold?
        │                     │
   ┌────┴────┐           ┌────┴────┐
   ▼         ▼           ▼         ▼
 Drowsy   Normal    Distracted  Focused
   │                     │
   ▼                     ▼
🔊 Drowsy Alert     🔊 Focus Alert
```

### Detection Process

1. The webcam captures a frame; MediaPipe's **FaceLandmarker** returns facial landmarks and a 3D transformation matrix.
2. **Drowsiness**: 6 landmark points per eye are used to compute the Eye Aspect Ratio (vertical eye distances over horizontal eye distance). A low EAR sustained over a configurable number of consecutive frames confirms drowsiness.
3. **Distraction**: The rotation component of the transformation matrix is converted into yaw/pitch (Euler angles). Sustained off-angle values confirm distraction.
4. If either condition is confirmed, its matching `.wav` alert plays — respecting a per-alert cooldown so it doesn't fire every frame.
5. The on-screen overlay updates live with status text, EAR, and yaw/pitch values.
6. On quit (`q`), a session summary prints: duration, drowsiness alerts, and distraction alerts.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **OpenCV** | Webcam capture, frame drawing, display window |
| **MediaPipe** | Face landmark detection & head-pose transformation matrix |
| **NumPy** | Rotation matrix → Euler angle math |
| **winsound** *(built-in, Windows)* | Asynchronous alert playback |

> ⚠️ **Windows only** — the current audio playback uses Python's built-in `winsound` module. See [Cross-Platform Note](#-cross-platform-note) to run on macOS/Linux.

---

## 📂 Project Structure

```text
FocusSense/
│
├── smart_study_monitor.py   # main script — run this
├── face_landmarker.task     # MediaPipe model (auto-downloaded on first run)
├── get_up.wav               # drowsiness alert sound
├── stay_focused.wav           # distraction alert sound
├── requirements.txt
└── .gitignore
```

All four core files (script, model, and both `.wav` files) must live in the **same folder** — the script resolves paths relative to its own location.

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/vipin-soni01/Study-Monitoring-.git
cd Study-Monitoring-
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

**Windows**
```bash
.venv\Scripts\activate
```

**Linux / macOS**
```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install opencv-python mediapipe numpy
```

Or, if using `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

```bash
python smart_study_monitor.py
```

Make sure that:

- Your webcam is connected and not in use by another app.
- Camera permissions are enabled for your terminal/IDE.
- `face_landmarker.task`, `uth_jaa.wav`, and `focus_alert.wav` are present next to the script (the model auto-downloads on first run if missing).

**Controls:** press `q` to quit and print a session summary.

---

## 🔊 Audio Alert System

FocusSense plays a distinct audio warning for each detected state:

- 😴 A **drowsiness alert** when eyes stay closed too long.
- 🙃 A **distraction alert** when your head turns or tilts away from the screen too long.

Each alert has its own cooldown to avoid spamming you while the condition persists.

---

## ⚙️ Configuration

Key thresholds live at the top of `smart_study_monitor.py` and can be tuned for your face, camera, and lighting:

```python
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
```

---

## 🎯 Objective

The main objective of FocusSense is to create a simple, practical tool that helps students maintain concentration during study sessions by:

- Monitoring eye and head activity in real time.
- Detecting signs of drowsiness and distraction independently.
- Providing timely audio feedback.
- Encouraging productive study habits.
- Demonstrating a practical, local-first computer vision application.

---

## 💡 Why FocusSense?

Traditional study timers can tell you **how long** you've been sitting at your desk — but not whether you're actually paying attention.

FocusSense introduces real-time monitoring of both **eye state** and **head orientation**, giving a more complete picture of engagement than a timer alone.

---

## 🔐 Privacy

FocusSense runs entirely **locally** — no camera footage or landmark data is uploaded anywhere.

For privacy and security:

- Camera data is processed locally, frame by frame, and never saved by default.
- Don't upload personal recordings to public repositories.
- Keep private configuration files out of Git.
- Review `.gitignore` before pushing the project to GitHub.

---



- 📷 Webcam monitoring screen
- 👁️ EAR overlay + eye landmarks
- 🟢 Focused state
- 😴 Drowsiness alert state
- 🙃 Distraction alert state

---


## 🎓 Learning Outcomes

Building FocusSense covers:

- Python programming
- Computer vision fundamentals (MediaPipe, OpenCV)
- Real-time webcam processing
- Facial landmark detection & geometric feature extraction (EAR)
- Rotation matrix → Euler angle conversion
- Audio alert integration
- Real-time application development
- Debugging and project organization
- Git and GitHub workflow

---

## 🚀 Future Improvements

- [ ] **Cross-platform audio** — replace `winsound` with `playsound` or `simpleaudio`
- [ ] **Configurable thresholds** via a config file or CLI args
- [ ] **Session logging** to CSV for tracking focus trends over time
- [ ] **Desktop notifications** as an alternative/addition to sound alerts
- [ ] **Productivity dashboard** with charts of focus/distraction over time
- [ ] **Customizable alerts** — sound, volume, sensitivity, duration
- [ ] **Graphical User Interface** showing camera feed, timer, and alert history
- [ ] **Low-light support** improvements
- [ ] **Daily & weekly reports**
- [ ] **Multi-face handling** / webcam selection

---

## ⚠️ Limitations

FocusSense is a monitoring and educational project — treat it as a productivity aid, not a medical or diagnostic tool. Performance can be affected by:

- Poor lighting
- Low-quality cameras
- Face partially outside the camera frame
- Large or rapid head movements
- Glasses or reflections
- Multiple people in frame
- Camera permission issues

---

## 🧪 Testing

Before a study session, verify that:

- The webcam is detected correctly.
- Your face is visible and well-lit.
- EAR and yaw/pitch values respond sensibly to blinking/turning.
- Both audio alerts play correctly.
- Required dependencies are installed.
- The application runs continuously without errors.

---

## 🧰 Troubleshooting

### Camera is not opening

- Check whether another app is using the webcam.
- Confirm camera permissions are enabled.
- Confirm the correct camera index is being used (`cv2.VideoCapture(0)` by default).

### Model download fails

- Check your internet connection.
- Manually download the model from the URL printed in the console and place it next to the script as `face_landmarker.task`.

### Audio alert is not playing

- Confirm `uth_jaa.wav` and `focus_alert.wav` exist next to the script (the console will warn if missing).
- Confirm your system volume is enabled.
- On non-Windows systems, swap `winsound` for a cross-platform library (see below).

### Eye/head detection is inaccurate

- Improve room lighting.
- Sit directly in front of the camera.
- Keep your face fully within frame.
- Adjust `EAR_THRESHOLD`, `YAW_THRESHOLD`, or `PITCH_THRESHOLD` in the config section.

---

## 🌍 Cross-Platform Note

Alert playback currently uses `winsound`, which is **Windows-only**. To run on macOS/Linux:

```bash
pip install playsound
```

```python
from playsound import playsound

def play_sound(path):
    playsound(path, block=False)
```

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch:
```bash
   git checkout -b feature/your-feature
```
3. Make your changes.
4. Commit your changes:
```bash
   git add .
   git commit -m "Add your feature"
```
5. Push the branch:
```bash
   git push origin feature/your-feature
```
6. Open a Pull Request.

---

## ⭐ Support

If you find **FocusSense** useful or interesting, consider giving the repository a ⭐ on GitHub — it helps motivate further development.

---

## 👨‍💻 Author

### Vipin Soni

**B.Tech Computer Science & Engineering — Artificial Intelligence & Machine Learning**

Interested in:

- Computer Vision
- Machine Learning
- Artificial Intelligence
- Software Development
- Full-Stack Development

---

## 📄 License

This project is created for **educational and learning purposes**. You are welcome to explore, modify, and improve it, following the applicable licensing terms of the repository.

---

## 🔗 Project

**FocusSense — Smart Study Monitoring & Drowsiness Detection System**

> Stay focused. Stay consistent. Keep learning. 🚀
