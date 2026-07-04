from flask import Blueprint, send_file
from flask_login import login_required
from app.utils.database import db_instance
from openpyxl import Workbook
import io

export_bp = Blueprint("export", __name__)

@export_bp.route("/users")
@login_required
def export_users():

    users = db_instance.get_collection("users").find()

    wb = Workbook()
    ws = wb.active
    ws.title = "Users"

    ws.append([
        "Username",
        "Email",
        "Full Name",
        "Phone"
    ])

    for user in users:
        ws.append([
            user.get("username"),
            user.get("email"),
            user.get("full_name"),
            user.get("phone")
        ])

    file = io.BytesIO()
    wb.save(file)
    file.seek(0)

    return send_file(
        file,
        as_attachment=True,
        download_name="users.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )