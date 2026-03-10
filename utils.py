from scipy.spatial import distance
import winsound
import os

# -------------------- Eye --------------------
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)


# -------------------- Mouth (optional) --------------------
def mouth_aspect_ratio(mouth):
    A = distance.euclidean(mouth[2], mouth[10])
    B = distance.euclidean(mouth[4], mouth[8])
    C = distance.euclidean(mouth[0], mouth[6])
    return (A + B) / (2.0 * C)


# -------------------- Alarm --------------------
alarm_path = os.path.join(os.path.dirname(__file__), "alarm.wav")

def play_alarm():
    winsound.PlaySound(alarm_path, winsound.SND_FILENAME | winsound.SND_ASYNC)