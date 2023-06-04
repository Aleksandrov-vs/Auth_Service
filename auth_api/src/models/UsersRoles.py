import uuid
from sqlalchemy import Table, Column, Integer, ForeignKey
from .db import db
from sqlalchemy.dialects.postgresql import UUID

UserRole = Table(
    'UsersRoles',
    db.metadata,
    Column('id', UUID(as_uuid=True), default=uuid.uuid4, primary_key=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('User.id')),
    Column('role_id', UUID(as_uuid=True), ForeignKey('Role.id'))
)
