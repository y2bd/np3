"""Add album_art_url

Revision ID: 7c1e3181c5ad
Revises: 7c3bd17a7133
Create Date: 2024-01-07 20:21:49.665196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c1e3181c5ad'
down_revision = '7c3bd17a7133'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.add_column(sa.Column('album_art_url', sa.VARCHAR(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('rating', schema=None) as batch_op:
        batch_op.drop_column('album_art_url')

    # ### end Alembic commands ###
