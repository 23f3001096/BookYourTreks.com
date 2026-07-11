# ============================================
# app/blueprints/customer_blueprint.py
# ============================================
from flask import Blueprint, request
from flask_login import current_user

from app.extensions import db
from app.middleware.auth_middleware import customer_required
from app.models.trek import Trek, TrekStatusEnum, DifficultyEnum
from app.models.booking import Booking, BookingStatusEnum ,PaymentStatusEnum
from app.models.customer_profile import CustomerProfile
from app.utils.response import success_response, error_response
from app.utils.cache import get_cache, set_cache, delete_cache
from app.tasks.export_tasks import generate_csv_export
from app.celery_app import celery
from flask import send_file
from app.tasks.notification_tasks import send_booking_confirmation_email
from app.tasks.export_tasks import generate_csv_export
from app.celery_app import celery
from flask import send_file
import os


customer_bp = Blueprint('customer', __name__)


@customer_bp.before_request
@customer_required
def check_customer():
    pass


def _get_current_customer_profile():
    return CustomerProfile.query.filter_by(user_id=current_user.id).first()


# ============================================
# DASHBOARD
# ============================================
@customer_bp.route('/dashboard', methods=['GET'])
def dashboard():
    try:
        available_count = Trek.query.filter_by(status=TrekStatusEnum.OPEN).count()
        my_bookings = Booking.query.filter_by(user_id=current_user.id, status=BookingStatusEnum.BOOKED).count()

        return success_response(data={
            "available_treks": available_count,
            "my_active_bookings": my_bookings,
        })
    except Exception as e:
        return error_response(f"Failed to load dashboard: {str(e)}", 500)


# ============================================
# PROFILE
# ============================================
@customer_bp.route('/profile', methods=['GET'])
def profile():
    profile = _get_current_customer_profile()
    if not profile:
        return error_response("Profile not found", 404)
    return success_response(data=profile.to_dict())


@customer_bp.route('/profile', methods=['PUT'])
def edit_profile():
    profile = _get_current_customer_profile()
    if not profile:
        return error_response("Profile not found", 404)

    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body missing or invalid JSON", 400)

    try:
        if "name" in data and data["name"].strip():
            current_user.name = data["name"].strip()
        if "contact_number" in data:
            profile.contact_number = data["contact_number"].strip()
        if "emergency_contact" in data:
            profile.emergency_contact = data["emergency_contact"].strip()

        db.session.commit()
        return success_response(data=profile.to_dict(), message="Profile updated")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Update failed: {str(e)}", 500)


# ============================================
# AVAILABLE TREKS — CACHED
# ============================================
@customer_bp.route('/treks', methods=['GET'])
def available_treks():
    cache_key = "treks:available"

    cached = get_cache(cache_key)
    if cached:
        return success_response(data=cached, message="Available treks (cached)")

    try:
        treks = Trek.query.filter_by(status=TrekStatusEnum.OPEN).all()
        result = [t.to_dict() for t in treks]
        set_cache(cache_key, result)
        return success_response(data=result)
    except Exception as e:
        return error_response(f"Failed to fetch treks: {str(e)}", 500)


# ============================================
# SEARCH — NO caching, query har baar alag hoti hai
# ============================================
@customer_bp.route('/treks/search', methods=['GET'])
def search_treks():
    location = request.args.get('location', '').strip()
    difficulty = request.args.get('difficulty', '').strip()
    max_duration = request.args.get('max_duration', '').strip()

    try:
        filters = [Trek.status == TrekStatusEnum.OPEN]

        if location:
            filters.append(Trek.location.ilike(f"%{location}%"))
        if difficulty:
            if difficulty.lower() not in [d.value for d in DifficultyEnum]:
                return error_response(f"Invalid difficulty. Must be one of {[d.value for d in DifficultyEnum]}", 400)
            filters.append(Trek.difficulty == DifficultyEnum(difficulty.lower()))
        if max_duration:
            filters.append(Trek.duration_days <= int(max_duration))

        results = Trek.query.filter(*filters).all()
        return success_response(data=[t.to_dict() for t in results])
    except Exception as e:
        return error_response(f"Search failed: {str(e)}", 500)


# ============================================
# TREK DETAILS — CACHED (per trek_id)
# ============================================
@customer_bp.route('/treks/<int:trek_id>', methods=['GET'])
def trek_details(trek_id):
    cache_key = f"trek:{trek_id}"

    cached = get_cache(cache_key)
    if cached:
        return success_response(data=cached)

    trek = Trek.query.get(trek_id)
    if not trek:
        return error_response("Trek not found", 404)

    result = trek.to_dict()
    set_cache(cache_key, result)
    return success_response(data=result)


