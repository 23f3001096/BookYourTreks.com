# ============================================
# app/blueprints/staff_blueprint.py
# ============================================
from flask import Blueprint, request
from flask_login import current_user

from app.extensions import db
from app.middleware.auth_middleware import staff_required
from app.models.trek import Trek, TrekStatusEnum
from app.models.staff_profile import StaffProfile
from app.models.booking import Booking, BookingStatusEnum
from app.utils.response import success_response, error_response
from app.utils.validators import validate_positive_int

staff_bp = Blueprint('staff', __name__)


@staff_bp.before_request
@staff_required
def check_staff():
    pass


def _get_current_staff_profile():
    """Helper — current_user (User) se uska StaffProfile nikalta hai."""
    return StaffProfile.query.filter_by(user_id=current_user.id).first()


# ============================================
# DASHBOARD
# ============================================
@staff_bp.route('/dashboard', methods=['GET'])
def dashboard():
    staff = _get_current_staff_profile()
    if not staff:
        return error_response("Staff profile not found", 404)

    try:
        assigned_treks = Trek.query.filter_by(assigned_staff_id=staff.id).all()
        total_registered_users = sum(t.registered_users_count() for t in assigned_treks)

        return success_response(data={
            "assigned_treks_count": len(assigned_treks),
            "total_registered_users": total_registered_users,
            "treks": [t.to_dict() for t in assigned_treks],
        })
    except Exception as e:
        return error_response(f"Failed to load dashboard: {str(e)}", 500)


# ============================================
# PROFILE
# ============================================
@staff_bp.route('/profile', methods=['GET'])
def profile():
    staff = _get_current_staff_profile()
    if not staff:
        return error_response("Staff profile not found", 404)
    return success_response(data=staff.to_dict())


@staff_bp.route('/profile', methods=['PUT'])
def edit_profile():
    staff = _get_current_staff_profile()
    if not staff:
        return error_response("Staff profile not found", 404)

    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body missing or invalid JSON", 400)

    try:
        if "name" in data and data["name"].strip():
            current_user.name = data["name"].strip()   # <-- User table pe update

        if "contact_number" in data and data["contact_number"].strip():
            staff.contact_number = data["contact_number"].strip()  # <-- StaffProfile table pe update

        db.session.commit()
        return success_response(data=staff.to_dict(), message="Profile updated")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Update failed: {str(e)}", 500)


# ============================================
# ASSIGNED TREKS
# ============================================
@staff_bp.route('/treks', methods=['GET'])
def assigned_treks():
    staff = _get_current_staff_profile()
    if not staff:
        return error_response("Staff profile not found", 404)

    try:
        treks = Trek.query.filter_by(assigned_staff_id=staff.id).all()
        return success_response(data=[t.to_dict() for t in treks])
    except Exception as e:
        return error_response(f"Failed to fetch treks: {str(e)}", 500)


def _get_owned_trek_or_error(trek_id, staff):
    trek = Trek.query.get(trek_id)
    if not trek:
        return None, error_response("Trek not found", 404)
    if trek.assigned_staff_id != staff.id:
        return None, error_response("You are not assigned to this trek", 403)
    return trek, None


@staff_bp.route('/treks/<int:trek_id>', methods=['GET'])
def view_trek(trek_id):
    staff = _get_current_staff_profile()
    if not staff:
        return error_response("Staff profile not found", 404)

    trek, err = _get_owned_trek_or_error(trek_id, staff)
    if err:
        return err

    return success_response(data=trek.to_dict())


@staff_bp.route('/treks/<int:trek_id>/slots', methods=['PUT'])
def update_slots(trek_id):
    staff = _get_current_staff_profile()
    if not staff:
        return error_response("Staff profile not found", 404)

    trek, err = _get_owned_trek_or_error(trek_id, staff)
    if err:
        return err

    if trek.status == TrekStatusEnum.COMPLETED:
        return error_response("This trek is already completed and cannot be modified. Contact admin for changes.", 403)

    data = request.get_json(silent=True)
    if not data or "available_slots" not in data:
        return error_response("available_slots is required", 400)

    slots, verr = validate_positive_int(data["available_slots"], "available_slots")
    if verr:
        return error_response(verr, 400)

    try:
        trek.available_slots = slots
        db.session.commit()
        return success_response(data=trek.to_dict(), message="Slots updated successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to update slots: {str(e)}", 500)
    
@staff_bp.route('/treks/<int:trek_id>/status', methods=['PUT'])
def update_status(trek_id):
    staff = _get_current_staff_profile()
    if not staff:
        return error_response("Staff profile not found", 404)

    trek, err = _get_owned_trek_or_error(trek_id, staff)
    if err:
        return err

    if trek.status == TrekStatusEnum.COMPLETED:
        return error_response("This trek is already completed and cannot be modified. Contact admin for changes.", 403)

    data = request.get_json(silent=True)
    if not data or "status" not in data:
        return error_response("status is required", 400)

    status_value = data["status"].strip().lower()
    if status_value not in [s.value for s in TrekStatusEnum]:
        return error_response(f"Invalid status. Must be one of {[s.value for s in TrekStatusEnum]}", 400)

    try:
        trek.status = TrekStatusEnum(status_value)
        db.session.commit()
        return success_response(data=trek.to_dict(), message="Trek status updated")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to update status: {str(e)}", 500)


@staff_bp.route('/treks/<int:trek_id>/trekkers', methods=['GET'])
def view_trekkers(trek_id):
    staff = _get_current_staff_profile()
    if not staff:
        return error_response("Staff profile not found", 404)

    trek, err = _get_owned_trek_or_error(trek_id, staff)
    if err:
        return err

    bookings = Booking.query.filter_by(trek_id=trek_id, status=BookingStatusEnum.BOOKED).all()
    return success_response(data=[b.to_dict() for b in bookings])


@staff_bp.route('/treks/<int:trek_id>/start', methods=['POST'])
def mark_trek_started(trek_id):
    staff = _get_current_staff_profile()
    if not staff:
        return error_response("Staff profile not found", 404)

    trek, err = _get_owned_trek_or_error(trek_id, staff)
    if err:
        return err

    if trek.status == TrekStatusEnum.COMPLETED:
        return error_response("This trek is already completed and cannot be modified.", 403)

    try:
        trek.mark_started()
        return success_response(data=trek.to_dict(), message="Trek marked as started")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to mark trek started: {str(e)}", 500)


@staff_bp.route('/treks/<int:trek_id>/complete', methods=['POST'])
def mark_completed_trek(trek_id):
    staff = _get_current_staff_profile()
    if not staff:
        return error_response("Staff profile not found", 404)

    trek, err = _get_owned_trek_or_error(trek_id, staff)
    if err:
        return err

    if trek.status == TrekStatusEnum.COMPLETED:
        return error_response("This trek is already marked as completed.", 400)

    try:
        trek.mark_completed()
        active_bookings = Booking.query.filter_by(trek_id=trek_id, status=BookingStatusEnum.BOOKED).all()
        for b in active_bookings:
            b.status = BookingStatusEnum.COMPLETED
        db.session.commit()
        return success_response(data=trek.to_dict(), message="Trek marked as completed")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to mark trek completed: {str(e)}", 500)