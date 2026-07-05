from datetime import datetime
from app.extensions import db

class BaseModel(db.Model):
    
    __abstract__ = True

    id         = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
