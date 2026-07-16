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

    category_totals = {}

    for expense in expenses:

        category = expense["category"]

        category_totals[category] = (
            category_totals.get(category, 0)
            + expense["amount"]
        )

    return render_template(

        "expense/index.html",

        expenses=expenses,

        total=total,

        category_totals=category_totals

    )

@expense_bp.route("/add", methods=["POST"])
def add():

    expenses.append({

        "title": request.form["title"],

        "amount": float(request.form["amount"]),

        "category": request.form["category"],

        "date": request.form["date"]

})

    return redirect("/expense")