import requests
from flask import Blueprint, render_template, request

weather_bp = Blueprint("weather", __name__)

API_KEY = "288df0f1b431343c7b5ef0cc59a53cfe"


@weather_bp.route("/advisory", methods=["GET", "POST"])
def advisory():

    city = "Coimbatore"

    if request.method == "POST":
        city = request.form.get("city", "Coimbatore")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)

    if response.status_code != 200:
        return render_template(
            "weather.html",
            error="City not found."
        )

    data = response.json()

    weather = {
        "city": city,
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "condition": data["weather"][0]["main"],
        "description": data["weather"][0]["description"],
        "wind": data["wind"]["speed"],
        "icon": data["weather"][0]["icon"]
    }

    return render_template(
        "weather.html",
        weather=weather
    )