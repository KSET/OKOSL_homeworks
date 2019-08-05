from cujes import db
from datetime import datetime


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
    solutions = db.relationship("Solution", backref="task", lazy="dynamic")


class Solution(db.Model):
    __tablename__ = "solutions"
    id = db.Column(db.Integer, primary_key=True)
    solution_text = db.Column(db.Text, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    comments = db.relationship("Comment", backref="solution", lazy="dynamic")
    # the following fields should be filled once a final, aggregate comment is written
    final_comment = db.Column(db.Text, nullable=True)
    final_score_penalty = db.Column(db.Integer, nullable=True)


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    score_penalty = db.Column(db.Float(), nullable=False)
    author = db.Column(db.String(255), nullable=True)  # this should reflect users once implemented
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    solution_id = db.Column(db.Integer, db.ForeignKey("solutions.id"), nullable=False)
