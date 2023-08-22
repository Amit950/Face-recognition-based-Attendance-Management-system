import cv2
import dlib
from math import hypot

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
font = cv2.FONT_HERSHEY_COMPLEX_SMALL


def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)


def detect_blink(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        # cv2.rectangle(frame, (x, y), (x1, y1), (0, 0, 255), 2)
        landmarks = predictor(gray, face)

        # Horizontal distances
        left_part = (landmarks.part(36).x, landmarks.part(36).y)
        right_part = (landmarks.part(39).x, landmarks.part(39).y)

        center_top = midpoint(landmarks.part(37), landmarks.part(38))
        center_bottom = midpoint(landmarks.part(41), landmarks.part(40))

        hor_line = cv2.line(frame, left_part, right_part, (0, 255, 0), 1)
        ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 1)

        # Euclidean distance using hypot, math library
        hor_line_length = hypot(
            left_part[0] - right_part[0], left_part[1] - right_part[1])
        ver_line_length = hypot(
            center_top[0] - center_bottom[0], center_top[1] - center_bottom[1])
        ratio = hor_line_length / ver_line_length
        if ratio > 5.7:
            cv2.putText(frame, "Blinking", (350, 150), font, 2, (255, 0, 0), 2)

        # Right eye
        left_part1 = (landmarks.part(42).x, landmarks.part(42).y)
        right_part1 = (landmarks.part(45).x, landmarks.part(45).y)

        center_top1 = midpoint(landmarks.part(43), landmarks.part(44))
        center_bottom1 = midpoint(landmarks.part(47), landmarks.part(46))

        hor_line1 = cv2.line(frame, left_part1, right_part1, (0, 255, 0), 1)
        ver_line1 = cv2.line(frame, center_top1,
                             center_bottom1, (0, 255, 0), 1)

        for i in range(68):
            x = landmarks.part(i).x
            y = landmarks.part(i).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

            x = landmarks.part(37).x
            y = landmarks.part(37).y
            cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)

        # cv2.imshow("Video", frame)
        # key = cv2.waitKey(1)
        # if key == ord("q"):
        #     break

    return frame
