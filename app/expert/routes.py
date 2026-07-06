from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.expert import ExpertModel

expert_bp = Blueprint(
    "expert",
    __name__,
    url_prefix="/expert"
)

expert_model = ExpertModel()

@expert_bp.route("/")
def index():
    experts = expert_model.get_all()
    return render_template("expert/index.html", experts=experts)


@expert_bp.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        expert_model.create({

            "name": request.form["name"],

            "district": request.form["district"],

            "specialization": request.form["specialization"],

            "phone": request.form["phone"],

            "email": request.form["email"]

        })

        flash("Expert Added Successfully", "success")

        return redirect(url_for("expert.index"))

    return render_template("expert/add.html")