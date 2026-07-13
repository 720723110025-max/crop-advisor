from flask import Blueprint, render_template, request, jsonify

seed_bp = Blueprint(
    "seed",
    __name__,
    url_prefix="/seed"
)

@seed_bp.route("/")
def index():
    return render_template("seed.html")


@seed_bp.route("/recommend", methods=["POST"])
def recommend():

    crop = request.form.get("crop")

    seeds = {

        "Rice":"ADT-43, CO-51, BPT-5204",

        "Maize":"COH(M)-8, NK-6240",

        "Wheat":"HD-2967, PBW-343",

        "Groundnut":"TMV-13, VRI-8"

    }

    return jsonify({

        "seed":seeds.get(crop, "No recommendation")

    })