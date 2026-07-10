# app/models/staff_profile.py

from app.extensions import db
from app.models.base import TimestampMixin
import enum


class StaffStatusEnum(str, enum.Enum):
    ACTIVE = "active"
    BLOCKED = "blocked"


class StaffProfile(db.Model, TimestampMixin):
    __tablename__ = 'staff_profile'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.Enum(StaffStatusEnum), default=StaffStatusEnum.ACTIVE, nullable=False)

    user = db.relationship('User', backref=db.backref('staff_profile', uselist=False))

    def __init__(self, **kwargs):
        super(StaffProfile, self).__init__(**kwargs)

    def is_blocked(self):
        return self.status == StaffStatusEnum.BLOCKED

    def block(self):
        self.status = StaffStatusEnum.BLOCKED
        db.session.commit()

    def unblock(self):
        self.status = StaffStatusEnum.ACTIVE
        db.session.commit()

    def assigned_trek_count(self):
        return len(self.treks)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.user.name if self.user else None,
            "contact_number": self.contact_number,
            "status": self.status.value,
            "assigned_treks": self.assigned_trek_count(),
        }