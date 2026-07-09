from flask import Blueprint, session, redirect, request, render_template

language_bp = Blueprint(
    "language",
    __name__,
    url_prefix="/language"
)


@language_bp.route("/")
def select_language():
    return render_template("language.html")


@language_bp.route("/<lang>")
def set_language(lang):

    if lang not in ["en", "od"]:
        lang = "en"

    session["lang"] = lang

    return redirect(request.args.get("next") or "/")