from flask import Blueprint, render_template, request, redirect, url_for

profit_bp = Blueprint(
    "profit",
    __name__,
    url_prefix="/profit"
)

records = []


@profit_bp.route("/")
def index():

    total_income = sum(r["income"] for r in records)

    total_expense = sum(r["expense"] for r in records)

    total_profit = sum(r["profit"] for r in records)

    return render_template(

        "profit/index.html",

        records=records,

        total_income=total_income,

        total_expense=total_expense,

        total_profit=total_profit

    )


@profit_bp.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        crop = request.form.get("crop")

        quantity = float(request.form.get("quantity"))

        expense = float(request.form.get("expense"))

        price = float(request.form.get("price"))

        income = quantity * price

        profit = income - expense

        records.append({

            "crop": crop,

            "quantity": quantity,

            "expense": expense,

            "income": income,

            "profit": profit

        })

        return redirect(
            url_for("profit.index")
        )

    return render_template(
        "profit/add.html"
    )