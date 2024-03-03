import mediapipe as mp
import cv2
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from docx import Document
import pyautogui
import time
import pyperclip

doc = Document("C:\\Users\\pauli\\Documents\\Profesional\\Maestria UNIR\\Seminario IA\\Prueba.docx")

# Create a GestureRecognizer object.
base_options = python.BaseOptions(model_asset_path='gesture_recognizer.task')
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)

# Initialize webcam.
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to RGB (MediaPipe requires RGB input)
    rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    # Recognize gestures in the frame
    recognition_result = recognizer.recognize(rgb_frame)

    # Check if gestures were recognized
    if recognition_result.gestures:
        top_gesture = recognition_result.gestures[0][0]
        cv2.putText(frame, f'{top_gesture.category_name} ({top_gesture.score:.2f})', 
        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        if top_gesture.category_name == "ILoveYou":
            pyautogui.press("win")
            time.sleep(0.1)
            pyautogui.typewrite("Prueba")
            time.sleep(0.1)
            pyautogui.press("enter")
            time.sleep(3)
        if top_gesture.category_name == "Victory":
            pyautogui.hotkey('ctrl', 'v')
            break

    # Display the frame
    cv2.imshow('Webcam', frame)

    # Check for 'q' key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()