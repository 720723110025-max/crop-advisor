from flask import Blueprint, render_template
from app.models.expert import ExpertModel

expert_directory_bp = Blueprint(
    "expert_directory",
    __name__,
    url_prefix="/experts"
)

expert_model = ExpertModel()


@expert_directory_bp.route("/")
def index():

    experts = expert_model.get_all()

    return render_template(
        "experts/index.html",
        experts=experts
    )