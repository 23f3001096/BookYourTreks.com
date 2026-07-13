# ============================================
# app/blueprints/auth_blueprint.py
# ============================================
from flask import Blueprint, request ,session
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db
from app.models.user import User, RoleEnum
from app.models.customer_profile import CustomerProfile
from app.utils.response import success_response, error_response
from app.utils.validators import (
    validate_email,
    validate_password,
    validate_required_fields,
)

auth_bp = Blueprint('auth', __name__)


# ============================================
# REGISTER — sirf customer ke liye, admin/staff yaha se nahi ban sakte
# ============================================
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body missing or invalid JSON", 400)

    # required fields check
    ok, err = validate_required_fields(data, ["email", "password", "name"])
    if not ok:
        return error_response(err, 400)

    email = data.get("email").strip().lower()
    password = data.get("password")
    name = data.get("name").strip()
    contact_number = data.get("contact_number")          # optional
    emergency_contact = data.get("emergency_contact")     # optional

    # email format check
    ok, err = validate_email(email)
    if not ok:
        return error_response(err, 400)

    # password strength check
    ok, err = validate_password(password)
    if not ok:
        return error_response(err, 400)

    # duplicate email check
    if User.query.filter_by(email=email).first():
        return error_response("Email already registered", 409)

    try:
        # create user with role=customer (default anyway, but explicit is safer)
        new_user = User(
            email=email,
            name=name,
            role=RoleEnum.CUSTOMER,
            active=True,
            blocked=False,
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()   # taaki new_user.id mil jaye commit se pehle

        # customer profile linked to this user
        profile = CustomerProfile(
            user_id=new_user.id,
            contact_number=contact_number,
            emergency_contact=emergency_contact,
        )
        db.session.add(profile)
        db.session.commit()

        return success_response(
            data=new_user.to_dict(),
            message="Registration successful",
            status_code=201
        )

    except Exception as e:
        db.session.rollback()
        return error_response(f"Registration failed: {str(e)}", 500)


# ============================================
# LOGIN — Admin, Staff, Customer sab isi se login karenge
# ============================================
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body missing or invalid JSON", 400)

    ok, err = validate_required_fields(data, ["email", "password"])
    if not ok:
        return error_response(err, 400)

    email = data.get("email").strip().lower()
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    # generic message — batana nahi chahiye email exist karta hai ya nahi (security)
    if not user or not user.check_password(password):
        return error_response("Invalid email or password", 401)

    if user.blocked:
        return error_response("Your account has been blocked. Contact admin.", 403)

    if not user.active:
        return error_response("Your account is deactivated. Contact admin.", 403)

    login_user(user, remember=True)
    session.permanent = True

    return success_response(
        data=user.to_dict(),
        message="Login successful"
    )


# ============================================
# LOGOUT
# ============================================
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return success_response(message="Logged out successfully")


# ============================================
# GET CURRENT USER — "who am I" check, frontend session restore ke liye
# ============================================
@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    print(request.remote_addr,"---------------------------------------------------------")
    return success_response(data=current_user.to_dict())