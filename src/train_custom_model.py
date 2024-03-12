import os
import neptune
from dotenv import load_dotenv
from src.model_trainer import ModelTrainer

load_dotenv()

dataset_path = ""
run = neptune.init_run(
    project=os.environ["NEPTUNE_PROJECT"],
    api_token=os.environ["NEPTUNE_API_KEY"],
)

model_trainer = ModelTrainer(dataset_path)
train_data, test_data, validation_data = model_trainer.prepare_data()
model = model_trainer.train_model(train_data=train_data, validation_data=validation_data, run=run)
loss, acc = model_trainer.evaluate_model(model=model, test_data=test_data, run=run)
model_trainer.optimize_model(model)

run.stop()