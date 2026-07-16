from flask import Blueprint

mail_bp = Blueprint(
    "mail",
    __name__,
    url_prefix="/mail"
)

@mail_bp.route("/")
def index():
    return "Mail Module Working"