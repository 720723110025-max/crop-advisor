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

# Initialize extensions (without app yet)
login_manager = LoginManager()
bcrypt = Bcrypt()
csrf = CSRFProtect()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def create_app(config_name='default'):
    """
    Application factory function.

    Args:
        config_name (str): Configuration environment name

    Returns:
        Flask: Configured Flask application instance
    """
    from config import config

    # Create Flask app instance
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='static')

    # Load configuration
    app.config.from_object(config[config_name])

    # CSRF: keep enabled but exempt API endpoints below
    app.config['WTF_CSRF_ENABLED'] = True

    # Initialize extensions with app
    login_manager.init_app(app)
    bcrypt.init_app(app)
    csrf.init_app(app)

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.session_protection = 'strong'

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        """Load user by ID from MongoDB."""
        from app.models.user import User
        return User.find_by_id(user_id)

    # Unauthorized handler
    @login_manager.unauthorized_handler
    def unauthorized():
        """Handle unauthorized access."""
        from flask import flash, redirect, url_for, request
        flash('You need to be logged in to access this page.', 'warning')
        return redirect(url_for('auth.login', next=request.url))

    # Register blueprints
    register_blueprints(app)

    # Create upload directory if it doesn't exist
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'app/static/uploads'), exist_ok=True)

    # Initialize database connection (non-fatal if unavailable)
    try:
        from app.utils.database import db_instance
        logger.info("MongoDB connection established successfully")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        logger.warning("App will run but database features won't work")

    # Home redirect
    @app.route('/')
    def home():
        from flask import redirect
        return redirect('/dashboard/')

    # Add template context processors
    @app.context_processor
    def utility_processor():
        """Add utility functions to all templates."""
        from datetime import datetime
        return {
            'now': datetime.utcnow(),
            'app_name': 'Crop Advisory System',
            'app_version': '1.0.0'
        }

    # Error handlers
    register_error_handlers(app)

    logger.info(f"Application initialized with {config_name} configuration")
    return app


def register_blueprints(app):
    """
    Register all route blueprints.

    Args:
        app (Flask): Flask application instance
    """
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.crop_recommendation import crop_bp
    from app.routes.disease_detection import disease_bp
    from app.routes.fertilizer import fertilizer_bp
    from app.routes.irrigation import irrigation_bp
    from app.routes.weather import weather_bp
    from app.routes.yield_prediction import yield_bp
    from app.routes.admin import admin_bp

    # Exempt all JSON API routes from CSRF (they use login_required instead)
    from flask_wtf.csrf import CSRFProtect
    csrf.exempt(crop_bp)
    csrf.exempt(disease_bp)
    csrf.exempt(fertilizer_bp)
    csrf.exempt(irrigation_bp)
    csrf.exempt(yield_bp)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(crop_bp, url_prefix='/crop')
    app.register_blueprint(disease_bp, url_prefix='/disease')
    app.register_blueprint(fertilizer_bp, url_prefix='/fertilizer')
    app.register_blueprint(irrigation_bp, url_prefix='/irrigation')
    app.register_blueprint(weather_bp, url_prefix='/weather')
    app.register_blueprint(yield_bp, url_prefix='/yield')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    logger.info("All blueprints registered")


def register_error_handlers(app):
    """
    Register custom error handlers.

    Args:
        app (Flask): Flask application instance
    """

    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        logger.error(f"Internal Server Error: {str(error)}")
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        from flask import render_template
        return render_template('errors/403.html'), 403

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        from flask import render_template
        return render_template('errors/405.html'), 405

    @app.errorhandler(413)
    def request_entity_too_large_error(error):
        from flask import flash, redirect, url_for, request
        flash('File too large. Maximum file size is 16MB.', 'danger')
        return redirect(request.referrer or url_for('dashboard.index'))

    logger.info("Error handlers registered")
