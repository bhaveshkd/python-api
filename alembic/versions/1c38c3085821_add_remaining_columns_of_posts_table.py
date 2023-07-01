"""add remaining columns of posts table

Revision ID: 1c38c3085821
Revises: 7398d08f213c
Create Date: 2023-07-01 16:28:46.224164

"""
from email.policy import default
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c38c3085821'
down_revision = '7398d08f213c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
