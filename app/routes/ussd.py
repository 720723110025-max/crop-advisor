from flask import Blueprint, request

ussd_bp = Blueprint(
    "ussd",
    __name__,
    url_prefix="/ussd"
)


@ussd_bp.route("/", methods=["POST"])
def menu():

    text = request.form.get("text", "")

    if text == "":

        return """CON Welcome to Krushak Saathi

1. Crop Advice

2. Market Price

3. Weather

4. Workshops

5. Expert Call
"""

    elif text == "1":

        return "END Paddy is recommended for your area."

    elif text == "2":

        return "END Paddy Price ₹2450 / Quintal"

    elif text == "3":

        return "END Heavy Rain Expected Tomorrow"

    elif text == "4":

        return "END Organic Farming Workshop on Sunday"

    elif text == "5":

        return "END Expert will contact you shortly."

    return "END Invalid Choice"