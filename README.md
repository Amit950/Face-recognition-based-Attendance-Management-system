# Face Recognition Attendance System

This project implements a Face Recognition Based Attendance Management System using Python and OpenCV. The system captures images, recognizes faces, and records attendance in a user-friendly interface.

## Features

- Face detection and recognition using OpenCV and face_recognition library.
- Real-time attendance recording.
- Option to add students and capture images for training.
- Blink detection for enhanced security.

## Getting Started

To run this project on your machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Amit950/face-recognition-attendance.git
   cd face-recognition-attendance
##Install the required dependencies:
pip install -r requirements.txt

##Execute the main script:
python main.py


##Usage
Launch the application.
Add students by capturing images or uploading them.
Choose the "Go Live" option to start real-time face recognition.
Detected faces will be marked in the video feed.
Detected students' attendance will be recorded in the "Attendance records" directory.

##Dependencies
Python 3.7 or higher
OpenCV
face_recognition
numpy
tkinter
PIL (Python Imaging Library)

##Project Structure
The project is structured as follows

face-recognition-attendance/
├── main.py              # Main application script
├── blink_detection.py   # Blink detection module
├── Training_images/     # Directory for student images
├── Attendance records/  # Directory for attendance records
├── README.md            # Project documentation
└── requirements.txt     # List of required Python packages


##Contributions
Contributions are welcome! If you have any suggestions, bug fixes, or feature enhancements, feel free to create a pull request

#Contact
If you have any questions or need assistance, you can contact Amit at ak4898295@gmail.com
