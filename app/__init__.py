"""
Application Factory
"""

import os
import logging

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from app.routes.notifications import notifications_bp

mail = Mail()
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def create_app(config_name="default"):
    def register_blueprints(app):

        # Feature Modules
        from app.farmer.routes import farmer_bp
        from app.expert.routes import expert_bp
        from app.lands.routes import lands_bp
        from app.workshops.routes import workshop_bp
        from app.market.routes import market_bp
        from app.feedback.routes import feedback_bp
        from app.crop_ai.routes import crop_ai_bp
        from app.chatbot.routes import chatbot_bp
        from app.routes.main import main_bp
        from app.routes.auth import auth_bp
        from app.routes.dashboard import dashboard_bp
        from app.routes.admin import admin_bp
        from app.routes.crop_recommendation import crop_bp
        from app.routes.disease_detection import disease_bp
        from app.routes.weather import weather_bp
        from app.routes.yield_prediction import yield_bp
        from app.routes.language import language_bp
        from app.routes.voice import voice_bp
        from app.routes.location import location_bp
        from app.routes.appointment import appointment_bp
        from app.routes.profit import profit_bp
        from app.routes.report import report_bp
        from app.routes.ussd import ussd_bp
        from app.routes.settings import settings_bp
        from app.routes.tasks import tasks_bp
        from app.routes.diary import diary_bp
        from app.routes.fertilizer import fertilizer_bp
        from app.routes.irrigation import irrigation_bp
        from app.routes.analytics import analytics_bp
        from app.routes.analytics_dashboard import analytics_dashboard_bp
        from app.routes.weather_history import weather_history_bp
        from app.routes.yield_history import yield_history_bp
        from app.routes.weather_ai import weather_ai_bp
        from app.routes.schemes import schemes_bp
        from app.routes.assistant import assistant_bp
        from app.routes.seed import seed_bp
        from app.routes.soil import soil_bp
        from app.routes.export import export_bp
        from app.routes.expert_directory import expert_directory_bp
        from app.routes.disease_ai import disease_ai_bp
        from app.routes.mail import mail_bp
        from app.routes.expense import expense_bp
        from app.routes.calendar import calendar_bp

        # Disable CSRF for AI APIs
        csrf.exempt(crop_bp)
        csrf.exempt(disease_bp)
        csrf.exempt(fertilizer_bp)
        csrf.exempt(irrigation_bp)
        csrf.exempt(yield_bp)

        # Register Blueprints (REGISTER EACH ONLY ONCE)

        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(farmer_bp)
        app.register_blueprint(expert_bp)
        app.register_blueprint(lands_bp)
        app.register_blueprint(workshop_bp)
        app.register_blueprint(market_bp)
        app.register_blueprint(feedback_bp)
        app.register_blueprint(crop_bp, url_prefix="/crop")
        app.register_blueprint(disease_bp, url_prefix="/disease")
        app.register_blueprint(weather_bp, url_prefix="/weather")
        app.register_blueprint(yield_bp, url_prefix="/yield")
        app.register_blueprint(fertilizer_bp)
        app.register_blueprint(irrigation_bp)
        app.register_blueprint(seed_bp)
        app.register_blueprint(soil_bp)
        app.register_blueprint(weather_ai_bp)
        app.register_blueprint(crop_ai_bp)
        app.register_blueprint(disease_ai_bp)
        app.register_blueprint(language_bp, url_prefix="/language")
        app.register_blueprint(voice_bp, url_prefix="/voice")
        app.register_blueprint(location_bp, url_prefix="/location")
        app.register_blueprint(appointment_bp)
        app.register_blueprint(profit_bp, url_prefix="/profit")
        app.register_blueprint(report_bp)
        app.register_blueprint(ussd_bp)
        app.register_blueprint(settings_bp)
        app.register_blueprint(tasks_bp)
        app.register_blueprint(diary_bp)
        app.register_blueprint(chatbot_bp)
        app.register_blueprint(export_bp)
        app.register_blueprint(assistant_bp)
        app.register_blueprint(weather_history_bp)
        app.register_blueprint(yield_history_bp)
        app.register_blueprint(analytics_bp)
        app.register_blueprint(analytics_dashboard_bp)
        app.register_blueprint(schemes_bp)
        app.register_blueprint(expert_directory_bp)
        app.register_blueprint(expense_bp)
        app.register_blueprint(calendar_bp)
        app.register_blueprint(notifications_bp)



    logger.info("All blueprints registered")

    from config import config

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="static"
    )

    app.config.from_object(config[config_name])
    app.config["WTF_CSRF_ENABLED"] = False

    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login first."

    register_blueprints(app)
    register_error_handlers(app)

    os.makedirs(
        app.config.get(
            "UPLOAD_FOLDER",
            "app/static/uploads"
        ),
        exist_ok=True
    )

    return app
@login_manager.user_loader
def load_user(user_id):

    from app.models.user import User

    return User.find_by_id(user_id)


def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(405)
    def method_not_allowed(error):
        return render_template("errors/405.html"), 405

    @app.errorhandler(413)
    def file_too_large(error):

        from flask import flash, redirect, request

        flash("Uploaded file is too large.", "danger")

        return redirect(request.referrer or "/")

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("errors/500.html"), 500

    @app.route("/")
    def home():

        from flask import redirect, url_for

        return redirect(url_for("dashboard.index"))

    @app.route("/about")
    def about():
        return render_template("about.html")

    logger.info("Error handlers registered")