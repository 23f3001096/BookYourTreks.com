# app/__init__.py

from flask import Flask
import redis

from app.extensions import db, login_manager, mail
import app.extensions as extensions
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ---------- Init extensions ----------
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # ---------- Init Redis ----------
    extensions.redis_client = redis.Redis(
        host=app.config['REDIS_HOST'],
        port=app.config['REDIS_PORT'],
        db=app.config['REDIS_DB'],
        decode_responses=True
    )

    # ---------- Init Celery ----------
    from app.celery_app import init_celery
    init_celery(app)

    # ---------- Flask-Login config ----------
    login_manager.login_view = None
    login_manager.session_protection = "strong"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        from app.utils.response import error_response
        return error_response("Login required", 401)

    # ---------- Register blueprints ----------
    from app.blueprints import admin_bp, auth_bp, staff_bp, customer_bp, review_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(staff_bp, url_prefix='/api/staff')
    app.register_blueprint(customer_bp, url_prefix='/api/customer')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')

    # ---------- Create DB tables + seed admin ----------
    with app.app_context():
        from app.models import create_tables
        create_tables()

    return app