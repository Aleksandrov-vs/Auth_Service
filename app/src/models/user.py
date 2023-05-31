import uuid
from sqlalchemy.dialects.postgresql import UUID

from src import db
from .role import Role


class User(db.Model):
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
        'Role',
        secondary=Role.__table__
    )

    def __repr__(self):
        return f'<User {self.login}:{self.roles}>'
