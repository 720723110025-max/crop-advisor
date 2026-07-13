"""
Application factory module for Crop Advisory System.
Initializes Flask app and all extensions.
"""

import os
import logging
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from app.farmer.routes import farmer_bp
from app.expert.routes import expert_bp
from app.lands.routes import lands_bp
from app.workshops.routes import workshop_bp
from app.notifications.routes import notification_bp
from app.market.routes import market_bp
from app.feedback.routes import feedback_bp
from app.crop_ai.routes import crop_ai_bp
from app.chatbot.routes import chatbot_bp
from app.routes.language import language_bp
from app.routes.main import main_bp
from app.routes.disease_ai import disease_ai_bp
from app.routes.voice import voice_bp
from app.routes.appointment import appointment_bp
from app.routes.profit import profit_bp
from app.routes.report import report_bp
from app.routes.location import location_bp
from app.routes.ussd import ussd_bp
from app.routes.settings import settings_bp
from app.routes.tasks import tasks_bp
from app.routes.diary import diary_bp
from app.routes.irrigation import irrigation_bp
from app.routes.fertilizer import fertilizer_bp
from app.routes.assistant import assistant_bp
from app.routes.analytics_dashboard import analytics_dashboard_bp
from app.routes.weather_history import weather_history_bp
from app.routes.yield_history import yield_history_bp
from app.routes.schemes import schemes_bp
from app.routes.weather import weather_bp

# Extensions
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app(config_name="default"):

    from config import config

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="static"
    )
    app.register_blueprint(farmer_bp)
    app.register_blueprint(expert_bp)
    app.register_blueprint(lands_bp)
    app.register_blueprint(workshop_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(market_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(assistant_bp)
    app.register_blueprint(analytics_dashboard_bp)
    app.register_blueprint(weather_history_bp)
    app.register_blueprint(yield_history_bp)
    app.register_blueprint(schemes_bp)
    app.register_blueprint(weather_bp)
    

    app.config.from_object(config[config_name])

    app.config["WTF_CSRF_ENABLED"] = False

    # Initialize extensions
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in first."
    login_manager.login_message_category = "info"

    # User Loader
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.find_by_id(user_id)

    # Unauthorized
    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import redirect, url_for, flash, request
        flash("Please login first.", "warning")
        return redirect(url_for("auth.login", next=request.url))

    # Register all blueprints
    register_blueprints(app)

    # Upload folder
    os.makedirs(
        app.config.get(
            "UPLOAD_FOLDER",
            "app/static/uploads"
        ),
        exist_ok=True
    )

    # MongoDB
    try:
        from app.utils.database import db_instance
        logger.info("MongoDB connection established successfully")
    except Exception as e:
        logger.error(e)

    # Context Processor
    @app.context_processor
    def utility_processor():
        from datetime import datetime
        return {
            "now": datetime.utcnow(),
            "app_name": "Crop Advisory System",
            "app_version": "1.0.0"
        }

    register_error_handlers(app)

    logger.info(
        f"Application initialized with {config_name} configuration"
    )

    return app


def register_blueprints(app):

    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.crop_recommendation import crop_bp
    from app.routes.disease_detection import disease_bp
    from app.routes.weather import weather_bp
    from app.routes.yield_prediction import yield_bp
    from app.routes.admin import admin_bp
    from app.routes.export import export_bp
    from app.routes.soil_analysis import soil_bp
    from app.routes.seed import seed_bp
    from app.routes.weather_ai import weather_ai_bp
    from app.routes.smart_notifications import smart_bp
    from app.routes.analytics import analytics_bp
    from app.routes.expert_directory import expert_directory_bp

    csrf.exempt(crop_bp)
    csrf.exempt(disease_bp)
    csrf.exempt(fertilizer_bp)
    csrf.exempt(irrigation_bp)
    csrf.exempt(yield_bp)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(main_bp)

    app.register_blueprint(crop_bp, url_prefix="/crop")
    app.register_blueprint(disease_bp, url_prefix="/disease")
    app.register_blueprint(weather_bp, url_prefix="/weather")
    app.register_blueprint(yield_bp, url_prefix="/yield")

    app.register_blueprint(fertilizer_bp)
    app.register_blueprint(irrigation_bp)

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(export_bp, url_prefix="/export")

    app.register_blueprint(soil_bp)
    app.register_blueprint(seed_bp)

    app.register_blueprint(weather_ai_bp)
    app.register_blueprint(smart_bp)
    app.register_blueprint(analytics_bp)

    app.register_blueprint(language_bp)
    app.register_blueprint(voice_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(appointment_bp)
    app.register_blueprint(profit_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(diary_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(ussd_bp)
    app.register_blueprint(crop_ai_bp)
    app.register_blueprint(disease_ai_bp)
    app.register_blueprint(expert_directory_bp)

    logger.info("All blueprints registered")


def register_error_handlers(app):

    @app.errorhandler(404)
    def not_found(error):
        from flask import render_template
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        from flask import render_template
        return render_template("errors/500.html"), 500

    @app.errorhandler(403)
    def forbidden(error):
        from flask import render_template
        return render_template("errors/403.html"), 403

    @app.errorhandler(405)
    def method_not_allowed(error):
        from flask import render_template
        return render_template("errors/405.html"), 405

    @app.errorhandler(413)
    def too_large(error):
        from flask import flash, redirect, request, url_for
        flash("File too large.", "danger")
        return redirect(
            request.referrer or url_for("dashboard.index")
        )
    
    @app.route("/about")
    def about():
      return render_template("about.html")

    logger.info("Error handlers registered")