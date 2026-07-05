from blueprints import auth_bp  

import os, csv, uuid
from datetime import datetime
from flask import request, current_app ,jsonify
from flask_login import current_user, logout_user, login_user, login_required

@auth_bp.route('/register', methods=['POST'])
def register():
    return jsonify({"message": "Registration endpoint"}), 200

