import requests

API_KEY = "288df0f1b431343c7b5ef0cc59a53cfe"


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city):

    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)

    data = response.json()

    return {

        "temperature": data["main"]["temp"],

        "humidity": data["main"]["humidity"],

        "condition": data["weather"][0]["main"],

        "wind": data["wind"]["speed"],

        "rain": data.get("clouds", {}).get("all", 0)

    }