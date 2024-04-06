import json
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from cryptography.fernet import Fernet

def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class GestureLogger():

    def __init__(self, name : str, level = logging.INFO) -> None:
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        key = Fernet.generate_key()
        self.cipher = Fernet(key)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        file_handler = RotatingFileHandler(os.path.join('usr','app.log'), maxBytes=10000, backupCount=5)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message):
        #message = self.cipher.encrypt(bytes(message, 'utf-8'))
        self.logger.debug(message)

    def info(self, message):
        #message = self.cipher.encrypt(bytes(message, 'utf-8'))
        self.logger.info(message)
    

class ActionDictBuilder(object):

    def __init__(self, path : list) -> None:
        full_path = os.path.join(*path)
        with open(full_path) as file:
            self.actions_dict = json.load(file)

    def get_actions(self) -> dict:
        return self.actions_dict

    def get_gesture_action_map(self, tools : list, type : int) -> dict:
        gesture_action = dict()
        for tool in tools:
            for action,value in self.actions_dict[tool].items():
                gesture = value["triggers"][type]
                gesture_action[gesture] = action
        return gesture_action
    
    def get_operative_system(self) -> str:
        ops = "macos" if sys.platform == "darwin" else "windows"
        return ops