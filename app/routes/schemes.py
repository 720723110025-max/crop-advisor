from flask import Blueprint, render_template

schemes_bp = Blueprint(
    "schemes",
    __name__,
    url_prefix="/schemes"
)


@schemes_bp.route("/")
def index():

    schemes = [

        {
            "name":"PM-KISAN",
            "benefit":"₹6000/year",
            "description":"Income support for farmers"
        },

        {
            "name":"PMFBY",
            "benefit":"Crop Insurance",
            "description":"Insurance against crop loss"
        },

        {
            "name":"Soil Health Card",
            "benefit":"Free Soil Testing",
            "description":"Provides soil nutrient information"
        },

        {
            "name":"Kisan Credit Card",
            "benefit":"Low Interest Loan",
            "description":"Easy agricultural loans"
        }

    ]

    return render_template(
        "schemes/index.html",
        schemes=schemes
    )