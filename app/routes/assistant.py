from flask import Blueprint, render_template

assistant_bp = Blueprint(
    "assistant",
    __name__,
    url_prefix="/assistant"
)


@assistant_bp.route("/")
def index():

    data = {

        "weather":"Cloudy 30°C",

        "crop":"Paddy",

        "soil":"Healthy",

        "irrigation":"Required Tomorrow",

        "market":"₹2450 / Quintal",

        "profit":"₹60,000",

        "notification":"Heavy Rain Expected",

        "task":"Apply Fertilizer"

    }

    return render_template(
        "assistant/index.html",
        data=data
    )