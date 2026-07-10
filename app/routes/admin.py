from flask import Blueprint, render_template

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


@admin_bp.route("/")
def dashboard():

    stats = {

        "farmers":245,

        "lands":580,

        "experts":18,

        "workshops":34,

        "notifications":156,

        "diseases":73,

        "predictions":450,

        "profit":"₹18,75,000"

    }

    return render_template(

        "admin/dashboard.html",

        stats=stats

    )