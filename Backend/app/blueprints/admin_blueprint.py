# ============================================
# app/blueprints/admin_blueprint.py
# ============================================
from flask import Blueprint, request
from flask_login import current_user

from app.extensions import db
from app.middleware.auth_middleware import admin_required
from app.models.user import User, RoleEnum
from app.models.staff_profile import StaffProfile, StaffStatusEnum
from app.models.customer_profile import CustomerProfile
from app.models.trek import Trek, TrekStatusEnum, DifficultyEnum
from app.models.booking import Booking, BookingStatusEnum
from app.utils.response import success_response, error_response
from app.utils.validators import (
    validate_email,
    validate_password,
    validate_required_fields,
    validate_date,
    validate_positive_int,
)
from app.tasks.notification_tasks import send_staff_welcome_email,send_trek_assignment_email


admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
@admin_required
def check_admin():
    pass


# ============================================
# DASHBOARD
# ============================================
@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        total_treks = Trek.query.count()
        total_users = User.query.filter_by(role=RoleEnum.CUSTOMER).count()
        total_staff = User.query.filter_by(role=RoleEnum.STAFF).count()
        total_bookings = Booking.query.count()

        return success_response(data={
            "total_treks": total_treks,
            "total_users": total_users,
            "total_staff": total_staff,
            "total_bookings": total_bookings,
        })
    except Exception as e:
        return error_response(f"Failed to load dashboard: {str(e)}", 500)


# ============================================
# PROFILE
# ============================================
@admin_bp.route('/profile', methods=['GET'])
def profile():
    return success_response(data=current_user.to_dict())


@admin_bp.route('/profile', methods=['PUT'])
def edit_profile():
    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body missing or invalid JSON", 400)

    try:
        if "name" in data and data["name"].strip():
            current_user.name = data["name"].strip()

        db.session.commit()
        return success_response(data=current_user.to_dict(), message="Profile updated")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Update failed: {str(e)}", 500)


# ============================================
# STAFF MANAGEMENT
# ============================================
@admin_bp.route('/staff', methods=['GET'])
def list_staff():
    try:
        staff_list = StaffProfile.query.all()
        return success_response(data=[s.to_dict() for s in staff_list])
    except Exception as e:
        return error_response(f"Failed to fetch staff: {str(e)}", 500)


@admin_bp.route('/staff/<int:staff_id>', methods=['GET'])
def view_staff_details(staff_id):
    staff = StaffProfile.query.get(staff_id)
    if not staff:
        return error_response("Staff not found", 404)
    return success_response(data=staff.to_dict())


