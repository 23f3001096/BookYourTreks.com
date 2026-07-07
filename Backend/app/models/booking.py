# ============================================
# app/models/booking.py
# ============================================
from app.extensions import db
from app.models.base import TimestampMixin
import enum


class BookingStatusEnum(str, enum.Enum):
    BOOKED = "booked"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class PaymentStatusEnum(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    REFUNDED = "refunded"


class Booking(db.Model, TimestampMixin):
    __tablename__ = 'booking'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)
    status = db.Column(db.Enum(BookingStatusEnum), default=BookingStatusEnum.BOOKED, nullable=False)
    payment_status = db.Column(db.Enum(PaymentStatusEnum), default=PaymentStatusEnum.PENDING, nullable=False)

    user = db.relationship('User', backref=db.backref('bookings', lazy=True))
    trek = db.relationship('Trek', backref=db.backref('bookings', lazy=True))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'trek_id', name='uq_user_trek_booking'),
    )

    def __init__(self, **kwargs):
        super(Booking, self).__init__(**kwargs)

    # ---------- Business logic helpers ----------
    def cancel(self):
        if self.status != BookingStatusEnum.BOOKED:
            raise ValueError("Only active bookings can be cancelled")
        self.status = BookingStatusEnum.CANCELLED
        self.trek.increase_slot()
        db.session.commit()

    def mark_completed(self):
        self.status = BookingStatusEnum.COMPLETED
        db.session.commit()

    def is_active(self):
        return self.status == BookingStatusEnum.BOOKED

    @staticmethod
    def already_booked(user_id, trek_id):
        """Use before creating a booking to block duplicates."""
        return Booking.query.filter_by(
            user_id=user_id, trek_id=trek_id, status=BookingStatusEnum.BOOKED
        ).first() is not None

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "trek_id": self.trek_id,
            "trek_name": self.trek.name if self.trek else None,
            "status": self.status.value,
            "payment_status": self.payment_status.value,
            "booking_date": self.created_at.strftime('%Y-%m-%d') if self.created_at else None,
        }