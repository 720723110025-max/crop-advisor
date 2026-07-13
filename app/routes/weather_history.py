from flask import Blueprint, render_template

weather_history_bp = Blueprint(
    "weather_history",
    __name__,
    url_prefix="/weather-history"
)

@weather_history_bp.route("/")
def index():

    history = [
        {"day":"Monday","temp":31,"humidity":70},
        {"day":"Tuesday","temp":32,"humidity":65},
        {"day":"Wednesday","temp":30,"humidity":80},
        {"day":"Thursday","temp":29,"humidity":85},
        {"day":"Friday","temp":33,"humidity":60},
        {"day":"Saturday","temp":34,"humidity":58},
        {"day":"Sunday","temp":32,"humidity":67},
    ]

    return render_template(
        "weather_history/index.html",
        history=history
    )