from app import db
from datetime import datetime
from flask_user import UserMixin
from sqlalchemy.schema import UniqueConstraint, CheckConstraint
from sqlalchemy.ext.orderinglist import ordering_list


SNIPPET_LENGTH = 20

solved_homework_solution_association = db.Table(
    "solved_homeworks_solutions",
    db.Model.metadata,
    db.Column("solved_homeworks_id", db.Integer, db.ForeignKey("solved_homeworks.id", ondelete="CASCADE")),
    db.Column("solutions_id", db.Integer, db.ForeignKey("solutions.id", ondelete="CASCADE"))
)


def get_text_snippet(text):
    return text if len(text) < SNIPPET_LENGTH else f'{text[:SNIPPET_LENGTH - 3]}...'


class Homework(db.Model):
    """Homework model. Each homework uniquely defined by its ordinal number and the AY it occurs in."""

    __tablename__ = "homeworks"
    __table_args__ = (UniqueConstraint('ordinal_number', 'year', name="unique_homework_year"),)
    id = db.Column(db.Integer, primary_key=True)
    ordinal_number = db.Column(db.Integer, nullable=False)
    activity = db.Column(db.String(255), nullable=True, default='DZ')  # in case we want to extend to e.g. lab exercises
    year = db.Column(db.Integer, nullable=False)

    tasks = db.relationship("Task", backref="homework", order_by="Task.task_number",
                            collection_class=ordering_list("task_number", count_from=1))
    solved_homeworks = db.relationship("SolvedHomework", backref="homework")

    def get_slug(self):
        return f"{self.activity}_{self.ordinal_number}-{self.year}"

    def has_unresolved(self):
        for task in self.tasks:
            for subtask in task.subtasks:
                for solution_group in subtask.solution_groups:
                    if solution_group.final_remark is None:
                        return True
        return False

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<HW: {self.get_slug()}>'


class Task(db.Model):
    """Task model. Each homework is divided into tasks, which roughly correspond to a single topic
    (e.g. tasks with sed or user creation). Each task is divided into subtasks."""

    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_number = db.Column(db.Integer, nullable=False)  # the task's homework-level ordinal number

    # task-level note, e.g. "All subtasks pertain to the file /usr/share/dict/words"
    task_text = db.Column(db.Text, nullable=True)

    # filename that should exist in the repo and contain the task solution
    solution_filename = db.Column(db.Text, nullable=False)

    homework_id = db.Column(db.Integer, db.ForeignKey("homeworks.id", ondelete="CASCADE"), nullable=False)
    subtasks = db.relationship("Subtask", backref="task", order_by="Subtask.subtask_number",
                               collection_class=ordering_list("subtask_number", count_from=1))

    def __init__(self, *args, **kwargs):
        """
        Overriding to add default solution filename if empty - set it to "task_{number}.sh"
        """
        if 'solution_filename' not in kwargs:
            kwargs['solution_filename'] = f'task_{kwargs["task_number"]}.sh'
        super().__init__(*args, **kwargs)

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<HWID:{self.homework_id};Task#{self.task_number}>'


class Subtask(db.Model):
    """Subtask model. Each subtask has its number, text, and the ID of the Task it belongs to."""

    __tablename__ = "subtasks"
    id = db.Column(db.Integer, primary_key=True)
    subtask_number = db.Column(db.Integer, nullable=False)
    subtask_text = db.Column(db.Text, nullable=False)
    max_points = db.Column(db.Float(), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)

    solution_groups = db.relationship("SolutionGroup", backref="subtask", lazy="dynamic")

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<TaskID:{self.task_id};Task#{self.subtask_number}>'


