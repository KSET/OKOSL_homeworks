from app import db
from datetime import datetime
from flask_user import UserMixin


class Homework(db.Model):
    __tablename__ = "homeworks"
    id = db.Column(db.Integer, primary_key=True)
    ordinal_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=True)  # in case we want to name the homework
    year = db.Column(db.Integer, unique=True, nullable=False)
    tasks = db.relationship("Task", backref="homework", lazy="dynamic")


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    task_number = db.Column(db.Integer, nullable=False)
    task_text = db.Column(db.Text, nullable=False)
    homework_id = db.Column(db.Integer, db.ForeignKey("homeworks.id"), nullable=False)
    solution_groups = db.relationship("SolutionGroup", backref="task", lazy="dynamic")


class SolutionGroup(db.Model):
    __tablename__ = "solution_groups"
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    solutions = db.relationship("Solution", backref="task", lazy="dynamic")
    # the following fields should be filled once a final, aggregate comment is written
    final_comment = db.Column(db.Text, nullable=True)
    final_score_penalty = db.Column(db.Integer, nullable=True)


class Solution(db.Model):
    __tablename__ = "solutions"
    id = db.Column(db.Integer, primary_key=True)
    solution_text = db.Column(db.Text, nullable=False)
    comments = db.relationship("Comment", backref="solution", lazy="dynamic")
    solution_group_id = db.Column(db.Integer, db.ForeignKey("solution_groups.id"), nullable=False)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    score_penalty = db.Column(db.Float(), nullable=False)
    author = db.Column(db.String(255), nullable=True)  # this should reflect users once implemented
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    solution_id = db.Column(db.Integer, db.ForeignKey("solutions.id"), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')

    # User information
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')

    # Define the relationship to Role via UserRoles
    roles = db.relationship('Role', secondary='user_roles')

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


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))
