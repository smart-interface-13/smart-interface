"""This file contains the general code for gesture/command-action mapping
"""

from abc import ABC, abstractmethod
import pyautogui
import time
    
def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        print(cls)
        print(instances)
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


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
                print("Gesto no reconocido")
        elif type == "voice":
            try:
                action = self.voice_command_actions_map[input]
            except KeyError as e:
                print("Comando de voz no reconocido")
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
            print(step[1:], keys)
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

@singleton
class PowerPointActionPicker(SoftwareActionPicker):

    def __init__(self, type: str) -> None:
        super().__init__(type)
        self.gesture_actions_map = {
            "Gesture1" : "Action10",
            "Gesture2" : "Action20",
        }
        self.voice_command_actions_map = {
            "Voice1" : "Action30",
            "Voice2" : "Action40",
        }

    def map_input_to_action(self, input: str, type : str) -> str:
        action = ""
        if type == "gesture":
            try:
                action = self.gesture_actions_map[input]
            except KeyError as e:
                print(e)
        elif type == "voice":
            try:
                action = self.voice_command_actions_map[input]
            except KeyError as e:
                print(e)
        else:
            raise Exception("Type of input not supported. Check supported types: 'gesture' and 'voice'")
        return action
    
    def execute_action(self, action: str) -> None:
        pass

"""
software_open = "Word"
if software_open == "Word":
    action_picker = WordActionPicker(type = software_open.lower())
    action_picker2 = WordActionPicker(type = software_open.lower())
elif software_open == "PowerPoint":
    action_picker = PowerPointActionPicker(type = software_open.lower())
else:
    raise Exception("Attempted to open a non supported software")

gesture = "Gesture1"
input_type = "gesture"
action = action_picker.map_input_to_action(gesture, type=input_type)
print(f"The action taken for gesture : {gesture} of type {input_type} is {action}")

if id(action_picker) == id(action_picker2):
    print("Word is aplying Singleton")
else:
    print("No successful singleton")"""