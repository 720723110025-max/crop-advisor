from flask import Blueprint, render_template

smart_bp = Blueprint(
    "smart",
    __name__,
    url_prefix="/notifications"
)


@smart_bp.route("/")
def index():

    notifications = [

        {
            "title":"🌧 Weather Alert",
            "message":"Heavy rainfall expected tomorrow."
        },

        {
            "title":"💧 Irrigation",
            "message":"No irrigation required for next 2 days."
        },

        {
            "title":"🌾 Harvest",
            "message":"Paddy harvesting starts next week."
        },

        {
            "title":"💰 Market",
            "message":"Rice price increased by ₹250 per quintal."
        },

        {
            "title":"🎓 Workshop",
            "message":"Organic Farming Workshop on Sunday."
        }

    ]

    return render_template(
        "notifications/index.html",
        notifications=notifications
    )