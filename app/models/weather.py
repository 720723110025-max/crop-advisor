import requests
import os

class WeatherModel:

    def get_weather(self, city="Coimbatore"):

        api=os.getenv("288df0f1b431343c7b5ef0cc59a53cfe")

        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api}&units=metric"

        response=requests.get(url).json()

        return{

            "temperature":response["main"]["temp"],

            "humidity":response["main"]["humidity"],

            "wind":response["wind"]["speed"],

            "condition":response["weather"][0]["main"]

        }

    def irrigation_advice(self,weather):

        if weather["temperature"]>35:

            return "Water your crops in morning."

        elif weather["humidity"]>80:

            return "Avoid over irrigation."

        else:

            return "Weather is suitable."