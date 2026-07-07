from flask import Blueprint, render_template
from app.models.market import MarketModel

market_bp = Blueprint(
    "market",
    __name__,
    url_prefix="/market"
)

model = MarketModel()

@market_bp.route("/")
def index():

    prices = model.get_all()

    return render_template(
        "market/index.html",
        prices=prices
    )