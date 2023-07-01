"""add content column to posts table

Revision ID: 0e8ebe22ad37
Revises: abaa85fe4e66
Create Date: 2023-07-01 16:09:02.240813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e8ebe22ad37'
down_revision = 'abaa85fe4e66'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
