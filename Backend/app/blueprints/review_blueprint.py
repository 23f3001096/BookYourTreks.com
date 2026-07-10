# ============================================
# app/blueprints/review_blueprint.py
# ============================================
from flask import Blueprint, request
from flask_login import current_user

from app.extensions import db
from app.middleware.auth_middleware import customer_required
from app.models.trek import Trek
from app.models.review import Review
from app.models.booking import Booking, BookingStatusEnum
from app.utils.response import success_response, error_response
from app.utils.validators import validate_required_fields

review_bp = Blueprint('review', __name__)


# ============================================
# VIEW REVIEWS — public, koi login nahi chahiye
# ============================================
@review_bp.route('/treks/<int:trek_id>/reviews', methods=['GET'])
def view_reviews(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return error_response("Trek not found", 404)

    try:
        reviews = Review.query.filter_by(trek_id=trek_id).order_by(Review.created_at.desc()).all()
        return success_response(data={
            "average_rating": trek.average_rating(),
            "total_reviews": len(reviews),
            "reviews": [r.to_dict() for r in reviews],
        })
    except Exception as e:
        return error_response(f"Failed to fetch reviews: {str(e)}", 500)


# ============================================
# ADD REVIEW — sirf customer, aur sirf jisne trek complete kiya ho
# ============================================
@review_bp.route('/treks/<int:trek_id>/reviews', methods=['POST'])
@customer_required
def add_review(trek_id):
    trek = Trek.query.get(trek_id)
    if not trek:
        return error_response("Trek not found", 404)

    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body missing or invalid JSON", 400)

    ok, err = validate_required_fields(data, ["rating"])
    if not ok:
        return error_response(err, 400)

    rating = data.get("rating")
    comment = data.get("comment", "").strip() if data.get("comment") else None

    # rating type + range check
    try:
        rating = int(rating)
    except (ValueError, TypeError):
        return error_response("Rating must be an integer", 400)

    if not (1 <= rating <= 5):
        return error_response("Rating must be between 1 and 5", 400)

    # sirf wahi user review kar sakta hai jisne actually trek book/complete kiya ho
    has_valid_booking = Booking.query.filter_by(
        user_id=current_user.id,
        trek_id=trek_id
    ).filter(
        Booking.status.in_([BookingStatusEnum.BOOKED, BookingStatusEnum.COMPLETED])
    ).first()

    if not has_valid_booking:
        return error_response("You can only review treks you have booked", 403)

    # duplicate review check
    if Review.user_already_reviewed(current_user.id, trek_id):
        return error_response("You have already reviewed this trek", 409)

    try:
        review = Review(
            user_id=current_user.id,
            trek_id=trek_id,
            rating=rating,
            comment=comment,
        )
        db.session.add(review)
        db.session.commit()
        return success_response(data=review.to_dict(), message="Review added successfully", status_code=201)
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to add review: {str(e)}", 500)


# ============================================
# EDIT REVIEW — sirf apni review edit kar sakta hai
# ============================================
@review_bp.route('/reviews/<int:review_id>', methods=['PUT'])
@customer_required
def edit_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return error_response("Review not found", 404)

    if review.user_id != current_user.id:
        return error_response("You can only edit your own review", 403)

    data = request.get_json(silent=True)
    if not data:
        return error_response("Request body missing or invalid JSON", 400)

    try:
        if "rating" in data:
            try:
                rating = int(data["rating"])
            except (ValueError, TypeError):
                return error_response("Rating must be an integer", 400)

            if not (1 <= rating <= 5):
                return error_response("Rating must be between 1 and 5", 400)

            review.rating = rating

        if "comment" in data:
            review.comment = data["comment"].strip() if data["comment"] else None

        db.session.commit()
        return success_response(data=review.to_dict(), message="Review updated successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to update review: {str(e)}", 500)


# ============================================
# DELETE REVIEW — sirf apni review delete kar sakta hai
# ============================================
@review_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
@customer_required
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        return error_response("Review not found", 404)

    if review.user_id != current_user.id:
        return error_response("You can only delete your own review", 403)

    try:
        db.session.delete(review)
        db.session.commit()
        return success_response(message="Review deleted successfully")
    except Exception as e:
        db.session.rollback()
        return error_response(f"Failed to delete review: {str(e)}", 500)