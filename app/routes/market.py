from flask import Blueprint, render_template
from app.services.market_service import MarketService

market_bp = Blueprint(
    "market",
    __name__,
    url_prefix="/market"
)


@market_bp.route("/")
def index():

    prices = [
        service = MarketService()
        prices = service.get_prices()
    ]

    return render_template(
        "market/index.html",
        prices=prices
    )