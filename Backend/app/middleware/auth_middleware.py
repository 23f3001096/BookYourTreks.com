# ============================================
# app/middleware/auth_middleware.py
# ============================================
from functools import wraps
from flask_login import current_user
from app.utils.response import error_response


def role_required(*allowed_roles):
    """Generic role gate. Use the named ones below in your routes, not this directly."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                return error_response("Login required", 401)
            if current_user.is_blocked or not current_user.is_active_flag:
                return error_response("Account is blocked or inactive", 403)
            if current_user.role.value not in allowed_roles:
                return error_response("You don't have permission to access this", 403)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def admin_required(f):
    return role_required("admin")(f)


def staff_required(f):
    return role_required("staff")(f)


def customer_required(f):
    return role_required("customer")(f)


def admin_or_staff_required(f):
    return role_required("admin", "staff")(f)