import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-this'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'linkup.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')

    # App settings
    APP_NAME = "Link-Up"
    APP_VERSION = "1.0.0"

    # Categories
    MARKETPLACE_CATEGORIES = [
        'cars', 'electronics', 'fashion', 'home', 'books',
        'sports', 'cosmetics', 'other'
    ]

    SERVICE_CATEGORIES = [
        'gym', 'massage', 'tutoring', 'repair', 'cleaning',
        'beauty', 'fitness', 'consulting', 'other'
    ]