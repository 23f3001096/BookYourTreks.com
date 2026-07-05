from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.base import BaseModel

class User(BaseModel,):
    __tablename__ = 'users'

    email          = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash  = db.Column(db.String(200), nullable=False)
    role           = db.Column(db.String(20), nullable=False)  # admin|staff|customer
    is_active_user = db.Column(db.Boolean, default=True, nullable=False)
    is_verified    = db.Column(db.Boolean, default=False, nullable=False)  # email OTP done
    last_login     = db.Column(db.DateTime, nullable=True)

    # relationships
    customer_profile = db.relationship('CustomerProfile', backref='user',
                                        uselist=False, lazy='joined')
    staff_profile    = db.relationship('StaffProfile', backref='user',
                                        uselist=False, lazy='joined')
    bookings         = db.relationship('Booking', backref='user', lazy='dynamic')
    reviews          = db.relationship('Review', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def profile(self):
        if self.role == 'customer':
            return self.customer_profile
        if self.role == 'staff':
            return self.staff_profile
        return None

    def is_admin(self):
        return self.role == 'admin'

    def is_staff(self):
        return self.role == 'staff'

    def is_customer(self):
        return self.role == 'customer'

    def get_id(self):
        return str(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'is_active_user': self.is_active_user,
            'is_verified': self.is_verified,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
        }