"""empty message

Revision ID: 523201412811
Revises: 91a31e1ef1d6
Create Date: 2019-10-09 19:41:56.889852

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '523201412811'
down_revision = '91a31e1ef1d6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('homeworks', sa.Column('activity', sa.String(length=255), nullable=True))
    op.drop_column('homeworks', 'name')
    op.alter_column('remarks', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_constraint('remarks_solution_group_id_fkey', 'remarks', type_='foreignkey')
    op.drop_constraint('remarks_author_id_fkey', 'remarks', type_='foreignkey')
    op.create_foreign_key(None, 'remarks', 'users', ['author_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key(None, 'remarks', 'solution_groups', ['solution_group_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('solution_groups_subtask_id_fkey', 'solution_groups', type_='foreignkey')
    op.create_foreign_key(None, 'solution_groups', 'subtasks', ['subtask_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('solutions_solution_group_id_fkey', 'solutions', type_='foreignkey')
    op.create_foreign_key(None, 'solutions', 'solution_groups', ['solution_group_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('subtasks_task_id_fkey', 'subtasks', type_='foreignkey')
    op.create_foreign_key(None, 'subtasks', 'tasks', ['task_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('tasks_homework_id_fkey', 'tasks', type_='foreignkey')
    op.create_foreign_key(None, 'tasks', 'homeworks', ['homework_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'tasks', type_='foreignkey')
    op.create_foreign_key('tasks_homework_id_fkey', 'tasks', 'homeworks', ['homework_id'], ['id'])
    op.drop_constraint(None, 'subtasks', type_='foreignkey')
    op.create_foreign_key('subtasks_task_id_fkey', 'subtasks', 'tasks', ['task_id'], ['id'])
    op.drop_constraint(None, 'solutions', type_='foreignkey')
    op.create_foreign_key('solutions_solution_group_id_fkey', 'solutions', 'solution_groups', ['solution_group_id'], ['id'])
    op.drop_constraint(None, 'solution_groups', type_='foreignkey')
    op.create_foreign_key('solution_groups_subtask_id_fkey', 'solution_groups', 'subtasks', ['subtask_id'], ['id'])
    op.drop_constraint(None, 'remarks', type_='foreignkey')
    op.drop_constraint(None, 'remarks', type_='foreignkey')
    op.create_foreign_key('remarks_author_id_fkey', 'remarks', 'users', ['author_id'], ['id'])
    op.create_foreign_key('remarks_solution_group_id_fkey', 'remarks', 'solution_groups', ['solution_group_id'], ['id'])
    op.alter_column('remarks', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('homeworks', sa.Column('name', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('homeworks', 'activity')
    # ### end Alembic commands ###
