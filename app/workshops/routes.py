from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.workshop import WorkshopModel

workshop_bp = Blueprint(
    "workshops",
    __name__,
    url_prefix="/workshops"
)

model = WorkshopModel()


# ==========================
# View All Workshops
# ==========================

@workshop_bp.route("/")
@login_required
def index():

    workshops = model.get_all()

    return render_template(
        "workshops/index.html",
        workshops=workshops
    )


# ==========================
# Add Workshop (Admin)
# ==========================

@workshop_bp.route("/add", methods=["GET","POST"])
@login_required
def add():

    if current_user.role != "admin":

        flash("Only Admin can create workshops", "danger")

        return redirect(url_for("workshops.index"))

    if request.method == "POST":

        model.create({

            "title": request.form["title"],

            "description": request.form["description"],

            "district": request.form["district"],

            "mode": request.form["mode"],

            "location": request.form["location"],

            "date": request.form["date"],

            "time": request.form["time"],

            "capacity": request.form["capacity"],

            "speaker": request.form["speaker"],

            "resource": request.form["resource"]

        })

        flash("Workshop Created Successfully", "success")

        return redirect(url_for("workshops.index"))

    return render_template("workshops/add.html")


# ==========================
# Register Workshop
# ==========================

@workshop_bp.route("/register/<id>")
@login_required
def register(id):

    model.register(id)

    flash("Workshop Registered Successfully", "success")

    return redirect(url_for("workshops.index"))


# ==========================
# Edit Workshop
# ==========================

@workshop_bp.route("/edit/<id>", methods=["GET","POST"])
@login_required
def edit(id):

    if current_user.role != "admin":

        flash("Access Denied", "danger")

        return redirect(url_for("workshops.index"))

    workshop = model.get(id)

    if request.method == "POST":

        model.update(id, {

            "title": request.form["title"],

            "description": request.form["description"],

            "district": request.form["district"],

            "mode": request.form["mode"],

            "location": request.form["location"],

            "date": request.form["date"],

            "time": request.form["time"],

            "capacity": request.form["capacity"],

            "speaker": request.form["speaker"],

            "resource": request.form["resource"]

        })

        flash("Workshop Updated Successfully", "success")

        return redirect(url_for("workshops.index"))

    return render_template(
        "workshops/edit.html",
        workshop=workshop
    )


# ==========================
# Delete Workshop
# ==========================

@workshop_bp.route("/delete/<id>")
@login_required
def delete(id):

    if current_user.role != "admin":

        flash("Access Denied", "danger")

        return redirect(url_for("workshops.index"))

    model.delete(id)

    flash("Workshop Deleted Successfully", "success")

    return redirect(url_for("workshops.index"))