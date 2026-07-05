from flask import Flask 
from .extensions import db , login_manager ,mail 

from blueprints import auth_bp ,admin_bp ,staff_bp  ,customer_bp
from config import DevelopmentConfig



def Create_app():
    
    # Creating Flask application instance
    app = Flask(__name__)
    
    # App configuration
    app.config.from_object(DevelopmentConfig)
    
    # register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(customer_bp)
    
    
    
    
    
    return app