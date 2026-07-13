from flask import Blueprint, render_template

market_bp = Blueprint(
    "market",
    __name__,
    url_prefix="/market"
)


@market_bp.route("/")
def index():

    prices = [

        {
            "crop": "Paddy",
            "market": "Bhubaneswar",
            "price": "₹2450 / Quintal"
        },

        {
            "crop": "Maize",
            "market": "Cuttack",
            "price": "₹2250 / Quintal"
        },

        {
            "crop": "Cotton",
            "market": "Sambalpur",
            "price": "₹7200 / Quintal"
        },

        {
            "crop": "Groundnut",
            "market": "Balasore",
            "price": "₹6100 / Quintal"
        }

    ]

    return render_template(
        "market/index.html",
        prices=prices
    )