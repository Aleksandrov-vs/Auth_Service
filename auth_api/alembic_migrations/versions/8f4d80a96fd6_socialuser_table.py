"""SocialUser table

Revision ID: 8f4d80a96fd6
Revises: b83ee4c730e2
Create Date: 2023-06-15 23:42:01.691164

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8f4d80a96fd6'
down_revision = 'b83ee4c730e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('social_user',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('social_id', sa.Text(), nullable=False),
    sa.Column('login', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('social_user')
    # ### end Alembic commands ###
