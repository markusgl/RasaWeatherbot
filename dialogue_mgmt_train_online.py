from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from rasa_core.agent import Agent
from rasa_core.channels.console import ConsoleInputChannel
from rasa_core.featurizers import MaxHistoryTrackerFeaturizer, BinarySingleStateFeaturizer
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.interpreter import RasaNLUInterpreter

logger = logging.getLogger(__name__)


def run_weather_online(input_channel, interpreter,
                          domain_file="./data/dialogue_mgmt/weather_domain.yml",
                          training_data_file='data/dialogue_mgmt/stories.md'):

    featurizer = MaxHistoryTrackerFeaturizer(BinarySingleStateFeaturizer(), max_history=2)
    agent = Agent(domain_file,
                  policies=[MemoizationPolicy(), KerasPolicy(featurizer)],
                  interpreter=interpreter)

    training_data = agent.load_data(training_data_file)
    agent.train_online(training_data,
                       input_channel=input_channel,
                       batch_size=50,
                       epochs=200,
                       max_training_samples=300)

    return agent


if __name__ == '__main__':
    logging.basicConfig(level="INFO")
    nlu_interpreter = RasaNLUInterpreter('./models/nlu/default/weathernlu')
    run_weather_online(ConsoleInputChannel(), nlu_interpreter)