from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.feedback import FeedbackModel

feedback_bp = Blueprint(
    "feedback",
    __name__,
    url_prefix="/feedback"
)

model = FeedbackModel()

@feedback_bp.route("/")
def index():
    feedbacks = model.get_all()
    return render_template(
        "feedback/index.html",
        feedbacks=feedbacks
    )

@feedback_bp.route("/add", methods=["GET","POST"])
def add():

    if request.method == "POST":

        model.create({

            "farmer":"demo_user",

            "message":request.form["message"]

        })

        flash("Feedback Submitted","success")

        return redirect(url_for("feedback.index"))

    return render_template("feedback/add.html")