# app/__init__.py

from flask import Flask
from app.extensions import db, login_manager
from config import DevelopmentConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.models import create_tables
        create_tables()          

    return app
