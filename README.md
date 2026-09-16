# Focus-Sense
FocusSense helps students stay focused by monitoring eye activity in real time, detecting signs of drowsiness, and providing audio alerts when attention starts to drop.

# 👁️ FocusSense

### Smart Study Monitoring & Drowsiness Detection System

FocusSense is a smart study monitoring system designed to help students maintain focus during study sessions. It uses computer vision and eye-rate analysis to monitor the user's eye activity in real time, identify signs of drowsiness, and provide audio alerts when the user appears to be losing focus.

---

## 📌 Overview

Staying focused during long study sessions can be challenging, especially when fatigue and drowsiness begin to affect concentration.

**FocusSense** addresses this problem by using a laptop camera to continuously observe the user's face and eyes while studying. The system analyzes eye activity and determines whether the user is actively studying or showing signs of sleepiness.

When prolonged eye closure or drowsiness is detected, FocusSense plays an audio alert to bring the user's attention back to their studies.

---

## ✨ Features

- 👁️ **Real-Time Eye Monitoring**
  - Monitors eye activity through the webcam.

- 📊 **Eye-Rate Analysis**
  - Uses eye-related measurements to determine the user's attention state.

- 😴 **Drowsiness Detection**
  - Detects prolonged eye closure and signs of sleepiness.

- 🔊 **Audio Alerts**
  - Plays an alert when the system detects that the user may be falling asleep.

- 🎥 **Webcam-Based Monitoring**
  - Works with a standard laptop or external webcam.

- ⚡ **Real-Time Processing**
  - Processes camera input continuously during a study session.

- 🎓 **Student-Focused**
  - Designed specifically to support students during self-study and long learning sessions.

---

## 🧠 How It Works

The system follows a simple monitoring pipeline:

```text
        ┌─────────────────┐
        │   Webcam Input  │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Face Detection │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  Eye Detection  │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Eye-Rate / Eye  │
        │ Activity Analysis│
        └────────┬────────┘
                 │
          ┌──────┴──────┐
          │             │
          ▼             ▼
      Focused       Drowsy
          │             │
          │             ▼
          │       🔊 Audio Alert
          │
          ▼
      Continue Studying

Detection Process
The webcam captures the user's face.
The system identifies the eyes.
Eye activity is analyzed continuously.
The system checks for prolonged eye closure or reduced eye activity.
If drowsiness is detected, an audio alert is triggered.
The user can then regain attention and continue studying.
