from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import json
import urllib.request

from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.channels.telegram import TelegramInput
from rasa_core.channels import HttpInputChannel
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter
from rasa_core.featurizers import (MaxHistoryTrackerFeaturizer,
                                   BinarySingleStateFeaturizer)

logger = logging.getLogger(__name__)

def train_dialogue(domain_file='./data/dialogue_mgmt/weather_domain.yml',
                    model_path='./models/dialogue',
                    training_data_file='./data/dialogue_mgmt/stories.md'):

    featurizer = MaxHistoryTrackerFeaturizer(BinarySingleStateFeaturizer(), max_history=3)
    agent = Agent(domain_file, policies=[MemoizationPolicy(), KerasPolicy(featurizer)])

    training_data = agent.load_data(training_data_file)
    agent.train(
                training_data,
                epochs=300,
                batch_size=50,
                validation_split=0.2,
                augmentation_factor=50
                )

    agent.persist(model_path)
    return agent


def run_weather_bot(serve_forever=True, train=False):
    logging.basicConfig(level="INFO")
    if train:
        train_dialogue()

    # load Rasa-NLU
    interpreter = RasaNLUInterpreter('./models/nlu/default/weathernlu')
    agent = Agent.load('./models/dialogue', interpreter)

    if serve_forever:
        agent.handle_channel(ConsoleInputChannel())
        
    return agent


def run_telegram_bot(webhook_url, train=False):
    logging.basicConfig(level="INFO")
    if train:
        train_dialogue()

    with open('keys.json') as f:
        data = json.load(f)
    telegram_api_key = data['telegram-api-key']

    # set webhook of telegram bot
    try:
        telegram_url = 'https://api.telegram.org/bot' + telegram_api_key + '/setWebhook?url=' + webhook_url
        urllib.request.urlopen(telegram_url)
    except:
        print("Error setting telegram webhook")
        return

    interpreter = RasaNLUInterpreter('./models/nlu/default/weathernlu')
    agent = Agent.load('./models/dialogue', interpreter)

    input_channel = (TelegramInput(access_token=telegram_api_key,
                                   verify='we11er_bot',
                                   webhook_url=webhook_url,
                                   debug_mode=True))

    agent.handle_channel(HttpInputChannel(5004, '/app', input_channel))


if __name__ == '__main__':
    run_telegram_bot("cf29bb15.ngrok.io/app/webhook", True)