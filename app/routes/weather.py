from flask import Blueprint, render_template

from app.services.weather_service import get_weather

weather_bp = Blueprint(
    "weather",
    __name__,
    url_prefix="/weather"
)


@weather_bp.route("/")
def dashboard():

    weather = get_weather("Coimbatore")

    return render_template(

        "weather.html",

        weather=weather

    )