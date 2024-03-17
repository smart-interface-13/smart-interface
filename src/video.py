import cv2
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class VideoCapturer(object):

    def __init__(self, recognizer) -> None:
        self.recognizer = recognizer

    def get_gesture(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()
            if not ret:
                break
            # Convert the frame to RGB (MediaPipe requires RGB input)
            rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            # Recognize gestures in the frame
            recognition_result = self.recognizer.recognize(rgb_frame)
            gesture = self._recognize_gesture(frame, recognition_result)
            # Display the frame
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) != -1:
            #if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def _recognize_gesture(self, frame, gesture):
        if gesture.gestures:
            top_gesture = gesture.gestures[0][0]
            cv2.putText(frame, f'{top_gesture.category_name} ({top_gesture.score:.2f})', 
            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if top_gesture.category_name == "ILoveYou":
                print("ILoveYou")
            if top_gesture.category_name == "Victory":
                print("Victory")
            if top_gesture.category_name == "Thumb_Down":
                print("Thumb down")
        return gesture


base_options = python.BaseOptions(model_asset_path=os.path.join(os.getcwd(),'gesture_recognizer.task'))
options = vision.GestureRecognizerOptions(base_options=base_options)
recognizer = vision.GestureRecognizer.create_from_options(options)
vc = VideoCapturer(recognizer)
vc.get_gesture()