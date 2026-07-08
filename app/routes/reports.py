from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.database import db_instance

reports_bp = Blueprint(
    "reports",
    __name__,
    url_prefix="/reports"
)

@reports_bp.route("/")
@login_required
def index():

    records = list(
        db_instance.get_collection("farm_income")
        .find({"user_id": str(current_user.id)})
    )

    labels = []
    income = []
    expense = []

    for r in records:
        labels.append(r["crop"])
        income.append(r["income"])
        expense.append(r["expense"])

    return render_template(
        "reports.html",
        labels=labels,
        income=income,
        expense=expense
    )