from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.market import MarketModel

market_bp = Blueprint(
    "market",
    __name__,
    url_prefix="/market"
)

market_model = MarketModel()


@market_bp.route("/")
@login_required
def index():

    prices = market_model.get_prices()

    return render_template(
        "market/index.html",
        prices=prices
    )


@market_bp.route("/add", methods=["GET","POST"])
@login_required
def add():

    if current_user.role != "admin":

        flash("Only Admin can add prices","danger")

        return redirect(url_for("market.index"))

    if request.method=="POST":

        market_model.create({

            "crop":request.form["crop"],

            "district":request.form["district"],

            "market":request.form["market"],

            "price":request.form["price"],

            "unit":request.form["unit"],

            "trend":request.form["trend"]

        })

        flash("Market Price Added","success")

        return redirect(url_for("market.index"))

    return render_template("market/add.html")