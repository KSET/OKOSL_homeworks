"""empty message

Revision ID: ea87a6729ee7
Revises: 8d21886aade7
Create Date: 2019-09-26 17:02:11.475468

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ea87a6729ee7'
down_revision = '8d21886aade7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('remarks', sa.Column('score_percentage', sa.Float(), nullable=False))
    op.drop_column('remarks', 'score_penalty')
    op.add_column('solution_groups', sa.Column('final_score_percentage', sa.Float(), nullable=True))
    op.drop_column('solution_groups', 'final_score_penalty')
    op.add_column('tasks', sa.Column('max_points', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'max_points')
    op.add_column('solution_groups', sa.Column('final_score_penalty', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('solution_groups', 'final_score_percentage')
    op.add_column('remarks', sa.Column('score_penalty', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.drop_column('remarks', 'score_percentage')
    # ### end Alembic commands ###