# app/models/__init__.py

from app.extensions import db

# import all models so SQLAlchemy registers their tables

from app.models.user import User, RoleEnum
from app.models.staff_profile import StaffProfile, StaffStatusEnum
from app.models.customer_profile import CustomerProfile
from app.models.trek import Trek, DifficultyEnum, TrekStatusEnum
from app.models.booking import Booking, BookingStatusEnum, PaymentStatusEnum
from app.models.review import Review


def create_tables():
    from app.utils.seed import insert_admin
    db.create_all()
    insert_admin()


__all__ = [
    "db",
    "User", "RoleEnum",
    "StaffProfile", "StaffStatusEnum",
    "CustomerProfile",
    "Trek", "DifficultyEnum", "TrekStatusEnum",
    "Booking", "BookingStatusEnum", "PaymentStatusEnum",
    "Review",
    "create_tables",
]