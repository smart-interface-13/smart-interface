import json
import os
import sys

class ActionDictBuilder(object):

    def __init__(self, path : list) -> None:
        full_path = os.join(*path)
        with open(full_path) as file:
            self.actions_dict = json.load(file)

    def get_gesture_action_map(self, tool : str, type : int) -> dict:
        gesture_action = dict()
        for action,value in self.actions_dict[tool].items():
            gesture = value["triggers"][type]
            gesture_action[gesture] = action
        return gesture_action
    
    def get_operative_system(self) -> str:
        ops = "macos" if sys.platform == "darwin" else "windows"
        return ops