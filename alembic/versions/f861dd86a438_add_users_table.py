"""add users table

Revision ID: f861dd86a438
Revises: 0e8ebe22ad37
Create Date: 2023-07-01 16:13:59.121646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f861dd86a438'
down_revision = '0e8ebe22ad37'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable=False), 
                    sa.Column('email', sa.String(), nullable=False), 
                    sa.Column('password', sa.String(), nullable=False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email') 
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
