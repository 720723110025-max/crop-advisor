from flask import Blueprint, session, redirect, request

language_bp = Blueprint(
    "language",
    __name__,
    url_prefix="/language"
)

@language_bp.route("/<lang>")
def change(lang):

    session["lang"]=lang

    return redirect(
        request.referrer or "/"
    )