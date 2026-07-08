from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from app.utils.database import db_instance
from datetime import datetime

income_bp = Blueprint(
    "income",
    __name__,
    url_prefix="/income"
)


@income_bp.route("/")
@login_required
def index():

    records = list(
        db_instance.get_collection("farm_income")
        .find({"user_id": str(current_user.id)})
        .sort("created_at", -1)
    )

    total_income = sum(r.get("income", 0) for r in records)
    total_expense = sum(r.get("expense", 0) for r in records)

    return render_template(
        "farm_income.html",
        records=records,
        total_income=total_income,
        total_expense=total_expense,
        profit=total_income-total_expense
    )


@income_bp.route("/add", methods=["POST"])
@login_required
def add():

    db_instance.get_collection(
        "farm_income"
    ).insert_one({

        "user_id": str(current_user.id),

        "crop": request.form["crop"],

        "income": float(request.form["income"]),

        "expense": float(request.form["expense"]),

        "created_at": datetime.utcnow()

    })

    return redirect("/income/")