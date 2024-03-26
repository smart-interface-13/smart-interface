"""This file contains the main loop to run the prototype
"""

import cv2
from src.action import WordActionPicker, PowerPointActionPicker
from src.video import VideoCapturer
from src.voice import AudioTranscriber
from src.utils import ActionDictBuilder
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import keyboard
import pyautogui
import time
import json


# Get actions dictionary
actions_path = ["config", "key-commands.json"]
adb = ActionDictBuilder(actions_path)
ops = adb.get_operative_system()
actions = adb.get_actions()
gesture_action_map = adb.get_gesture_action_map(tools=["text_processor", "slides_processor"], type=0)
voice_action_map = adb.get_gesture_action_map(tools=["text_processor", "slides_processor"], type=1)

print(voice_action_map)

# Initialization of models
base_options = python.BaseOptions(model_asset_path=os.path.join(os.getcwd(),"models", "gesture_recognizer.task"))
options = vision.GestureRecognizerOptions(base_options=base_options)
gesture_recognizer = vision.GestureRecognizer.create_from_options(options)
audio_model_path = os.path.join(os.getcwd(), "models", "vosk-model-es-0.42")


wap = WordActionPicker(type="text", gesture_actions_map=gesture_action_map, 
                        voice_command_actions_map=voice_action_map)

voice_recognizer = AudioTranscriber(audio_model_path, action_picker_text=wap, action_picker_slides=None)
stream = voice_recognizer.open_channel()

video_capturer = VideoCapturer(recognizer=gesture_recognizer, action_picker=wap)

if __name__ == "__main__":
    # Here lies all the business logic
    while True:
        gm = voice_recognizer.capture_voice(actions=actions, tool="text_processor", ops=ops)
        if gm == "exit":
            break
        gm = video_capturer.get_gesture(actions=actions, tool="text_processor", ops=ops)
        if gm == "exit":
            break
        
        
    