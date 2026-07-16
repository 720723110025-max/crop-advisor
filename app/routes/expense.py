from flask import Blueprint, render_template, request, redirect

expense_bp = Blueprint(
    "expense",
    __name__,
    url_prefix="/expense"
)

expenses = []

@expense_bp.route("/")
def index():
    total = sum(e["amount"] for e in expenses)
    return render_template(
        "expense/index.html",
        expenses=expenses,
        total=total
    )

@expense_bp.route("/add", methods=["POST"])
def add():

    expenses.append({

        "title": request.form["title"],

        "amount": float(request.form["amount"])

    })

    return redirect("/expense")