import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from docx import Document
import pyautogui
import time
import pyperclip
import os
from vosk import Model, KaldiRecognizer
import pyaudio
import json

ruta = "C:\\Users\\pauli\\Documents\\Profesional\\Maestria UNIR\\Seminario IA\\Prueba.docx"

# Modelo de reconocimiento de voz
model = Model("C:\\Users\\pauli\\Documents\\Python Projects\\Vosk Models\\es")
voice_recog = KaldiRecognizer(model, 16000)

# Create a GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

def voice_commands(recognizer):
    cap = pyaudio.PyAudio()
    stream = cap.open(format=pyaudio.paInt16, 
                    channels=1, 
                    rate=16000, 
                    input=True, 
                    frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            if result.get('text') :
                print("Texto transrito:", result['text'])
                if result['text'] == "abrir archivo":
                    open_word()
                if result['text'] == "pegar":
                    paste_word()
                if result['text'] == "deshacer":
                    undo_word()

# Initialize webcam.
def webcam(recog):
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break
        # Convert the frame to RGB (MediaPipe requires RGB input)
        rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Recognize gestures in the frame
        recognition_result = recog.recognize(rgb_frame)
        gest_rec(frame, recognition_result)
        # Display the frame
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) != -1:
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def open_word():
    global ruta
    nombre_archivo = os.path.basename(ruta)
    pyautogui.press("win")
    time.sleep(0.1)
    pyautogui.typewrite(nombre_archivo)
    time.sleep(0.15)
    pyautogui.press("enter")
    time.sleep(3)

def undo_word():
    pyautogui.hotkey('ctrl', 'z')

def paste_word():
    pyautogui.hotkey('ctrl', 'v')

def gest_rec(fr, gesture):
    if gesture.gestures:
        top_gesture = gesture.gestures[0][0]
        cv2.putText(fr, f'{top_gesture.category_name} ({top_gesture.score:.2f})', 
        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if top_gesture.category_name == "ILoveYou":
            open_word(ruta)
        if top_gesture.category_name == "Victory":
            paste_word()
        if top_gesture.category_name == "Thumb_Down":
            undo_word()

#webcam(recognizer)
voice_commands(voice_recog)
