"""empty message

Revision ID: 0bfac18e753e
Revises: 4337f81f7398
Create Date: 2019-10-15 20:37:15.932663

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0bfac18e753e'
down_revision = '4337f81f7398'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('solution_groups', sa.Column('final_remark_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'solution_groups', 'remarks', ['final_remark_id'], ['id'], ondelete='SET NULL')
    op.drop_column('solution_groups', 'final_remark')
    op.drop_column('solution_groups', 'final_score_percentage')
    op.alter_column('tasks', 'task_text',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('tasks', 'task_text',
               existing_type=sa.TEXT(),
               nullable=False)
    op.add_column('solution_groups', sa.Column('final_score_percentage', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True))
    op.add_column('solution_groups', sa.Column('final_remark', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'solution_groups', type_='foreignkey')
    op.drop_column('solution_groups', 'final_remark_id')
    # ### end Alembic commands ###