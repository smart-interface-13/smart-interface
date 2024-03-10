"""This file contains code and utils to retrain the gesture recognition model
from MediaPipe with custom data
"""

from google.colab import files
import os
import tensorflow as tf
assert tf.__version__.startswith('2')

from mediapipe_model_maker import gesture_recognizer

import matplotlib.pyplot as plt

import neptune

class ModelTrainer(object):

    def __init__(self, dataset_path : str) -> None:
        """Inits the ModelTrainer class

        Args:
            dataset_path (str): Path of the folder with custom images
        """
        self.dataset_path = dataset_path

    def prepare_data(self):
        data = gesture_recognizer.Dataset.from_folder(
        dirname=self.dataset_path,
            hparams=gesture_recognizer.HandDataPreprocessingParams()
        )
        train_data, rest_data = data.split(0.8)
        validation_data, test_data = rest_data.split(0.5)
        return train_data, test_data, validation_data
    
    def train_model(self, train_data, validation_data, run):
        hparams = gesture_recognizer.HParams(export_dir="exported_model")
        run["parameters"] = hparams
        options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)
        model = gesture_recognizer.GestureRecognizer.create(
            train_data=train_data,
            validation_data=validation_data,
            options=options
        )
        return model
    
    def evaluate_model(self, model, test_data, run):
        loss, acc = model.evaluate(test_data, batch_size=1)
        run["eval/loss"] = loss
        run["eval/acc"] = acc
        print(f"Test loss:{loss}, Test accuracy:{acc}")
        return loss, acc

    def optimize_model(model):
        model.export_model()
        files.download('exported_model/gesture_recognizer.task')