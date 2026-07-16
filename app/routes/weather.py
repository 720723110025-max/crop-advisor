from flask import Blueprint, render_template
from flask_login import login_required
from app.services.weather_service import get_weather

weather_bp = Blueprint(
    "weather",
    __name__,
    url_prefix="/weather"
)


@weather_bp.route("/")
@login_required
def dashboard():

    weather = get_weather("Coimbatore")

    advice = []

    if weather:

        if weather["humidity"] > 80:
            advice.append("High humidity. Watch for fungal diseases.")

        if weather["temperature"] > 35:
            advice.append("Irrigate during morning or evening.")

        if weather["condition"].lower() == "rain":
            advice.append("Rain expected. Avoid irrigation.")

        if not advice:
            advice.append("Weather is suitable for farming.")

    return render_template(
        "weather.html",
        weather=weather,
        advice=advice
    )