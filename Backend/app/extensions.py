from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from redis import Redis
from flask_cors import CORS
from flask_mail import Mail
from celery import Celery


db =  SQLAlchemy()

login_manager = LoginManager()

mail = Mail()

cors = CORS()

celery =  Celery()

