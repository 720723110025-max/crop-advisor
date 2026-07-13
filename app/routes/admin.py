from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.user import User

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

def admin_required():

    if not current_user.is_authenticated:
        abort(403)

    if current_user.role != "admin":
        abort(403)


@admin_bp.route("/")
@login_required
def dashboard():

    admin_required()

    stats = {

    "farmers": User._get_collection().count_documents({"role":"farmer"}),

    "experts": User._get_collection().count_documents({"role":"expert"}),

    "admins": User._get_collection().count_documents({"role":"admin"}),

    "lands":0,

    "workshops":0,

    "notifications":0,

    "diseases":0,

    "predictions":0,

    "profit":"₹0"

}

    return render_template(
        "admin/dashboard.html",
        stats=stats
    )


# ==========================
# Expert Management
# ==========================

@admin_bp.route("/experts")
@login_required
def experts():

    admin_required()
    experts = User._get_collection().find({"role": "expert"})

    return render_template(
        "admin/experts.html",
        experts=experts
    )

@admin_bp.route("/farmers")
@login_required
def farmers():

    admin_required()

    farmers = User._get_collection().find({"role": "farmer"})

    return render_template(
        "admin/farmers.html",
        farmers=farmers
    )


@admin_bp.route("/add-expert", methods=["GET","POST"])
@login_required
def add_expert():

    admin_required()

    if request.method == "POST":

        expert = User(
            username=request.form["username"],
            email=request.form["email"],
            password=request.form["password"],
            full_name=request.form["full_name"],
            phone=request.form["phone"],
            district=request.form["district"],
            role="expert"
        )

        expert.save()

        flash("Expert Added Successfully", "success")

        return redirect(url_for("admin.experts"))

    return render_template("admin/add_expert.html")
