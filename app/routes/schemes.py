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
            "name": "PM-KISAN",
            "benefit": "₹6,000 per year",
            "eligibility": "Small and marginal farmers",
            "description": "Direct income support to eligible farmer families.",
            "apply": "https://pmkisan.gov.in/"
        },

        {
            "name": "PMFBY",
            "benefit": "Crop Insurance",
            "eligibility": "All farmers",
            "description": "Insurance against crop failure due to natural calamities.",
            "apply": "https://pmfby.gov.in/"
        },

        {
            "name": "Soil Health Card",
            "benefit": "Free Soil Testing",
            "eligibility": "All farmers",
            "description": "Provides nutrient status and fertilizer recommendations.",
            "apply": "https://soilhealth.dac.gov.in/"
        },

        {
            "name": "Kisan Credit Card",
            "benefit": "Low Interest Agricultural Loan",
            "eligibility": "Eligible farmers",
            "description": "Provides easy credit for agriculture and allied activities.",
            "apply": "https://www.myscheme.gov.in/"
        }

    ]

    return render_template(
        "schemes/index.html",
        schemes=schemes
    )