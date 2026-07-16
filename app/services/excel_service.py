from openpyxl import Workbook


def create_excel(filename, reports):

    wb = Workbook()

    ws = wb.active

    ws.title = "Disease Reports"

    ws.append([
        "Crop",
        "Disease",
        "Confidence",
        "Severity",
        "Treatment",
        "Date"
    ])

    for report in reports:

        ws.append([

            report.get("crop_type", ""),

            report.get("disease_name", ""),

            report.get("confidence", ""),

            report.get("severity", ""),

            report.get("treatment", ""),

            str(report.get("created_at", ""))

        ])

    wb.save(filename)