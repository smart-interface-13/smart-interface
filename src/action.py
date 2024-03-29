"""This file contains the general code for gesture/command-action mapping
"""

from abc import ABC, abstractmethod
import pyautogui
import time
from src.utils import singleton, GestureLogger

logger = GestureLogger("logger1")

class SoftwareActionPicker(ABC):

    def __init__(self, type : str) -> None:
        """This method initialized the abstract SoftwareProduct

        Args:
            type (str): Type of product such as : Word or PowerPoint
        """
        self.type = type

    @abstractmethod
    def map_input_to_action(self, input : str) -> str:
        pass

    @abstractmethod
    def execute_action(self, action : str) -> None:
        pass

@singleton
class WordActionPicker(SoftwareActionPicker):

    def __init__(self, type: str, gesture_actions_map : dict, voice_command_actions_map : dict) -> None:
        super().__init__(type)
        self.gesture_actions_map = gesture_actions_map
        self.voice_command_actions_map = voice_command_actions_map
        
    def map_input_to_action(self, input: str, type : str) -> str:
        action = ""
        if type == "gesture":
            try:
                action = self.gesture_actions_map[input]
            except KeyError as e:
                logger.info("Gesto no reconocido")
        elif type == "voice":
            try:
                action = self.voice_command_actions_map[input]
                logger.info(f"Comando de voz reconocido {action}")
            except KeyError as e:
                logger.info("Comando de voz no reconocido")
        else:
            raise Exception("Type of input not supported. Check supported types: 'gesture' and 'voice'")
        return action
    
    def get_action_sequence(self, action : str, actions : dict, tool : str, ops : str) -> dict:
        tool_actions = actions[tool]
        seq_type = "sequence_" + ops
        try:
            sequence = tool_actions[action][seq_type]
        except:
            sequence = {}
        return sequence

    def execute_action(self, action_sequence : dict, text : str = "") -> None:
        for step, keys in action_sequence.items():
            logger.info(str(step[1:]) + str(keys))
            if step[1:] == "press":
                pyautogui.press(keys)
            elif step[1:] == "hotkey":
                pyautogui.hotkey(keys)
            elif step[1:] == "typewrite":
                if len(keys) > 0:
                    pyautogui.typewrite(keys)
                else:
                    pyautogui.typewrite(text)
            elif step[1:] == "close":
                return "close"
            elif step[1:] == "exit":
                return "exit"
            time.sleep(0.1)

@singleton
class PowerPointActionPicker(SoftwareActionPicker):

    def __init__(self, type: str, gesture_actions_map : dict, voice_command_actions_map : dict, logger) -> None:
        super().__init__(type)
        self.gesture_actions_map = gesture_actions_map
        self.voice_command_actions_map = voice_command_actions_map
        logger = logger

    def map_input_to_action(self, input: str, type : str) -> str:
        action = ""
        if type == "gesture":
            try:
                action = self.gesture_actions_map[input]
            except KeyError as e:
                logger.info("Gesto no reconocido")
        elif type == "voice":
            try:
                action = self.voice_command_actions_map[input]
            except KeyError as e:
                logger.info("Comando de voz no reconocido")
        else:
            raise Exception("Type of input not supported. Check supported types: 'gesture' and 'voice'")
        return action
    
    def execute_action(self, action_sequence : dict, text : str = "") -> None:
        for step, keys in action_sequence.items():
            logger.info(str(step[1:]) + str(keys))
            if step[1:] == "press":
                pyautogui.press(keys)
            elif step[1:] == "hotkey":
                pyautogui.hotkey(keys)
            elif  step[1:] == "typewrite":
                if len(keys) > 0:
                    pyautogui.typewrite(keys)
                else:
                    pyautogui.typewrite(text)
            time.sleep(0.1)
