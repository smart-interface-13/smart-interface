# Import the necessary modules.
from mediapipe_model_maker import gesture_recognizer

data = gesture_recognizer.Dataset.from_folder(
    dirname=IMAGES_PATH,
    hparams=gesture_recognizer.HandDataPreprocessingParams()
)

# Split the archive into training, validation and test dataset.
train_data, rest_data = data.split(0.8)
validation_data, test_data = rest_data.split(0.5)
#80% of the data is used for training, with the remaining data split in half, so that 10% of the total is used for testing, and 10% for validation
# Entrenar el modelo
hparams = gesture_recognizer.HParams( export_dir="data_model")
options = gesture_recognizer.GestureRecognizerOptions(hparams=hparams)
model = gesture_recognizer.GestureRecognizer.create(
    train_data=train_data,  # Modifica tus datos de entrenamiento según sea necesario
    validation_data=validation_data,  # Modifica tus datos de validación según sea necesario
    options=options
)
loss, acc = model.evaluate(test_data, batch_size=1)
print(f"Test loss:{loss}, Test accuracy:{acc}")
# Export the model bundle.
model.export_model()

