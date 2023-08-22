import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter as tk
from tkinter import Label, Button, filedialog, Entry, StringVar
from PIL import Image, ImageTk
from blink_detection import detect_blink


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


def markAttendance(name, known_names, roll_number):
    day_suffix = "th" if 4 <= datetime.now().day <= 20 or 24 <= datetime.now(
    ).day <= 30 else {1: "st", 2: "nd", 3: "rd"}.get(datetime.now().day % 10, "th")
    formatted_date = datetime.now().strftime(f'%d{day_suffix} %B %Y')

    # Create the "Attendance records" directory if not exists
    records_dir = "Attendance records"
    os.makedirs(records_dir, exist_ok=True)

    filename = os.path.join(records_dir, f'{formatted_date}.csv')

    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write('Roll number,Name,Entry time,Date\n')

    if name not in known_names:
        with open(filename, 'a') as f:
            now = datetime.now()
            # Convert time to AM/PM format
            entry_time = now.strftime('%I:%M:%S %p')
            f.write(f'{roll_number},{name},{entry_time},{formatted_date}\n')
        known_names.add(name)


known_names = set()


def capture_image():
    if not entry_roll.get() or not entry_name.get():
        error_label.config(text="Please fill in all fields.")
        return

    _, img = cap.read()
    roll_number = entry_roll.get()
    name = entry_name.get()

    cv2.imwrite(f"{path}/{roll_number}_{name}.jpg", img)
    error_label.config(text="Image Captured and Saved.")
    entry_roll.set('')
    entry_name.set('')


def upload_image():
    if not entry_roll.get() or not entry_name.get():
        error_label.config(text="Please fill in all fields.")
        return

    file_path = filedialog.askopenfilename(title="Select Image",
                                           filetypes=(("Image files", "*.jpg;*.png"), ("All files", "*.*")))
    roll_number = entry_roll.get()
    name = entry_name.get()

    if file_path:
        img = Image.open(file_path)
        img = img.convert("RGB")
        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        cv2.imwrite(f"{path}/{roll_number}_{name}.jpg", img)
        error_label.config(text="Image Uploaded and Saved.")
        entry_roll.set('')
        entry_name.set('')


def update():
    _, img = cap.read()
    img = cv2.cvtColor(cv2.resize(img, (640, 480)), cv2.COLOR_BGR2RGB)

    # Call the detect_blink function to process the frame
    img_with_blink_overlays = detect_blink(img)

    img = Image.fromarray(img_with_blink_overlays)
    img = ImageTk.PhotoImage(img)

    video_label.img = img
    video_label.config(image=img)

    if is_live:
        process_live_feed()

    video_label.after(10, update)


def process_live_feed():
    _, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        landmarks = face_recognition.face_landmarks(imgS, [faceLoc])

        # Call the detect_blink function to process the frame
        imgS_with_blink = detect_blink(imgS)

        top, right, bottom, left = faceLoc
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(imgS_with_blink, (left, top),
                      (right, bottom), (0, 255, 0), 2)

        # Rest of your existing code for recognizing and displaying faces
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            full_name = classNames[matchIndex].upper()
            split_name = full_name.split('_')

            if len(split_name) > 1:
                # Reassign name as the string after the first split element
                name = "_".join(split_name[1:])
            else:
                name = full_name  # Keep the original full name if there is no "_" in the name

            roll_number = split_name[0]  # First element is the roll number

            markAttendance(name, known_names, roll_number)

            top, right, bottom, left = faceLoc
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(img, name, (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 2)

    img = cv2.resize(img, (640, 480))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)

    video_label.img = img
    video_label.config(image=img)


def toggle_live_capture():
    global is_live
    is_live = not is_live
    if is_live:
        live_button.config(text="Stop Live")
    else:
        live_button.config(text="Go Live")


def quit_program(event=None):
    cap.release()
    root.destroy()


root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("1366x768")

for i in range(5):
    root.grid_rowconfigure(i, weight=1)
    root.grid_columnconfigure(i, weight=1)

label_roll = Label(root, text="Roll Number:", font=("Helvetica", 20))
label_roll.grid(row=0, column=0, padx=10, pady=5)
entry_roll = StringVar()
entry_roll_field = Entry(root, textvariable=entry_roll, font=("Helvetica", 20))
entry_roll_field.grid(row=0, column=1, padx=10, pady=5)

label_name = Label(root, text="Name:", font=("Helvetica", 20))
label_name.grid(row=1, column=0, padx=10, pady=5)
entry_name = StringVar()
entry_name_field = Entry(root, textvariable=entry_name, font=("Helvetica", 20))
entry_name_field.grid(row=1, column=1, padx=10, pady=5)

student_button = Button(root, text="Add Student", font=(
    "Helvetica", 20), command=capture_image)
student_button.grid(row=2, column=0, padx=10, pady=5)

upload_button = Button(root, text="Upload Image", font=(
    "Helvetica", 20), command=upload_image)
upload_button.grid(row=2, column=1, padx=10, pady=5)

live_button = Button(root, text="Go Live", font=(
    "Helvetica", 20), command=toggle_live_capture)
live_button.grid(row=2, column=2, padx=10, pady=5)

quit_button = Button(root, text="Quit", font=(
    "Helvetica", 20), command=quit_program)
quit_button.grid(row=2, column=3, padx=10, pady=5)

error_label = Label(root, text="", fg="red", font=("Helvetica", 16))
error_label.grid(row=3, column=0, columnspan=4, padx=10, pady=5)

video_label = Label(root)
# Set column span to 5 to center-align the live camera preview
video_label.grid(row=4, column=0, columnspan=5, padx=10, pady=5)

# Initialize camera and known encodings
path = os.path.join(os.path.dirname(__file__), 'Training_images')
# Automatically create the folder if it doesn't exist
os.makedirs(path, exist_ok=True)
images = []
classNames = []

encodeListKnown = []

myList = os.listdir(path)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    if curImg is not None:
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

if images:
    encodeListKnown = findEncodings(images)
    print('Encoding Complete')
else:
    print('No images found in the "Training_images" folder.')

cap = cv2.VideoCapture(0)
is_live = False

update()

root.mainloop()