# ============================================
# BOOKINGS
# ============================================
@customer_bp.route('/bookings', methods=['POST'])
def book_trek():
    data = request.get_json(silent=True)
    if not data or "trek_id" not in data:
        return error_response("trek_id is required", 400)

    trek_id = data["trek_id"]
    trek = Trek.query.get(trek_id)
    if not trek:
        return error_response("Trek not found", 404)

    if not trek.is_open_for_booking():
        return error_response("This trek is not open for booking", 400)

    existing = Booking.query.filter_by(user_id=current_user.id, trek_id=trek_id).first()

    if existing:
        if existing.status == BookingStatusEnum.BOOKED:
            return error_response("You have already booked this trek", 409)

        
        try:
            existing.status = BookingStatusEnum.BOOKED
            existing.payment_status = PaymentStatusEnum.PENDING
            trek.reduce_slot()  

            try:
                from app.tasks.notification_tasks import send_booking_confirmation_email
                send_booking_confirmation_email.delay(
                    current_user.email, current_user.name, trek.name, existing.id
                )
            except Exception as mail_err:
                print(f"Email task failed (non-blocking): {mail_err}")

            delete_cache("treks:available")
            delete_cache(f"trek:{trek_id}")
            return success_response(data=existing.to_dict(), message="Trek booked successfully", status_code=201)

        except ValueError as ve:
            db.session.rollback()
            return error_response(str(ve), 400)
        except Exception as e:
            db.session.rollback()
            return error_response(f"Booking failed: {str(e)}", 500)

    # Case 2: Fresh New booking 
    try:
        booking = Booking(user_id=current_user.id, trek_id=trek_id, status=BookingStatusEnum.BOOKED)
        db.session.add(booking)
        trek.reduce_slot()   

        try:
            from app.tasks.notification_tasks import send_booking_confirmation_email
            send_booking_confirmation_email.delay(
                current_user.email, current_user.name, trek.name, booking.id
            )
        except Exception as mail_err:
            print(f"Email task failed (non-blocking): {mail_err}")

        delete_cache("treks:available")
        delete_cache(f"trek:{trek_id}")
        return success_response(data=booking.to_dict(), message="Trek booked successfully", status_code=201)

    except ValueError as ve:
        db.session.rollback()
        return error_response(str(ve), 400)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Booking failed: {str(e)}", 500)

@customer_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
def cancel_bookings(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return error_response("Booking not found", 404)

    if booking.user_id != current_user.id:
        return error_response("You cannot cancel someone else's booking", 403)

    try:
        booking.cancel()   # model method — status change + slot increase + commit

        delete_cache("treks:available")
        delete_cache(f"trek:{booking.trek_id}")

        return success_response(data=booking.to_dict(), message="Booking cancelled successfully")
    except ValueError as ve:
        return error_response(str(ve), 400)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Cancellation failed: {str(e)}", 500)


# ============================================
# HISTORY
# ============================================
@customer_bp.route('/history', methods=['GET'])
def history():
    try:
        all_bookings = Booking.query.filter_by(user_id=current_user.id).all()
        return success_response(data=[b.to_dict() for b in all_bookings])
    except Exception as e:
        return error_response(f"Failed to fetch history: {str(e)}", 500)


@customer_bp.route('/history/export', methods=['POST'])
def export_history():
    task = generate_csv_export.delay(current_user.id)
    return success_response(data={"job_id": task.id}, message="Export started, check status using job_id")


@customer_bp.route('/history/export/<string:job_id>', methods=['GET'])
def export_status(job_id):
    result = celery.AsyncResult(job_id)

    if result.state == 'PENDING':
        return success_response(data={"status": "processing"}, message="Export still in progress")
    elif result.state == 'SUCCESS':
        return success_response(data={
            "status": "ready",
            "download_url": f"/api/customer/history/export/{job_id}/download"
        })
    elif result.state == 'FAILURE':
        return error_response("Export failed", 500)
    else:
        return success_response(data={"status": result.state})


@customer_bp.route('/history/export/<string:job_id>/download', methods=['GET'])
def download_export(job_id):
    result = celery.AsyncResult(job_id)
    if result.state != 'SUCCESS':
        return error_response("File not ready yet", 400)

    filepath = result.result.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return error_response("File not found", 404)

    return send_file(filepath, as_attachment=True, download_name="booking_history.csv")