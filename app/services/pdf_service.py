from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def create_report(filename, title, data):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph(f"<b>{title}</b>", styles["Heading1"]))

    elements.append(Paragraph("<br/>", styles["Normal"]))

    for key, value in data.items():
        elements.append(
            Paragraph(f"<b>{key}</b>: {value}", styles["Normal"])
        )

    doc.build(elements)