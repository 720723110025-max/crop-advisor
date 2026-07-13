"""
Authentication routes for user registration, login, and profile management.
"""

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
    jsonify,
)
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)
from datetime import datetime

from app import csrf
from app.models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()

        farm_size = request.form.get("farm_size", 0)
        farm_location = request.form.get("farm_location", "").strip()

        # Force every self-registration to be a Farmer
        role = "farmer"
        language = request.form.get("language", "en")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template(
                "register.html",
                username=username,
                email=email,
                full_name=full_name,
            )

        if User.find_by_username(username):
            flash("Username already exists.", "danger")
            return render_template(
                "register.html",
                username=username,
                email=email,
                full_name=full_name,
            )

        if User.find_by_email(email):
            flash("Email already registered.", "danger")
            return render_template(
                "register.html",
                username=username,
                email=email,
                full_name=full_name,
            )

        try:

            user = User(
                username=username,
                email=email,
                password=password,
                role=role,
                language=language,
                full_name=full_name,
                phone=phone,
                farm_size=float(farm_size) if farm_size else 0,
                farm_location=farm_location,
            )

            user.save()

            flash(
                "Registration successful! Please login.",
                "success",
            )

            return redirect(url_for("auth.login"))

        except Exception as e:

            flash(
                f"Registration failed : {e}",
                "danger",
            )

    return render_template("register.html")
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:

        if getattr(current_user, "role", "farmer") == "admin":
            return redirect(url_for("admin.dashboard"))

        elif getattr(current_user, "role", "farmer") == "expert":
            return redirect(url_for("expert.dashboard"))

        return redirect(url_for("dashboard.index"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        print("\n========== LOGIN ==========")
        print("Email:", email)

        user = User.find_by_email(email)

        print("User Found:", user)

        if user:
            print("Password Match:", user.check_password(password))

        if user and user.check_password(password):

            login_user(user, remember=remember)

            session["user_id"] = user.id

            flash(
                f"Welcome back, {user.full_name}!",
                "success"
            )

            if user.role == "admin":
                return redirect(url_for("admin.dashboard"))

            elif user.role == "expert":
                return redirect(url_for("expert.dashboard"))

            else:
                return redirect(url_for("dashboard.index"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    session.clear()

    flash(
        "You have been logged out successfully.",
        "info"
    )

    return redirect(url_for("auth.login"))
@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():

    if request.method == "POST":

        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        farm_size = request.form.get("farm_size", 0)
        farm_location = request.form.get("farm_location", "").strip()

        update_data = {
            "full_name": full_name,
            "phone": phone,
            "address": address,
            "farm_size": float(farm_size) if farm_size else 0,
            "farm_location": farm_location,
            "updated_at": datetime.utcnow(),
        }

        current_user.update(update_data)

        flash("Profile updated successfully!", "success")

        return redirect(url_for("auth.profile"))

    return render_template("profile.html", user=current_user)


@auth_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():

    current_password = request.form.get("current_password", "")
    new_password = request.form.get("new_password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not current_user.check_password(current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("auth.profile"))

    if new_password != confirm_password:
        flash("Passwords do not match.", "danger")
        return redirect(url_for("auth.profile"))

    if len(new_password) < 8:
        flash("Password must be at least 8 characters.", "danger")
        return redirect(url_for("auth.profile"))

    try:

        current_user.set_password(new_password)

        current_user.update({
            "password_hash": current_user.password_hash,
            "updated_at": datetime.utcnow()
        })

        flash("Password updated successfully!", "success")

    except Exception as e:

        flash(f"Failed : {e}", "danger")

    return redirect(url_for("auth.profile"))


@auth_bp.route("/api/user-data")
@login_required
def get_user_data():

    return jsonify(current_user.get_profile_data())


@auth_bp.route("/api/login", methods=["POST"])
@csrf.exempt
def api_login():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = User.find_by_email(email)

    if user and user.check_password(password):

        login_user(user)

        return jsonify({

            "success": True,

            "user": {

                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "is_admin": user.is_admin

            }

        })

    return jsonify({

        "success": False,
        "message": "Invalid email or password"

    }), 401