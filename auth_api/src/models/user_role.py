import uuid
from sqlalchemy import Table, Column, Integer, ForeignKey
from .db import db
from sqlalchemy.dialects.postgresql import UUID

user_role_table = Table(
    'user_role',
    db.metadata,
    Column('id', UUID(as_uuid=True), default=uuid.uuid4, primary_key=True),
    Column('user_id', UUID(as_uuid=True), ForeignKey('users.id')),
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id'))
)
