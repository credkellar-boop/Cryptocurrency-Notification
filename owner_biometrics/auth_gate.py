
import face_recognition
import cv2
import numpy as np

def verify_identity():
    # Face I.D. Logic
    video_capture = cv2.VideoCapture(0)
    # Load authorized face encoding from local storage
    authorized_image = face_recognition.load_image_file("owner_biometrics/face_id.jpg")
    authorized_encoding = face_recognition.face_encodings(authorized_image)[0]

    print("Initiating Face I.D. scan...")
    # Capture frame and compare
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]
    face_encodings = face_recognition.face_encodings(rgb_frame)

    for face_encoding in face_encodings:
        match = face_recognition.compare_faces([authorized_encoding], face_encoding)
        if match[0]:
            print("Access Granted: Face Recognized.")
            video_capture.release()
            return True
    
    print("Access Denied.")
    video_capture.release()
    return False
