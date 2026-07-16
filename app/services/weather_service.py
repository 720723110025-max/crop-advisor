import requests

API_KEY = "288df0f1b431343c7b5ef0cc59a53cfe"

def get_weather(city="Coimbatore"):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    return {
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["main"],
        "wind": data["wind"]["speed"],
    }