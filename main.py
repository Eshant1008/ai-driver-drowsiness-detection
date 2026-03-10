import winsound
import cv2
import mediapipe as mp
import threading
from utils import eye_aspect_ratio, play_alarm

# Initialize Mediapipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Eye landmark indices
LEFT_EYE = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]

# Thresholds
EAR_THRESHOLD = 0.22
FRAME_LIMIT = 15

sleep_counter = 0
alarm_on = False

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()         
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            h, w, _ = frame.shape
            mesh_points = []

            for lm in face_landmarks.landmark:
                mesh_points.append((int(lm.x*w), int(lm.y*h)))

            left_eye = [mesh_points[p] for p in LEFT_EYE]
            right_eye = [mesh_points[p] for p in RIGHT_EYE]

            leftEAR = eye_aspect_ratio(left_eye)
            rightEAR = eye_aspect_ratio(right_eye)

            ear = (leftEAR + rightEAR) / 2

            # Display EAR value
            cv2.putText(frame, f"EAR: {ear:.2f}", (450, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            if ear < EAR_THRESHOLD:
                sleep_counter += 1

                cv2.putText(frame, "DROWSINESS DETECTED!", (50,100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 3)

                if sleep_counter >= FRAME_LIMIT:
                    if not alarm_on:
                        alarm_on = True
                        threading.Thread(target=play_alarm, daemon=True).start()

            else:
                sleep_counter = 0
                if alarm_on:
                    winsound.PlaySound(None, winsound.SND_PURGE)  # STOP SOUND
                alarm_on = False

    cv2.imshow("Driver Drowsiness Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
