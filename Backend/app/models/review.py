# app/models/review.py

from app.extensions import db
from app.models.base import TimestampMixin


class Review(db.Model, TimestampMixin):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('trek.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=True)

    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    trek = db.relationship('Trek', backref=db.backref('reviews', lazy=True))

    def __init__(self, **kwargs):
        super(Review, self).__init__(**kwargs)

    # Helper Methods
    def is_valid_rating(self):
        return 1 <= self.rating <= 5

    @staticmethod
    def user_already_reviewed(user_id, trek_id):
        return Review.query.filter_by(user_id=user_id, trek_id=trek_id).first() is not None

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user.name if self.user else None,
            "trek_id": self.trek_id,
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.strftime('%Y-%m-%d') if self.created_at else None,
        }