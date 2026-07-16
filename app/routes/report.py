from flask import Blueprint, send_file
from reportlab.pdfgen import canvas

report_bp = Blueprint(
    "report",
    __name__,
    url_prefix="/report"
)

@report_bp.route("/pdf")
def pdf():

    c = canvas.Canvas("report.pdf")

    c.drawString(
        100,
        800,
        "Crop Advisory Report"
    )

    c.save()

    return send_file(
        "report.pdf",
        as_attachment=True
    )