"""This file contains the main loop to run the prototype
"""

import cv2
from src.action import WordActionPicker, PowerPointActionPicker
from src.video import VideoCapturer
from src.voice import AudioTranscriber
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import pyautogui
import time

# Initialization of models
base_options = python.BaseOptions(model_asset_path=os.path.join(os.getcwd(),"models", "gesture_recognizer.task"))
options = vision.GestureRecognizerOptions(base_options=base_options)
gesture_recognizer = vision.GestureRecognizer.create_from_options(options)
audio_model_path = os.path.join(os.getcwd(), "models", "vosk-model-es-0.42")

if __name__ == "__main__":
    history = []
    # We initialize the camera and keep capturing image during the program execution
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Here lies all the business logic
        video_capturer = VideoCapturer(recognizer=gesture_recognizer, history=history)
        gesture = video_capturer.get_gesture(frame)
        if gesture == "Thumb_Down":
            # Open Pages
            ruta = "nui_test"
            #pyautogui.hotkey("command", "space")
            pyautogui.keyDown("command")
            pyautogui.keyDown("space")
            time.sleep(0.1)
            pyautogui.keyUp("command")
            pyautogui.keyUp("space")
            pyautogui.write("nuitest")
            time.sleep(3)
            pyautogui.press("enter")
            time.sleep(1)

        # Display the frame
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) != -1:
            break
    