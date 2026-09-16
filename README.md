👁️ FocusSense

Smart Study Monitoring & Drowsiness Detection System

FocusSense is a smart study monitoring system designed to help students maintain focus during study sessions. It uses computer vision and eye-rate analysis to monitor the user's eye activity in real time, identify signs of drowsiness, and provide audio alerts when the user appears to be losing focus.

📌 Overview

Staying focused during long study sessions can be challenging, especially when fatigue and drowsiness begin to affect concentration.

FocusSense addresses this problem by using a laptop camera to continuously observe the user's face and eyes while studying. The system analyzes eye activity and determines whether the user is actively studying or showing signs of sleepiness.

When prolonged eye closure or drowsiness is detected, FocusSense plays an audio alert to bring the user's attention back to their studies.

✨ Features

👁️ Real-Time Eye Monitoring
Monitors eye activity through the webcam.

📊 Eye-Rate Analysis
Uses eye-related measurements to determine the user's attention state.

😴 Drowsiness Detection
Detects prolonged eye closure and signs of sleepiness.

🔊 Audio Alerts
Plays an alert when the system detects that the user may be falling asleep.

🎥 Webcam-Based Monitoring
Works with a standard laptop or external webcam.

⚡ Real-Time Processing
Processes camera input continuously during a study session.

🎓 Student-Focused
Designed specifically to support students during self-study and long learning sessions.

🧠 How It Works

FocusSense follows a real-time monitoring pipeline:

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

The user can regain attention and continue studying.

🔄 System Workflow

Start
  │
  ▼
Initialize Camera
  │
  ▼
Capture Video Frame
  │
  ▼
Detect Face
  │
  ▼
Detect / Track Eyes
  │
  ▼
Calculate Eye Activity
  │
  ├───────────────┐
  │               │
  ▼               ▼
Normal Activity   Prolonged Eye Closure
  │               │
  ▼               ▼
Continue          Drowsiness Detected
Monitoring        │
                  ▼
             Play Audio Alert
                  │
                  ▼
             Resume Monitoring

🛠️ Technologies Used

Technology

Purpose

Python

Core programming language

OpenCV

Computer vision and webcam processing

NumPy

Numerical calculations and data processing

Computer Vision

Face and eye monitoring

Webcam

Real-time video input

Audio Processing

Drowsiness alert system


⚙️ Installation & Setup

1. Clone the Repository

git clone https://github.com/YOUR-USERNAME/FocusSense.git

2. Navigate to the Project

cd FocusSense

3. Create a Virtual Environment

python -m venv .venv

4. Activate the Virtual Environment

Windows

.venv\Scripts\activate

Linux / macOS

source .venv/bin/activate

5. Install Dependencies

pip install -r requirements.txt

▶️ How to Run

After installing the dependencies, start FocusSense with:

python smart_study_monitor.py

Make sure that:

Your webcam is connected.

Camera permissions are enabled.

Your environment has all required Python packages installed.

The required audio assets are available in the expected location.

🔊 Audio Alert System

FocusSense provides an audio warning when prolonged eye closure or drowsiness is detected.

The alert system is designed to:

Grab the user's attention.

Reduce extended periods of sleepiness.

Encourage the student to return their focus to studying.

Provide immediate feedback during a study session.

🎯 Objective

The main objective of FocusSense is to create a simple and practical tool that helps students maintain concentration during study sessions.

The project focuses on:

Monitoring study behavior.

Detecting signs of drowsiness.

Providing timely feedback.

Encouraging productive study habits.

Demonstrating a practical application of computer vision.

💡 Why FocusSense?

Long study sessions can lead to fatigue, reduced attention, and unintentional sleep.

Traditional study timers can tell a student how long they have been studying, but they cannot determine whether the student is actually maintaining attention.

FocusSense introduces a real-time monitoring approach by observing eye activity and providing an alert when signs of drowsiness are detected.

📊 Possible Study States

FocusSense can conceptually identify two primary states:

🟢 Focused / Active

The user's eyes show normal activity and the system continues monitoring without triggering an alert.

🔴 Drowsy / Sleeping

The system detects prolonged eye closure or reduced eye activity and triggers an audio warning.

Detection accuracy can vary depending on lighting, camera quality, face position, glasses, and other environmental conditions.

🔐 Privacy

FocusSense is designed around webcam-based local monitoring.

The camera is used to analyze the user's study session, and the project does not require uploading camera footage to an external server.

For privacy and security:

Camera data should be handled locally.

Do not upload personal recordings to public repositories.

Keep private configuration files out of Git.

Review .gitignore before pushing the project to GitHub.

