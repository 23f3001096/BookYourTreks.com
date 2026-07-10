# ============================================
# app/models/user.py
# ============================================
from app.extensions import db
from app.models.base import TimestampMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import enum


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"


class User(db.Model, UserMixin, TimestampMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(512), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.Enum(RoleEnum), nullable=False, default=RoleEnum.CUSTOMER)

    active = db.Column(db.Boolean, default=True, nullable=False)
    blocked = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    #  Auth helpers 
    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)

    # Flask-Login checks this automatically on login_user() and every session load.
    # Overrides UserMixin's default (which always returns True).
    
    @property
    def is_active(self) -> bool: # ignore 
        return self.active and not self.blocked

    #  Role check helpers 
    def is_admin(self):
        return self.role == RoleEnum.ADMIN

    def is_staff(self):
        return self.role == RoleEnum.STAFF

    def is_customer(self):
        return self.role == RoleEnum.CUSTOMER

    #  Account management 
    def block(self):
        self.blocked = True
        db.session.commit()

    def unblock(self):
        self.blocked = False
        db.session.commit()

    def deactivate(self):
        self.active = False
        db.session.commit()

    def activate(self):
        self.active = True
        db.session.commit()

    #  Serialization 
    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role.value,
            "active": self.active,
            "blocked": self.blocked,
            "created_at": self.created_at.strftime('%Y-%m-%d') if self.created_at else None,
        }