from flask import Blueprint, send_file
from reportlab.pdfgen import canvas
import os

report_bp = Blueprint(
    "report",
    __name__,
    url_prefix="/report"
)


@report_bp.route("/profit")
def profit_report():

    os.makedirs("reports", exist_ok=True)

    pdf = "reports/profit_report.pdf"

    c = canvas.Canvas(pdf)

    c.setFont("Helvetica-Bold",18)

    c.drawString(180,800,"Krushak Saathi")

    c.setFont("Helvetica",12)

    c.drawString(50,760,"Profit Report")

    c.drawString(50,730,"Crop : Paddy")

    c.drawString(50,710,"Production : 50 Quintals")

    c.drawString(50,690,"Income : ₹125000")

    c.drawString(50,670,"Expense : ₹65000")

    c.drawString(50,650,"Profit : ₹60000")

    c.save()

    return send_file(
        pdf,
        as_attachment=True
    )