@admin_bp.route('/staff', methods=['POST'])
def add_staff():
    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body missing or invalid JSON", 400)

    ok, err = validate_required_fields(data, ["email", "password", "name", "contact_number"])
    if not ok:
        return error_response(err, 400)

    email = data.get("email").strip().lower()
    password = data.get("password")
    name = data.get("name").strip()
    contact_number = data.get("contact_number").strip()

    ok, err = validate_email(email)
    if not ok:
        return error_response(err, 400)

    ok, err = validate_password(password)
    if not ok:
        return error_response(err, 400)

    if User.query.filter_by(email=email).first():
        return error_response("Email already registered", 409)

    try:
        new_staff_user = User(
            email=email,
            name=name,
            role=RoleEnum.STAFF,
            active=True,
            blocked=False,
        )
        new_staff_user.set_password(password)
        db.session.add(new_staff_user)
        db.session.flush()   # taaki new_staff_user.id mil jaye commit se pehle

        staff_profile = StaffProfile(
            user_id=new_staff_user.id,
            contact_number=contact_number,
            status=StaffStatusEnum.ACTIVE,
        )
        db.session.add(staff_profile)
        db.session.commit()
        
        send_staff_welcome_email.delay(email, name, password)

        return success_response(data=staff_profile.to_dict(), message="Staff added successfully", status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to add staff: {str(e)}", 500)


@admin_bp.route('/staff/<int:staff_id>', methods=['DELETE'])
def remove_staff():
    staff = StaffProfile.query.get(staff_id)
    if not staff:
        return error_response("Staff not found", 404)

    try:
        # trek se unassign kar de pehle taaki orphan reference na bache
        for trek in staff.treks:
            trek.assigned_staff_id = None

        db.session.delete(staff.user)   # user delete hone se staff_profile bhi cascade nahi hoga automatically, isliye dono delete
        db.session.delete(staff)
        db.session.commit()
        return success_response(message="Staff removed successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to remove staff: {str(e)}", 500)


@admin_bp.route('/staff/<int:staff_id>/assign-trek', methods=['POST'])
def assign_staff_to_trek(staff_id):
    data = request.get_json(silent=True)
    if not data or "trek_id" not in data:
        return error_response("trek_id is required", 400)

    staff = StaffProfile.query.get(staff_id)
    if not staff:
        return error_response("Staff not found", 404)

    if staff.is_blocked():
        return error_response("Cannot assign trek to a blocked staff", 403)

    trek = Trek.query.get(data["trek_id"])
    if not trek:
        return error_response("Trek not found", 404)

    try:
        trek.assigned_staff_id = staff.id
        db.session.commit()
        send_trek_assignment_email.delay(
                                        staff.user.email,
                                        staff.user.name,
                                        trek.name,
                                        trek.location,
                                        trek.start_date.strftime('%Y-%m-%d')
                                    )
        return success_response(data=trek.to_dict(), message="Staff assigned to trek successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to assign staff: {str(e)}", 500)


# ============================================
# USERS MANAGEMENT
# ============================================
@admin_bp.route('/users', methods=['GET'])
def list_users():
    try:
        users = User.query.filter_by(role=RoleEnum.CUSTOMER).all()
        return success_response(data=[u.to_dict() for u in users])
    except Exception as e:
        return error_response(f"Failed to fetch users: {str(e)}", 500)


@admin_bp.route('/users/<int:user_id>', methods=['GET'])
def view_user_details(user_id):
    user = User.query.get(user_id)
    if not user or user.role != RoleEnum.CUSTOMER:
        return error_response("User not found", 404)
    return success_response(data=user.to_dict())


# ============================================
# BLOCK / ACTIVATE — Users
# ============================================
@admin_bp.route('/users/<int:user_id>/blocklist', methods=['POST'])
def blocklist_user(user_id):
    user = User.query.get(user_id)
    if not user or user.role != RoleEnum.CUSTOMER:
        return error_response("User not found", 404)

    try:
        user.block()
        return success_response(data=user.to_dict(), message="User blocked successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to block user: {str(e)}", 500)


@admin_bp.route('/users/<int:user_id>/activate', methods=['POST'])
def active_user(user_id):
    user = User.query.get(user_id)
    if not user or user.role != RoleEnum.CUSTOMER:
        return error_response("User not found", 404)

    try:
        user.unblock()
        user.activate()
        return success_response(data=user.to_dict(), message="User activated successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to activate user: {str(e)}", 500)


# ============================================
# BLOCK / ACTIVATE — Staff
# ============================================
@admin_bp.route('/staff/<int:staff_id>/blocklist', methods=['POST'])
def blocklist_staff(staff_id):
    staff = StaffProfile.query.get(staff_id)
    if not staff:
        return error_response("Staff not found", 404)

    try:
        staff.block()
        return success_response(data=staff.to_dict(), message="Staff blocked successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to block staff: {str(e)}", 500)


@admin_bp.route('/staff/<int:staff_id>/activate', methods=['POST'])
def activate_staff(staff_id):
    staff = StaffProfile.query.get(staff_id)
    if not staff:
        return error_response("Staff not found", 404)

    try:
        staff.unblock()
        return success_response(data=staff.to_dict(), message="Staff activated successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to activate staff: {str(e)}", 500)


# ============================================
# SEARCH
# ============================================
@admin_bp.route('/staff/search', methods=['GET'])
def search_staff():
    query = request.args.get('q', '').strip()
    if not query:
        return error_response("Search query 'q' is required", 400)

    try:
        results = StaffProfile.query.join(User).filter(
            db.or_(
                User.name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%"),
            )
        ).all()
        return success_response(data=[s.to_dict() for s in results])
    except Exception as e:
        return error_response(f"Search failed: {str(e)}", 500)


@admin_bp.route('/users/search', methods=['GET'])
def search_trekkers():
    query = request.args.get('q', '').strip()
    if not query:
        return error_response("Search query 'q' is required", 400)

    try:
        results = User.query.filter(
            User.role == RoleEnum.CUSTOMER,
            db.or_(
                User.name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%"),
            )
        ).all()
        return success_response(data=[u.to_dict() for u in results])
    except Exception as e:
        return error_response(f"Search failed: {str(e)}", 500)


# ============================================
# TREK MANAGEMENT
# ============================================
@admin_bp.route('/treks', methods=['GET'])
def list_treks():
    try:
        treks = Trek.query.all()
        return success_response(data=[t.to_dict() for t in treks])
    except Exception as e:
        return error_response(f"Failed to fetch treks: {str(e)}", 500)


@admin_bp.route('/treks', methods=['POST'])
def create_trek():
    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body missing or invalid JSON", 400)

    required = ["name", "location", "difficulty", "duration_days", "available_slots", "start_date", "end_date"]
    ok, err = validate_required_fields(data, required)
    if not ok:
        return error_response(err, 400)

    # difficulty enum check
    difficulty_value = data.get("difficulty").strip().lower()
    if difficulty_value not in [d.value for d in DifficultyEnum]:
        return error_response(f"Invalid difficulty. Must be one of {[d.value for d in DifficultyEnum]}", 400)

    # duration + slots validation
    duration, err = validate_positive_int(data.get("duration_days"), "duration_days")
    if err:
        return error_response(err, 400)

    slots, err = validate_positive_int(data.get("available_slots"), "available_slots")
    if err:
        return error_response(err, 400)

    # date validation
    start_date, err = validate_date(data.get("start_date"))
    if err:
        return error_response(err, 400)

    end_date, err = validate_date(data.get("end_date"))
    if err:
        return error_response(err, 400)

    if end_date < start_date:
        return error_response("end_date cannot be before start_date", 400)

    expected_duration = (end_date - start_date).days
    if expected_duration != duration:
        return error_response(
            f"Duration mismatch: dates suggest {expected_duration} days, but duration_days is {duration}",
            400
        )

    try:
        trek = Trek(
            name=data.get("name").strip(),
            location=data.get("location").strip(),
            difficulty=DifficultyEnum(difficulty_value),
            duration_days=duration,
            available_slots=slots,
            status=TrekStatusEnum.PENDING,
            start_date=start_date,
            end_date=end_date,
        )
        db.session.add(trek)
        db.session.commit()
        return success_response(data=trek.to_dict(), message="Trek created successfully", status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to create trek: {str(e)}", 500)


@admin_bp.route('/treks/<int:trek_id>', methods=['GET'])
def view_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return error_response("Trek not found", 404)
    return success_response(data=trek.to_dict())


@admin_bp.route('/treks/<int:trek_id>', methods=['PUT'])
def edit_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return error_response("Trek not found", 404)

    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body missing or invalid JSON", 400)

    try:
        if "name" in data and data["name"].strip():
            trek.name = data["name"].strip()

        if "location" in data and data["location"].strip():
            trek.location = data["location"].strip()

        if "difficulty" in data:
            difficulty_value = data["difficulty"].strip().lower()
            if difficulty_value not in [d.value for d in DifficultyEnum]:
                return error_response(f"Invalid difficulty. Must be one of {[d.value for d in DifficultyEnum]}", 400)
            trek.difficulty = DifficultyEnum(difficulty_value)

        if "duration_days" in data:
            duration, err = validate_positive_int(data["duration_days"], "duration_days")
            if err:
                return error_response(err, 400)
            trek.duration_days = duration

        if "available_slots" in data:
            slots, err = validate_positive_int(data["available_slots"], "available_slots")
            if err:
                return error_response(err, 400)
            trek.available_slots = slots
        
        if "start_date" in data and "end_date" in data:
            if trek.end_date < trek.start_date:
                return error_response("end_date cannot be before start_date", 400)
            expected_duration = (trek.end_date - trek.start_date).days
            if expected_duration != trek.duration_days:
                return error_response(
                    f"Duration mismatch: dates suggest {expected_duration} days, but duration_days is {trek.duration_days}",
                    400
                )

        db.session.commit()
        return success_response(data=trek.to_dict(), message="Trek updated successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to update trek: {str(e)}", 500)


@admin_bp.route('/treks/<int:trek_id>', methods=['DELETE'])
def delete_trek(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return error_response("Trek not found", 404)

    try:
        db.session.delete(trek)
        db.session.commit()
        return success_response(message="Trek deleted successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to delete trek: {str(e)}", 500)


@admin_bp.route('/treks/<int:trek_id>/status', methods=['PATCH'])
def update_trek_status(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return error_response("Trek not found", 404)

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


@admin_bp.route('/treks/search', methods=['GET'])
def search_trek():
    query = request.args.get('q', '').strip()
    location = request.args.get('location', '').strip()
    difficulty = request.args.get('difficulty', '').strip()

    try:
        filters = []
        if query:
            filters.append(Trek.name.ilike(f"%{query}%"))
        if location:
            filters.append(Trek.location.ilike(f"%{location}%"))
        if difficulty:
            filters.append(Trek.difficulty == DifficultyEnum(difficulty.lower()))

        results = Trek.query.filter(*filters).all() if filters else Trek.query.all()
        return success_response(data=[t.to_dict() for t in results])
    except Exception as e:
        return error_response(f"Search failed: {str(e)}", 500)


@admin_bp.route('/treks/<int:trek_id>/trekkers', methods=['GET'])
def trekkers(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return error_response("Trek not found", 404)

    bookings = Booking.query.filter_by(trek_id=trek_id).all()
    return success_response(data=[b.to_dict() for b in bookings])


# ============================================
# BOOKINGS
# ============================================
@admin_bp.route('/bookings', methods=['GET'])
def bookings():
    try:
        all_bookings = Booking.query.all()
        return success_response(data=[b.to_dict() for b in all_bookings])
    except Exception as e:
        return error_response(f"Failed to fetch bookings: {str(e)}", 500)


# ============================================
# STATS / REPORTS
# ============================================
@admin_bp.route('/stats', methods=['GET'])
def stats():
    try:
        total_treks = Trek.query.count()
        open_treks = Trek.query.filter_by(status=TrekStatusEnum.OPEN).count()
        completed_treks = Trek.query.filter_by(status=TrekStatusEnum.COMPLETED).count()
        total_bookings = Booking.query.count()
        cancelled_bookings = Booking.query.filter_by(status=BookingStatusEnum.CANCELLED).count()
        total_customers = User.query.filter_by(role=RoleEnum.CUSTOMER).count()
        total_staff = User.query.filter_by(role=RoleEnum.STAFF).count()

        return success_response(data={
            "total_treks": total_treks,
            "open_treks": open_treks,
            "completed_treks": completed_treks,
            "total_bookings": total_bookings,
            "cancelled_bookings": cancelled_bookings,
            "total_customers": total_customers,
            "total_staff": total_staff,
        })
    except Exception as e:
        return error_response(f"Failed to load stats: {str(e)}", 500)