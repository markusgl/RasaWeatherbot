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

        # API XU
        api_key = 'de03db6657664ea48b184302181604'
        client = ApixuClient(api_key)

        loc = tracker.get_slot('location')
        time = tracker.get_slot('time')
        if time and loc:
            if time == 'heute':
                weather = client.getCurrentWeather(q=loc)
            elif time == 'morgen':
                weather = client.getForecastWeather(q=loc, days=1)
            elif time == 'übermorgen':
                weather = client.getForecastWeather(q=loc, days=2)
            else:
                weather = client.getForecastWeather(q=loc, days=3) #TODO calculate days until specific date
        else:
            weather = client.getCurrentWeather(q=loc)

        #country = weather['location']['country']
        city = weather['location']['name']
        condition = weather['current']['condition']['text']
        temperature = weather['current']['temp_c']

        if condition == 'Sunny':
            condition = 'sonnig'
        elif condition == 'Cloudy':
            condition = 'bewölkt'

        # WORLD WEATHER ONLINE
        #api_key = '5beaed4b1ee84cdd9b485549181704'

        response = """Es ist aktuell {} in {}. Die Temperatur beträgt {} °C.""".format(condition, city, temperature)

        # tell the chatbot that this message has to be send out
        dispatcher.utter_message(response)
        # return current slot value
        return [SlotSet('location', loc)]
