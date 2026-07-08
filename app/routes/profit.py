from flask import Blueprint, render_template, request, jsonify

profit_bp = Blueprint(
    "profit",
    __name__,
    url_prefix="/profit"
)

@profit_bp.route("/")
def index():
    return render_template("profit.html")


@profit_bp.route("/calculate", methods=["POST"])
def calculate():

    area = float(request.form["area"])
    yield_per_acre = float(request.form["yield"])
    market_price = float(request.form["price"])
    cost = float(request.form["cost"])

    income = area * yield_per_acre * market_price
    profit = income - cost

    return jsonify({
        "income": income,
        "profit": profit
    })