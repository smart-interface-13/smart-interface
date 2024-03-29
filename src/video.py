import cv2
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from src.utils import GestureLogger

logger = GestureLogger("logger1")

class VideoCapturer(object):

    def __init__(self, recognizer, action_picker) -> None:
        """Class for the video capture management

        Args:
            recognizer : The model to recognize gestures
            action_picker (WordActionPicker): The action mapper for the software
        """
        self.recognizer = recognizer
        self.action_picker = action_picker

    def get_gesture(self, actions : dict, tool : str, ops : str) -> str:
        """Gets the recognized gesture

        Args:
            actions (dict): Supported actions
            tool (str): The current software tool
            ops (str): Operative system

        Returns:
            str: Control command
        """
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            # Convert the frame to RGB (MediaPipe requires RGB input)
            rgb_frame = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            # Recognize gestures in the frame
            recognition_result = self.recognizer.recognize(rgb_frame)
            out = self._recognize_gesture(frame, recognition_result, actions, tool, ops)
            if out == "close":
                logger.info("Saliendo de modo reconocimiento de gestos")
                return "gesture_mode"
            elif out == "exit":
                return "exit"
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) != -1:
                break
        
            
    def _recognize_gesture(self, frame, gesture : str, actions : dict, tool : str, ops : str) -> str:
        """Gets the name of the recognized gesture and executes its sequence for action

        Args:
            frame (_type_): Frame of the video to recognize
            gesture (str): Gesture object from the model
            actions (dict): Supported actions
            tool (str): The current software tool
            ops (str): Operative system

        Returns:
            str: Control command
        """
        if gesture.gestures:
            top_gesture = gesture.gestures[0][0]
            cv2.putText(frame, f'{top_gesture.category_name} ({top_gesture.score:.2f})', 
            (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            action = top_gesture.category_name
            logger.info(f"Gesto reconocido : {action}")
            action = self.action_picker.map_input_to_action(action, "gesture")
            action_sequence = self.action_picker.get_action_sequence(action=action,
                                                                        actions=actions,
                                                                        tool=tool,
                                                                        ops=ops)
            out = self.action_picker.execute_action(action_sequence)
            return out
