# app/blueprints/payment_blueprint.py

from flask import Blueprint
from app.extensions import db
from app.models.booking import Booking, PaymentStatusEnum

payment_bp = Blueprint('payment', __name__)


@payment_bp.route('/confirm/<int:booking_id>', methods=['GET'])
def confirm_payment(booking_id):
    
    booking = Booking.query.get(booking_id)
    if not booking:
        return "<h3>Booking not found</h3>", 404

    if booking.payment_status == PaymentStatusEnum.PAID:
        return """
            <div style="font-family:sans-serif;text-align:center;padding:60px">
                <h2 style="color:#0f766e">Already Paid ✔</h2>
                <p>This booking's payment was already confirmed.</p>
            </div>
        """

    booking.payment_status = PaymentStatusEnum.PAID
    db.session.commit()

    return f"""
        <div style="font-family:sans-serif;text-align:center;padding:60px">
            <h2 style="color:#0f766e">Payment Successful ✔</h2>
            <p>Your payment for booking #{booking.id} has been confirmed (Demo Mode).</p>
            <p>You can close this tab now.</p>
        </div>
    """