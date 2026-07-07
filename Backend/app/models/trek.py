# ============================================
# app/models/trek.py
# ============================================
from app.extensions import db
from app.models.base import TimestampMixin
import enum


class DifficultyEnum(str, enum.Enum):
    EASY = "easy"
    MODERATE = "moderate"
    HARD = "hard"


class TrekStatusEnum(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    OPEN = "open"
    CLOSED = "closed"
    COMPLETED = "completed"


class Trek(db.Model, TimestampMixin):
    __tablename__ = 'trek'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    difficulty = db.Column(db.Enum(DifficultyEnum), nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False, default=0)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff_profile.id'), nullable=True)
    status = db.Column(db.Enum(TrekStatusEnum), default=TrekStatusEnum.PENDING, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    staff = db.relationship('StaffProfile', backref=db.backref('treks', lazy=True))

    def __init__(self, **kwargs):
        super(Trek, self).__init__(**kwargs)

    # ---------- Business logic helpers ----------
    def is_open_for_booking(self):
        return self.status == TrekStatusEnum.OPEN and self.available_slots > 0

    def has_slots(self):
        return self.available_slots > 0

    def reduce_slot(self):
        """Call when a booking is confirmed."""
        if self.available_slots <= 0:
            raise ValueError("No slots available")
        self.available_slots -= 1
        if self.available_slots == 0:
            self.status = TrekStatusEnum.CLOSED
        db.session.commit()

    def increase_slot(self):
        """Call when a booking is cancelled."""
        self.available_slots += 1
        if self.status == TrekStatusEnum.CLOSED and self.available_slots > 0:
            self.status = TrekStatusEnum.OPEN
        db.session.commit()

    def mark_started(self):
        self.status = TrekStatusEnum.OPEN
        db.session.commit()

    def mark_completed(self):
        self.status = TrekStatusEnum.COMPLETED
        db.session.commit()

    def registered_users_count(self):
        from app.models.booking import BookingStatusEnum
        return len([b for b in self.bookings if b.status == BookingStatusEnum.BOOKED])

    def average_rating(self):
        if not self.reviews:
            return None
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "difficulty": self.difficulty.value,
            "duration_days": self.duration_days,
            "available_slots": self.available_slots,
            "assigned_staff_id": self.assigned_staff_id,
            "status": self.status.value,
            "start_date": self.start_date.strftime('%Y-%m-%d') if self.start_date else None,
            "end_date": self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            "registered_users": self.registered_users_count(),
            "average_rating": self.average_rating(),
        }