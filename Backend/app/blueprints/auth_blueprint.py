# auth_blueprint.py

from blueprints import auth_bp

import os, csv, uuid
from datetime import datetime
from flask import request, current_app, jsonify
from flask_login import current_user, logout_user, login_user, login_required, current_user


@auth_bp.route('/register', methods=['POST'])
def register():
    pass

@auth_bp.route('/login', methods=['POST'])
def login():
    pass

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    pass

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    pass