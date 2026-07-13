from flask import Blueprint, render_template, request, redirect, url_for

tasks_bp = Blueprint(
    "tasks",
    __name__,
    url_prefix="/tasks"
)

tasks = []


@tasks_bp.route("/")
def index():
    return render_template(
        "tasks/index.html",
        tasks=tasks
    )


@tasks_bp.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        tasks.append({

            "crop": request.form.get("crop"),

            "task": request.form.get("task"),

            "date": request.form.get("date"),

            "status": "Pending"

        })

        return redirect(url_for("tasks.index"))

    return render_template(
        "tasks/add.html"
    )


@tasks_bp.route("/complete/<int:id>")
def complete(id):

    tasks[id]["status"] = "Completed"

    return redirect(url_for("tasks.index"))