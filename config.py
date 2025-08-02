import os

class BaseConfig:
    """Global settings shared by all environments"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Tneconni1.oibaf'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SECURE = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'images')
    ENABLE_SEARCH = True  # Custom flag for autocomplete & global search

class DevelopmentConfig(BaseConfig):
    """Settings for development mode"""
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///fallback.db')

class ProductionConfig(BaseConfig):
    """Settings for production mode"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///buxxel_prod.db'
    ENV = 'production'
    ENABLE_SEARCH = False  # Toggle based on performance and infra
    SESSION_COOKIE_SECURE = True
