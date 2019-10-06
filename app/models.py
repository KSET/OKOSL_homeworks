from app import db
from datetime import datetime
from flask_user import UserMixin
from sqlalchemy.schema import UniqueConstraint, CheckConstraint


SNIPPET_LENGTH = 20


def get_text_snippet(text):
    return text if len(text) < SNIPPET_LENGTH else f'{text[:SNIPPET_LENGTH - 3]}...'


class Homework(db.Model):
    """Homework model. Each homework uniquely defined by its ordinal number and the AY it occurs in."""

    __tablename__ = "homeworks"
    __table_args__ = (UniqueConstraint('ordinal_number', 'year', name="unique_homework_year"),)
    id = db.Column(db.Integer, primary_key=True)
    ordinal_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=True)  # in case we want to name the homework
    # a dedicated model for years could be added, but this would increase the complexity of the model,
    # and but the sole benefit would be getting all years in the database, and there will be only a
    # few homeworks per year, so it is probably not worth the increase in complexity
    year = db.Column(db.Integer, nullable=False)

    tasks = db.relationship("Task", backref="homework", lazy="dynamic")
    solved_homeworks = db.relationship("SolvedHomework", backref="homework")

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<HW name: {self.name}>'

    def __init__(self, *args, **kwargs):
        """
        Overriding to add default name if empty - set it to DZ<number>-<year>
        """
        if 'name' not in kwargs:
            kwargs['name'] = f'DZ{kwargs["ordinal_number"]}-{kwargs["year"]}'
        super().__init__(*args, **kwargs)


class Task(db.Model):
    """Task model. Each homework is divided into tasks, which roughly correspond to a single topic
    (e.g. tasks with sed or user creation). Each task is divided into subtasks."""

    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_number = db.Column(db.Integer, nullable=False)  # the task's homework-level ordinal number

    # task-level note, e.g. "All subtasks pertain to the file /usr/share/dict/words"
    task_text = db.Column(db.Text, nullable=False)

    # filename that should exist in the repo and contain the task solution
    solution_filename = db.Column(db.Text, nullable=False)

    homework_id = db.Column(db.Integer, db.ForeignKey("homeworks.id"), nullable=False)
    subtasks = db.relationship("Subtask", backref="task", lazy="dynamic")

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
    max_points = db.Column(db.Integer, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)

    solution_groups = db.relationship("SolutionGroup", backref="subtask", lazy="dynamic")

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<TaskID:{self.task_id};Task#{self.subtask_number}>'


class SolutionGroup(db.Model):
    """Solution Group model. Each subtask has several possible solutions, correct or otherwise.
    However, some solutions may be syntactically different, but functionally identical
    (e.g. ls -al and ls -la), so it makes sense to group these. This model enables it.
    """

    __tablename__ = "solution_groups"
    id = db.Column(db.Integer, primary_key=True)
    subtask_id = db.Column(db.Integer, db.ForeignKey("subtasks.id"), nullable=False)

    solutions = db.relationship("Solution", backref="solution_group", lazy="dynamic")
    remarks = db.relationship("Remark", backref="solution_group", lazy="dynamic")

    # the following fields should be filled once a final, aggregate remark is written
    final_remark = db.Column(db.Text, nullable=True)
    final_score_percentage = db.Column(db.Float(), nullable=True)

    __table_args__ = (
        CheckConstraint(final_score_percentage >= 0, name='check_final_score_percentage_positive'),
        CheckConstraint(final_score_percentage <= 1.5, name='check_final_score_percentage_not_exceeded'),
    )

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<SGID:{self.id};SubtaskID:{self.subtask_id}>'


class Remark(db.Model):
    """Remark model. Each SolutionGroup can have a remark. Each remark consists of its text
    (a reviewer's comment on the solution) and the percentage of the maximum points it attained.
    This percentage can be between 0 and 1.5 (e.g. in the case of a particularly innovative
    solution.)
    """

    __tablename__ = "remarks"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    score_percentage = db.Column(db.Float(), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    solution_group_id = db.Column(db.Integer, db.ForeignKey("solution_groups.id"), nullable=False)

    __table_args__ = (
        CheckConstraint(score_percentage >= 0, name='check_score_percentage_positive'),
        CheckConstraint(score_percentage <= 1.5, name='check_score_percentage_not_exceeded'),
    )

    def __repr__(self):
        """
        Override the default string representation method
        """
        return f'<RemarkID:{self.id};Text:{get_text_snippet(self.text)}>'


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
    solution_group_id = db.Column(db.Integer, db.ForeignKey("solution_groups.id"), nullable=False)

    solved_homeworks = db.relationship("SolvedHomeworkSolution", back_populates="solution")

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
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey("homeworks.id"), nullable=False)

    repo_path = db.Column(db.String(255), nullable=False)
    # points = db.Column(db.Float(), nullable=True)
    solutions = db.relationship("SolvedHomeworkSolution", back_populates="solved_homework")


class SolvedHomeworkSolution(db.Model):
    """
    Association model which links solved homeworks to the solutions contained in them.
    """

    __tablename__ = "solved_homeworks_solutions"

    id = db.Column(db.Integer, primary_key=True)
    solved_homework_id = db.Column(db.Integer, db.ForeignKey("solved_homeworks.id"), nullable=False)
    solution_id = db.Column(db.Integer, db.ForeignKey("solutions.id"), nullable=False)

    solved_homework = db.relationship("SolvedHomework", back_populates="solutions")
    solution = db.relationship("Solution", back_populates="solved_homeworks")


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

    def __init__(self, *args, **kwargs):
        """
        Override the constructor to derive a username from email if not otherwise specified
        """
        if 'username' not in kwargs:
            kwargs['username'] = kwargs['email'].split("@")[0]
        super().__init__(*args, **kwargs)

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
