import cv2
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class VideoCapturer(object):

    def __init__(self, recognizer, history) -> None:
        self.recognizer = recognizer
        self.history = history

    def get_gesture(self, frame):
        # Convert the frame to RGB (MediaPipe requires RGB input)
        rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Recognize gestures in the frame
        recognition_result = self.recognizer.recognize(rgb_frame)
        gesture = self._recognize_gesture(frame, recognition_result)
        return gesture
            
    def _recognize_gesture(self, frame, gesture):
        if gesture.gestures:
            top_gesture = gesture.gestures[0][0]
            cv2.putText(frame, f'{top_gesture.category_name} ({top_gesture.score:.2f})', 
            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            if top_gesture.category_name == "ILoveYou":
                print("ILoveYou")
                return top_gesture.category_name
            if top_gesture.category_name == "Victory":
                print("Victory")
                return top_gesture.category_name
            if top_gesture.category_name == "Thumb_Down":
                print("Thumb down")
                return top_gesture.category_name
        


#base_options = python.BaseOptions(model_asset_path=os.path.join(os.getcwd(),'gesture_recognizer.task'))
#options = vision.GestureRecognizerOptions(base_options=base_options)
#recognizer = vision.GestureRecognizer.create_from_options(options)
#vc = VideoCapturer(recognizer)
#vc.get_gesture()