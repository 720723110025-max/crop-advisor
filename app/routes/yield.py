from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.yield import YieldModel

yield_bp = Blueprint(

    "yield",

    __name__,

    url_prefix="/yield"

)

model = YieldModel()


@yield_bp.route("/")
@login_required
def index():

    history = model.get_all(current_user.id)

    total_profit = model.total_profit(current_user.id)

    return render_template(

        "yield/index.html",

        history=history,

        total_profit=total_profit

    )


@yield_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        quantity = float(request.form["quantity"])

        price = float(request.form["price"])

        expense = float(request.form["expense"])

        profit = quantity * price - expense

        model.create({

            "user_id": current_user.id,

            "crop": request.form["crop"],

            "quantity": quantity,

            "price": price,

            "expense": expense,

            "profit": profit

        })

        flash("Yield Saved Successfully", "success")

        return redirect(url_for("yield.index"))

    return render_template("yield/add.html")