📸 Screenshots

Add screenshots of the application here.

For example:

![FocusSense Monitoring](assets/screenshot.png)

Recommended screenshots:

📷 Webcam monitoring screen

👁️ Face and eye detection

🟢 Focused state

😴 Drowsiness detection

🔊 Audio alert state

🎥 Demo

You can add a demonstration video or GIF of FocusSense working in real time.

Example:

![FocusSense Demo](assets/demo.gif)

You can also add a YouTube or project demonstration link here:

Demo: YOUR-DEMO-LINK

🎓 Learning Outcomes

Developing FocusSense provides practical experience with:

Python programming

Computer vision fundamentals

Real-time webcam processing

Face detection

Eye detection

Image processing

Eye activity analysis

Audio alert integration

Working with external Python libraries

Real-time application development

Debugging and project organization

Git and GitHub workflow

🚀 Future Improvements

Future versions of FocusSense could include:

📈 Study Analytics

Store and visualize study-session information such as:

Total study time

Focused time

Drowsiness events

Number of alerts

Daily productivity

⏱️ Automatic Session Tracking

Automatically start and stop study sessions and calculate useful statistics.

📊 Productivity Dashboard

Add charts and graphs to help students understand their study patterns.

💤 Improved Drowsiness Detection

Improve detection reliability under different:

Lighting conditions

Camera angles

Face positions

User environments

🔔 Customizable Alerts

Allow users to select:

Alert sounds

Alert volume

Alert sensitivity

Alert duration

🖥️ Graphical User Interface

Create a dedicated interface displaying:

Camera feed

Current status

Study timer

Focus statistics

Alert history

🌙 Low-Light Support

Improve monitoring performance when the user is studying in low-light conditions.

📅 Daily & Weekly Reports

Generate reports showing study patterns and focus trends.

☁️ Study History

Optionally store study statistics for long-term progress tracking.

⚠️ Limitations

FocusSense is a monitoring and educational project, so its results may not always be accurate.

Performance can be affected by:

Poor lighting

Low-quality cameras

Face partially outside the camera frame

Large changes in head position

Glasses or reflections

Multiple people appearing in the frame

Camera permission issues

The system should be treated as a productivity aid rather than a medical or diagnostic tool.

🧪 Testing

Before using the system for a study session, verify that:

The webcam is detected correctly.

Your face is visible to the camera.

Eye detection works under the available lighting.

Audio alerts can be played.

Required dependencies are installed.

The application can run continuously without errors.

🧰 Troubleshooting

Camera is not opening

Check whether:

Another application is using the webcam.

Camera permissions are enabled.

The correct camera index is being used.

Your webcam is properly connected.

Audio alert is not playing

Check whether:

The audio file exists.

The file path is correct.

Your system volume is enabled.

The required audio library is installed.

Eye detection is inaccurate

Try:

Improving room lighting.

Sitting directly in front of the camera.

Keeping your face within the camera frame.

Cleaning the camera lens.

Avoiding strong reflections on glasses.

📌 Project Goals

The project was developed with the following goals:

✓ Monitor study sessions
✓ Detect eye activity
✓ Identify signs of drowsiness
✓ Provide real-time audio feedback
✓ Encourage better study habits
✓ Explore practical computer vision applications

🌟 Project Vision

FocusSense aims to make study sessions more interactive by providing real-time awareness of attention and drowsiness.

Instead of simply measuring how long a student sits at their desk, the system focuses on how actively they are engaging with their study session.

The long-term vision is to develop FocusSense into a complete personal productivity assistant for students, combining real-time monitoring with meaningful study analytics and progress tracking.

🤝 Contributing

Contributions are welcome!

If you would like to improve FocusSense:

Fork the repository.

Create a new branch.

git checkout -b feature/your-feature

Make your changes.

Commit your changes.

git add .
git commit -m "Add your feature"

Push the branch.

git push origin feature/your-feature

Open a Pull Request.

⭐ Support

If you find FocusSense useful or interesting, consider giving the repository a ⭐ on GitHub.

Your support helps motivate further development and improvements.

👨‍💻 Author

Vipin Soni

B.Tech Computer Science & Engineering — Artificial Intelligence & Machine Learning

Interested in:

Computer Vision

Machine Learning

Artificial Intelligence

Software Development

Full-Stack Development

📄 License

This project is created for educational and learning purposes.

You are welcome to explore, modify, and improve the project while following the applicable licensing requirements of the repository.

🔗 Project

FocusSense — Smart Study Monitoring & Drowsiness Detection System

Stay focused. Stay consistent. Keep learning. 🚀
