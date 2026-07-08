from flask import Blueprint, render_template, jsonify
from datetime import datetime

smart_bp = Blueprint(
    "smart",
    __name__,
    url_prefix="/smart"
)

@smart_bp.route("/")
def index():
    return render_template("smart_notifications.html")


@smart_bp.route("/today")
def today():

    month = datetime.now().month

    notifications = []

    if month in [6,7]:
        notifications.append(
            "🌾 Best time to sow Paddy."
        )

    if month in [10,11]:
        notifications.append(
            "🌽 Harvest Maize this month."
        )

    notifications.append(
        "💧 Check irrigation before evening."
    )

    notifications.append(
        "🌦 Check weather forecast daily."
    )

    return jsonify({
        "notifications": notifications
    })