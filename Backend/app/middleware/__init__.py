# ============================================
# app/middleware/__init__.py
# ============================================
from app.middleware.auth_middleware import (
    admin_required,
    staff_required,
    customer_required,
    admin_or_staff_required,
    role_required,
)