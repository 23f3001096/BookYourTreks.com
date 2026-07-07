# ============================================
# app/utils/response.py
# ============================================
from flask import jsonify


def success_response(data=None, message="Success", status_code=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status_code


def error_response(message="Something went wrong", status_code=400, errors=None):
    return jsonify({
        "success": False,
        "message": message,
        "errors": errors
    }), status_code