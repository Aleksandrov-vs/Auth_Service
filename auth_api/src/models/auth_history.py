import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from .db import db
from .user import User


class AuthHistory(db.Model):
    __tablename__ = 'auth_history'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False)
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey(
            User.id,
            ondelete='CASCADE'
        ),
        nullable=False
    )
    user_agent = db.Column(db.String(100))
    auth_date = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<AuthHistory {self.user_id}:{self.auth_date}>'
