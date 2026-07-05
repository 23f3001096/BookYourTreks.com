import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Secret_keyConfig:    
    SECRET_KEY = os.getenv('SECRET_KEY', 'xyz1023')
    
class DatabaseConfig:    # Database
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'Trekking.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class SessionConfig: # session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class FileConfig: # # uploads
    
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'instance', 'uploads')
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB
    
class MailConfig: # mail
    
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Peakpath', os.getenv('MAIL_USERNAME'))
    MAIL_MAX_EMAILS = 50

class CeleryConfig:
    
     # redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

    # celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    CELERY_TIMEZONE = 'Asia/Kolkata'
    CELERY_ENABLE_UTC = False
    
class DevelopmentConfig(SessionConfig,
                        DatabaseConfig,
                        Secret_keyConfig):
    pass