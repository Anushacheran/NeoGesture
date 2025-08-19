import cv2
import mediapipe as mp
from gtts import gTTS
from playsound import playsound
import subprocess
import os
import psutil
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# =========================
# Setup
# =========================
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Voice memory
last_spoken = ""
last_gesture = None
gesture_counter = 0  # To require consistency for gesture execution
GESTURE_THRESHOLD = 3  # Number of consecutive frames for stable detection

# =========================
# Voice function
# =========================
def speak(text):
    global last_spoken
    if text != last_spoken:
        tts = gTTS(text=text, lang='en')
        tts.save("temp.mp3")
        playsound("temp.mp3")
        os.remove("temp.mp3")
        last_spoken = text

# =========================
# Open/Close functions
# =========================
def open_notepad(): subprocess.Popen(["notepad.exe"])
def close_notepad():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == 'notepad.exe':
            proc.terminate()
def open_calculator(): subprocess.Popen(["calc.exe"])
def close_calculator():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() in ['calculator.exe', 'applicationframehost.exe']:
            proc.terminate()
def open_chrome(): subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
def close_chrome():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == 'chrome.exe':
            proc.terminate()

# =========================
# Gesture detection function
# =========================
def run_gesture_detection(frame, hands_detector):
    """
    Detects hand gestures and executes actions.
    Returns updated frame, detected gesture, action text, and finger count.
    """
    global last_gesture, gesture_counter
    action_text = "No Action"
    gesture = None
    finger_count = 0

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands_detector.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            fingers = []
            tip_ids = [4, 8, 12, 16, 20]

            # Thumb
            if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0]-1].x:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other fingers
            for id in range(1, 5):
                if hand_landmarks.landmark[tip_ids[id]].y < hand_landmarks.landmark[tip_ids[id]-2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)

            finger_count = sum(fingers)

            # Map gestures
            if finger_count == 1:
                gesture = "open_notepad"
                action_text = "Opening Notepad"
            elif finger_count == 2:
                gesture = "open_calculator"
                action_text = "Opening Calculator"
            elif finger_count == 3:
                gesture = "open_chrome"
                action_text = "Opening Chrome"
            elif finger_count == 4:
                gesture = "close_notepad"
                action_text = "Closing Notepad"
            elif finger_count == 5:
                gesture = "close_calculator"
                action_text = "Closing Calculator"
            elif finger_count == 0:
                gesture = "close_chrome"
                action_text = "Closing Chrome"

            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Gesture smoothing: only trigger after consistent detection
    if gesture == last_gesture:
        gesture_counter += 1
    else:
        gesture_counter = 0
    if gesture_counter >= GESTURE_THRESHOLD and gesture != None:
        # Execute gesture
        if gesture == "open_notepad": open_notepad()
        elif gesture == "close_notepad": close_notepad()
        elif gesture == "open_calculator": open_calculator()
        elif gesture == "close_calculator": close_calculator()
        elif gesture == "open_chrome": open_chrome()
        elif gesture == "close_chrome": close_chrome()
        speak(action_text)
        gesture_counter = 0  # reset after execution
        last_gesture = gesture

    # Update last_gesture if no action for smoothing
    if gesture != None and gesture != last_gesture:
        last_gesture = gesture

    return frame, gesture, action_text, finger_count
