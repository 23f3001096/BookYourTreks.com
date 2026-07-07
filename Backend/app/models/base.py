# ============================================
# app/models/base.py
# ============================================
from app.extensions import db
from datetime import datetime, timezone


class TimestampMixin:
    """Mixin so every model gets created_at/updated_at for free."""
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )