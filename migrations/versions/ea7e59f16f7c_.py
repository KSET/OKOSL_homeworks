"""empty message

Revision ID: ea7e59f16f7c
Revises: 4c2ba870f417
Create Date: 2019-10-09 16:58:46.344401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea7e59f16f7c'
down_revision = '4c2ba870f417'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'task_number',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'task_number',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
