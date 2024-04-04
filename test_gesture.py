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
base_options = python.BaseOptions(model_asset_path=os.path.join(os.getcwd(),"models", "data_model4.task"))
options = vision.GestureRecognizerOptions(base_options=base_options)
gesture_recognizer = vision.GestureRecognizer.create_from_options(options)
audio_model_path = os.path.join(os.getcwd(), "models", "vosk-model-small-es-0.42")

wap = WordActionPicker(type="text", gesture_actions_map=gesture_action_map, 
                        voice_command_actions_map=voice_action_map)

voice_recognizer = AudioTranscriber(audio_model_path, action_picker_text=wap)
stream = voice_recognizer.open_channel()

video_capturer = VideoCapturer(recognizer=gesture_recognizer, action_picker=wap)

if __name__ == "__main__":
    last_voice_gesture = None
    last_video_gesture = None
    while True:
        # Captura del gesto de voz
        voice_gesture = voice_recognizer.capture_voice(actions=actions, tool="text_processor", ops=ops)
        if voice_gesture == "exit":
            break
        # Verifica si el gesto de voz capturado es diferente al anterior
        if voice_gesture != last_voice_gesture:
            last_voice_gesture = voice_gesture
            # Captura del gesto visual
            video_gesture = video_capturer.get_gesture(actions=actions, tool="text_processor", ops=ops)
            if video_gesture == "exit":
                break
            # Verifica si el gesto visual capturado es diferente al anterior
            if video_gesture != last_video_gesture:
                last_video_gesture = video_gesture
                # Aquí puedes realizar las acciones correspondientes a los gestos capturados
    