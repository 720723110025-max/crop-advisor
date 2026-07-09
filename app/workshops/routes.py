from flask import Blueprint,render_template,redirect,url_for,flash
from app.models.workshop import WorkshopModel

workshop_bp=Blueprint(
    "workshops",
    __name__,
    url_prefix="/workshops"
)

model=WorkshopModel()


@workshop_bp.route("/")
def index():

    workshops=model.get_all()

    return render_template(
        "workshops/index.html",
        workshops=workshops
    )


@workshop_bp.route("/register/<id>")
def register(id):

    model.register(id)

    flash(
        "Workshop Registered Successfully",
        "success"
    )

    return redirect(
        url_for("workshops.index")
    )