class Remark(db.Model):
    """Remark model. Each SolutionGroup can have a remark. Each remark consists of its text
    (a reviewer's comment on the solution) and the percentage of the maximum points it attained.
    This percentage can be between 0 and 1.5 (e.g. in the case of a particularly innovative
    solution.)
    """

    # Note: Remark must be defined before SolutionGroup because SolutionGroup references it.
    __tablename__ = "remarks"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    score_percentage = db.Column(db.Float(), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    solution_group_id = db.Column(db.Integer, db.ForeignKey("solution_groups.id", ondelete="CASCADE"), nullable=False)
    solution_group = db.relationship('SolutionGroup', foreign_keys=[solution_group_id], back_populates='remarks')

    __table_args__ = (
        CheckConstraint(score_percentage >= 0, name='check_score_percentage_positive'),
        CheckConstraint(score_percentage <= 1.5, name='check_score_percentage_not_exceeded'),
    )

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<RemarkID:{self.id};SGID:{self.solution_group_id};Text:{get_text_snippet(self.text)}>'


class SolutionGroup(db.Model):
    """Solution Group model. Each subtask has several possible solutions, correct or otherwise.
    However, some solutions may be syntactically different, but functionally identical
    (e.g. ls -al and ls -la), so it makes sense to group these. This model enables it.
    """

    __tablename__ = "solution_groups"
    id = db.Column(db.Integer, primary_key=True)
    subtask_id = db.Column(db.Integer, db.ForeignKey("subtasks.id", ondelete="CASCADE"), nullable=False)

    solutions = db.relationship("Solution", backref="solution_group", lazy="dynamic")
    remarks = db.relationship("Remark", foreign_keys=[Remark.solution_group_id], back_populates="solution_group")

    # the following fields should be filled once a final, aggregate remark is written
    final_remark_id = db.Column(db.Integer, db.ForeignKey("remarks.id", ondelete="SET NULL"), nullable=True)
    final_remark = db.relationship("Remark", foreign_keys=[final_remark_id], post_update=True)

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<SGID:{self.id};SubtaskID:{self.subtask_id}>'


class Solution(db.Model):
    """
    Solution model. Each solution should be uniquely determined by its text and the solution group it belongs to.
    Several subtasks (e.g. recycled subtasks from previous years) may have the same solution, so imposing a unique
    constraint on solution_text would muddy the model up.
    A solution may be functionally identical to other solutions, so each solution belongs to a single SolutionGroup.
    """

    __tablename__ = "solutions"
    __table_args__ = (
        db.UniqueConstraint('solution_text', 'solution_group_id', name='_solution_text_group_unique'),
    )
    id = db.Column(db.Integer, primary_key=True)
    solution_text = db.Column(db.Text, nullable=False, unique=False)
    solution_group_id = db.Column(db.Integer, db.ForeignKey("solution_groups.id", ondelete="CASCADE"), nullable=False)

    solved_homeworks = db.relationship(
        "SolvedHomework",
        secondary=solved_homework_solution_association,
        back_populates="solutions"
    )

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<SolID:{self.id};Text:{get_text_snippet(self.solution_text)}>'


class Student(db.Model):
    """
    Student model. Used for linking the Solutions with repositories for each submitted homework.
    """

    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    jmbag = db.Column(db.String(10), nullable=False, unique=True)  # 10 because JMBAGs at UniZG have 10 digits
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)

    solved_homeworks = db.relationship("SolvedHomework", backref="student")


class SolvedHomework(db.Model):
    """
    Model which models a solved homework as a whole. It links students with homeworks, and points to the solutions to
    all the tasks for a given homework. There is an additional repo_url field which contains the URL to the repo.
    """

    __tablename__ = "solved_homeworks"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey("homeworks.id", ondelete="CASCADE"), nullable=False)

    repo_path = db.Column(db.String(255), nullable=False)
    # points = db.Column(db.Float(), nullable=True)
    solutions = db.relationship(
        "Solution",
        secondary=solved_homework_solution_association,
        back_populates="solved_homeworks")


class User(db.Model, UserMixin):
    """User model. This is used by the Flask-User module, which handles user authentication.
    Additionally, each solution group remark has an author, which is a user.
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    username = db.Column(db.String(100), nullable=False, unique=True)
    # email = db.Column(db.String(255), nullable=False, unique=True)
    added_at = db.Column(db.DateTime(), default=datetime.now)
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')
    remarks = db.relationship('Remark', backref='author', lazy='dynamic')

    def has_role(self, role):
        """
        Thi method simply checks if a user has a certain role.
        """
        return role in [r.name for r in self.roles]

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<Username: {self.username}>'


# Define the Role data-model
class Role(db.Model):
    """Role model. No, not a role-model. This table models roles users can have (e.g. admin)."""

    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<Role name: {self.name}>'


# Define the UserRoles association table
class UserRoles(db.Model):
    """Association table between users and roles."""

    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
