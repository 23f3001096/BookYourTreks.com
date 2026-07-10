# app/utils/validators.py

import re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def validate_email(email):
    if not email or not EMAIL_REGEX.match(email):
        return False, "Invalid email format"
    return True, None


def validate_password(password, min_len=6):
    if not password or len(password) < min_len:
        return False, f"Password must be at least {min_len} characters"
    return True, None


def validate_required_fields(data: dict, required_fields: list):
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None


def validate_date(date_str, fmt="%Y-%m-%d"):
    try:
        return datetime.strptime(date_str, fmt).date(), None
    except (ValueError, TypeError):
        return None, "Invalid date format, expected YYYY-MM-DD"


def validate_positive_int(value, field_name="value"):
    try:
        value = int(value)
        if value < 0:
            return None, f"{field_name} must be a positive number"
        return value, None
    except (ValueError, TypeError):
        return None, f"{field_name} must be a valid integer"