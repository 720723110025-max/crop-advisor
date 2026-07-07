from flask import Blueprint, render_template
from app.models.admin import AdminModel

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

model = AdminModel()

@admin_bp.route("/dashboard")
def dashboard():

    stats = {

        "users": model.users_count(),

        "feedback": model.feedback_count(),

        "workshops": model.workshop_count(),

        "notifications": model.notification_count()

    }

    return render_template(
        "admin/dashboard.html",
        stats=stats
    )