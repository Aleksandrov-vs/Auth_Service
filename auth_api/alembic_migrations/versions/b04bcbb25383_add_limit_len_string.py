"""add limit len string

Revision ID: b04bcbb25383
Revises: 2f6f2234615b
Create Date: 2023-06-10 23:25:21.569323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b04bcbb25383'
down_revision = '2f6f2234615b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('users', 'login', type_=sa.String(length=50), nullable=False)
    op.alter_column('roles', 'name', type_=sa.String(length=30), nullable=False)
    op.alter_column('auth_history', 'user_agent', type_=sa.String(length=100), nullable=False)


def downgrade() -> None:
    op.alter_column('users', 'login', type_=sa.String(), nullable=False)
    op.alter_column('roles', 'name', type_=sa.String(), nullable=False)
    op.alter_column('auth_history', 'user_agent', type_=sa.String(), nullable=False)
