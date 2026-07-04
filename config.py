"""
Configuration module for the Crop Advisory System.
All secrets must be provided via environment variables — never hard-coded.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # Security — MUST be set in production via env var
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False

    # MongoDB — set MONGO_URI in environment for production
    MONGO_URI = os.environ.get('MONGO_URI', '')
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'crop_advisory_db')

    # File uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'app/static/uploads')
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16777216))  # 16 MB

    # External APIs — optional; app falls back gracefully if missing
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')

    PERMANENT_SESSION_LIFETIME = 3600
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    MONGO_DB_NAME = 'crop_advisory_test'
    WTF_CSRF_ENABLED = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
