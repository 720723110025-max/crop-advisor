from flask import Blueprint, render_template
from flask_login import login_required
from app.models.weather import WeatherModel

weather_bp = Blueprint(

    "weather",

    __name__,

    url_prefix="/weather"

)

model = WeatherModel()


@weather_bp.route("/")
@login_required
def dashboard():

    weather = model.get_weather()

    advice = model.irrigation_advice(weather)

    return render_template(

        "weather/index.html",

        weather=weather,

        advice=advice

    )