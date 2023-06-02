import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from flask_security import RoleMixin

from .db import db


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<Role {self.id}:{self.name}>'