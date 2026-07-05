from flask import Blueprint

# Auth Blueprint for Authentications apis
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Admin relateed Apis
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

#  Staff related Apis
staff_bp = Blueprint('admin', __name__, url_prefix='/api/staff')

# customer related Apis
customer_bp = Blueprint('customer', __name__, url_prefix='/api/customer')


