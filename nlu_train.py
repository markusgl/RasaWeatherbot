from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.model import Trainer, Interpreter


def train_nlu(data, config_file, model_dir):
    training_data = load_data(data)
    trainer = Trainer(config.load(config_file))
    trainer.train(training_data)

    # output directory for the trained model
    trainer.persist(model_dir, fixed_model_name="weathernlu")


if __name__ == '__main__':
    print("training started...")
    train_nlu('./data/nlu/data.json', 'config_spacy.json', './models/nlu')
    print("training finished.")