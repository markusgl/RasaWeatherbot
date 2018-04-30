""" Custom Actions for API calls etc """
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from rasa_core.actions.action import Action
from rasa_core.events import SlotSet
from apixu.client import ApixuClient

class ActionWeather(Action):
    def name(self):
        return 'action_weather'

    def run(self, dispatcher, tracker, domain):
        # API call for the weather data
        api_key = 'de03db6657664ea48b184302181604'
        client = ApixuClient(api_key)

        loc = tracker.get_slot('location')
        time = tracker.get_slot('time')
        weather = client.getCurrentWeather(q=loc)
        if time:
            weather = client.getForecastWeather(q=loc)

        country = weather['location']['country']
        city = weather['location']['name']
        condition = weather['current']['condition']['text']
        temperature = weather['current']['temp_c']
                
        response = """Es ist aktuell {} in {}. Die Temperature beträgt {} °C.""".format(condition, city, temperature)

        # tell the chatbot that this message has to be send out
        dispatcher.utter_message(response)
        # return current slot value
        return [SlotSet('location',loc)]
