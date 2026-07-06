from flask import Blueprint, render_template, request
from flask_login import login_required
from app.utils.database import db_instance
from bson import ObjectId
from flask import redirect, url_for, flash
from flask import send_file
import io
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from flask import Blueprint, render_template
from app.utils.database import count

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/dashboard")
def dashboard():

    stats = {
        "farmers": count("farmers"),
        "experts": count("experts"),
        "lands": count("lands"),
        "workshops": count("workshops"),
        "feedback": count("feedback")
    }

    return render_template(
        "admin/dashboard.html",
        stats=stats
    )

    users = db_instance.get_collection("users").count_documents({})
    diseases = db_instance.get_collection("disease_reports").count_documents({})
    crops = db_instance.get_collection("crop_predictions").count_documents({})
    yields = db_instance.get_collection("yield_predictions").count_documents({})
    irrigation = db_instance.get_collection("irrigation_history").count_documents({})
    weather = db_instance.get_collection("weather_history").count_documents({})

    recent_reports = list(
        db_instance.get_collection("disease_reports")
        .find()
        .sort("created_at", -1)
        .limit(5)
    )

    notifications = list(
        db_instance.get_collection("notifications")
        .find()
        .sort("created_at", -1)
        .limit(10)
    )

    return render_template(
        "admin/dashboard.html",
        users=users,
        diseases=diseases,
        crops=crops,
        yields=yields,
        irrigation=irrigation,
        weather=weather,
        recent_reports=recent_reports,
        notifications=notifications
    )

@admin_bp.route("/users")
@login_required
def users():

    search = request.args.get("search", "")

    if search:
        users = list(
            db_instance.get_collection("users").find({
                "username": {
                    "$regex": search,
                    "$options": "i"
                }
            })
        )
    else:
        users = list(
            db_instance.get_collection("users").find()
        )

    return render_template(
        "admin/users.html",
        users=users
    )

@admin_bp.route("/delete-user/<user_id>")
@login_required
def delete_user(user_id):
    try:
        db_instance.get_collection("users").delete_one(
            {"_id": ObjectId(user_id)}
        )
        flash("User deleted successfully!", "success")
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", "danger")

    return redirect(url_for("admin.users"))

@admin_bp.route("/make-admin/<user_id>")
@login_required
def make_admin(user_id):
    try:
        db_instance.get_collection("users").update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_admin": True}}
        )

        flash("User promoted to Admin successfully!", "success")

    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("admin.users"))
@admin_bp.route("/remove-admin/<user_id>")
@login_required
def remove_admin(user_id):
    try:
        db_instance.get_collection("users").update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"is_admin": False}}
        )

        flash("Admin removed successfully!", "success")

    except Exception as e:
        flash(str(e), "danger")

    return redirect(url_for("admin.users"))

@admin_bp.route("/reports")
@login_required
def reports():

    reports = list(
        db_instance.get_collection("disease_reports")
        .find()
        .sort("created_at", -1)
    )

    return render_template(
        "admin/reports.html",
        reports=reports
    )
@admin_bp.route("/export-users")
@login_required
def export_users():

    users = list(
        db_instance.get_collection("users").find()
    )

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    data = [
        ["Username", "Email", "Admin"]
    ]

    for user in users:

        data.append([
            user.get("username", ""),
            user.get("email", ""),
            str(user.get("is_admin", False))
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.green),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige)
    ]))

    doc.build([table])

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Users_Report.pdf",
        mimetype="application/pdf"
    )
@admin_bp.route("/delete-report/<report_id>")
@login_required
def delete_report(report_id):

    try:
        db_instance.get_collection("disease_reports").delete_one(
            {"_id": ObjectId(report_id)}
        )

        flash("Report deleted successfully!", "success")

    except Exception as e:

        flash(str(e), "danger")

    return redirect(url_for("admin.reports"))