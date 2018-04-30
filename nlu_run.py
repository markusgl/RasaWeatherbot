from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Interpreter

def run_nlu():
    interpreter = Interpreter.load('./models/nlu/default/weathernlu', RasaNLUConfig('config_spacy.json'))
    print(interpreter.parse(u"Wie wird das Wetter in Berlin heute?"))

if __name__ == '__main__':
    run_nlu()