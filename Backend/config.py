# config.py

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Secret_keyConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'xyz1023')


class DatabaseConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'trekking.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class SessionConfig:
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


class RedisConfig:
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DB = int(os.getenv('REDIS_DB', 0))
    CACHE_EXPIRY_SECONDS = 300


class CeleryConfig:
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/2')
    CELERY_TIMEZONE = 'Asia/Kolkata'


class MailConfig:
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025
    MAIL_USE_TLS = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    MAIL_DEFAULT_SENDER = 'noreply@trekkingapp.com'  


class Config(Secret_keyConfig, DatabaseConfig, SessionConfig, RedisConfig, CeleryConfig, MailConfig):
    pass