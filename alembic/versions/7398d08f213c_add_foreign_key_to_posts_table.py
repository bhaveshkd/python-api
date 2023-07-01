"""add foreign-key to posts table

Revision ID: 7398d08f213c
Revises: f861dd86a438
Create Date: 2023-07-01 16:21:55.095880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7398d08f213c'
down_revision = 'f861dd86a438'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key(constraint_name='posts_users_fk', source_table='posts', referent_table='users', local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
    pass
