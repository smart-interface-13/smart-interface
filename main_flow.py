"""This file contains the main loop to run the prototype
"""

from src.action import WordActionPicker
from src.video import VideoCapturer
from src.voice import AudioTranscriber
from src.utils import ActionDictBuilder
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os

# Get actions dictionary
actions_path = ["config", "key-commands.json"]
adb = ActionDictBuilder(actions_path)
ops = adb.get_operative_system()
actions = adb.get_actions()
gesture_action_map = adb.get_gesture_action_map(tools=["text_processor"], type=0)
voice_action_map = adb.get_gesture_action_map(tools=["text_processor"], type=1)

print(voice_action_map)

# Initialization of models
base_options = python.BaseOptions(model_asset_path=os.path.join(os.getcwd(),"src", "modelo_3", "data_model3.task"))
options = vision.GestureRecognizerOptions(base_options=base_options)
gesture_recognizer = vision.GestureRecognizer.create_from_options(options)
audio_model_path = os.path.join(os.getcwd(), "Models", "es")

wap = WordActionPicker(type="text", gesture_actions_map=gesture_action_map, 
                        voice_command_actions_map=voice_action_map)

voice_recognizer = AudioTranscriber(audio_model_path, action_picker_text=wap)
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
        
        
    