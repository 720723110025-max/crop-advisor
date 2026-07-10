from flask import Blueprint, render_template

weather_bp = Blueprint(
    "weather",
    __name__,
    url_prefix="/weather"
)


@weather_bp.route("/")
def index():

    weather = {

        "location":"Odisha",

        "temperature":"31°C",

        "humidity":"78%",

        "wind":"15 km/h",

        "rain":"80%",

        "condition":"Cloudy",

        "advice":"Heavy rainfall expected. Avoid irrigation today."

    }

    return render_template(

        "weather/index.html",

        weather=weather

    )