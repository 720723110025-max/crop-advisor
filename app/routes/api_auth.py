from flask import Blueprint, request, jsonify
from flask_login import login_user
from app.models.user import User

api_auth = Blueprint("api_auth", __name__)

@api_auth.route("/api/login", methods=["POST"])
def api_login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.find_by_username(username)

    if user and user.check_password(password):

        login_user(user)

        return jsonify({
            "success": True,
            "user": {
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email
            }
        })

    return jsonify({
        "success": False,
        "message": "Invalid username or password"
    }), 401