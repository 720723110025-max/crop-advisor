from flask import Blueprint, render_template, request, redirect, url_for

diary_bp = Blueprint(
    "diary",
    __name__,
    url_prefix="/diary"
)

entries = []


@diary_bp.route("/")
def index():
    return render_template(
        "diary/index.html",
        entries=entries
    )


@diary_bp.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        entries.append({

            "crop": request.form.get("crop"),

            "date": request.form.get("date"),

            "fertilizer": request.form.get("fertilizer"),

            "irrigation": request.form.get("irrigation"),

            "notes": request.form.get("notes")

        })

        return redirect(url_for("diary.index"))

    return render_template(
        "diary/add.html"
    )