from flask import Blueprint, render_template
from flask_login import login_required

weather_alert_bp = Blueprint(
    "weather_alert",
    __name__,
    url_prefix="/weather-alerts"
)

@weather_alert_bp.route("/")
@login_required
def index():

    alerts = [

        {
            "type": "Heavy Rain",
            "message": "Expected in next 24 hours. Avoid irrigation."
        },

        {
            "type": "High Temperature",
            "message": "Increase watering frequency."
        },

        {
            "type": "Strong Wind",
            "message": "Protect young crops."
        }

    ]

    return render_template(
        "weather_alerts.html",
        alerts=alerts
    )