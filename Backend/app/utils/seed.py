# app/utils/seed.py

from app.extensions import db
from app.models.user import User, RoleEnum


def insert_admin():
    if not User.query.filter_by(email="admin@gmail.com").first():
        admin = User(
            email="admin@gmail.com",
            name="System Admin",
            role=RoleEnum.ADMIN,
            active=True,
            blocked=False
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully.")
    else:
        print("Admin already exists.")