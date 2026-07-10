
# app/models/customer_profile.py

from app.extensions import db
from app.models.base import TimestampMixin


class CustomerProfile(db.Model, TimestampMixin):
    __tablename__ = 'customer_profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)
    emergency_contact = db.Column(db.String(15), nullable=True)

    user = db.relationship('User', backref=db.backref('customer_profile', uselist=False))

    def __init__(self, **kwargs):
        super(CustomerProfile, self).__init__(**kwargs)

    # ---------- Helpers ----------
    def total_bookings(self):
        from app.models.booking import Booking
        return Booking.query.filter_by(user_id=self.user_id).count()

    def active_bookings(self):
        from app.models.booking import Booking, BookingStatusEnum
        return Booking.query.filter_by(user_id=self.user_id, status=BookingStatusEnum.BOOKED).all()

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.user.name if self.user else None,
            "contact_number": self.contact_number,
            "emergency_contact": self.emergency_contact,
        }