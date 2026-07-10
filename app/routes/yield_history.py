from flask import Blueprint, render_template

yield_history_bp = Blueprint(
    "yield_history",
    __name__,
    url_prefix="/yield-history"
)

@yield_history_bp.route("/")
def index():

    history = [

        {
            "year":2023,
            "crop":"Paddy",
            "yield":"2200 kg",
            "income":"₹55,000"
        },

        {
            "year":2024,
            "crop":"Paddy",
            "yield":"2400 kg",
            "income":"₹61,000"
        },

        {
            "year":2025,
            "crop":"Paddy",
            "yield":"2550 kg",
            "income":"₹68,000"
        }

    ]

    return render_template(
        "yield_history/index.html",
        history=history
    )