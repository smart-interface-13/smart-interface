"""This file contains code and utils to retrain the gesture recognition model
from MediaPipe with custom data
"""

#from google.colab import files
import os
import tensorflow as tf
from mediapipe_model_maker import gesture_recognizer
assert tf.__version__.startswith('2')
import matplotlib.pyplot as plt

import neptune

dataset_path = "src\dataset\Train"
test_path = "src\dataset\Test"

class ModelTrainer(object):

    def __init__(self, dataset_path : str, test_path: str) -> None:
        """Inits the ModelTrainer class

        Args:
            dataset_path (str): Path of the folder with custom images
        """
        self.dataset_path = dataset_path
        self.test_path= test_path

    def prepare_data(self):
        #data = gesture_recognizer.Dataset.from_folder(
        #dirname=self.dataset_path,
            #hparams=gesture_recognizer.HandDataPreprocessingParams()
        #)
        train_data = gesture_recognizer.Dataset.from_folder(
        dirname=self.train_path,
        hparams=gesture_recognizer.HandDataPreprocessingParams()
        )
        test_data = gesture_recognizer.Dataset.from_folder(
        dirname=self.train_path,
        hparams=gesture_recognizer.HandDataPreprocessingParams()
        )
        #train_data, rest_data = data.split(0.8)
        
        #validation_data, test_data = rest_data.split(0.5)
        validation_data=None
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

    def optimize_model(self, model):
        model.export_model()
        #files.download('exported_model/gesture_recognizer.task')

    def visualize_results(self, model, test_data):
        # Visualize some results
        num_examples = 10
        fig, axes = plt.subplots(1, num_examples, figsize=(20, 2))
        for i, (image, label) in enumerate(test_data.dataset.take(num_examples)):
            image = tf.expand_dims(image, axis=0)  # add batch dimension
            prediction = model.predict(image)
            predicted_label = tf.argmax(prediction, axis=1).numpy()[0]
            axes[i].imshow(image.numpy().squeeze())
            axes[i].set_title(f"True: {label.numpy()}, Predicted: {predicted_label}")
            axes[i].axis('off')
        plt.show()

trainer = ModelTrainer(dataset_path, test_path)

train_data, test_data, validation_data = trainer.prepare_data()
#Entrenar modelo
model = trainer.train_model(train_data, validation_data, run)
#Evaluar modelo
loss, acc = trainer.evaluate_model(model, test_data, run)
#Optimizar modelo
trainer.optimize_model(model)
#Visualizar resultados
trainer.visualize_results(model, test_data)