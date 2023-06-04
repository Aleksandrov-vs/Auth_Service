import uuid

from sqlalchemy.dialects.postgresql import UUID
from flask_security import UserMixin

from .UsersRoles import UserRole
from .db import db
from .role import Role


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship(
        'Detail',
        secondary=UserRole,
        backref='User'
    )

    def __repr__(self):
        return f'<User {self.login}>'

