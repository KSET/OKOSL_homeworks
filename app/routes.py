from app import app
from flask import render_template  # , flash, redirect, url_for
# from werkzeug.utils import secure_filename
from flask_user import login_required, roles_required  # , current_user
from .models import Homework, Task
# import datetime


NUMBER_OF_ARTICLES = 3


@app.route('/')
@app.route('/homeworks')
@login_required
def homeworks():
    years = sorted([homework.year for homework in Homework.query.distinct(Homework.year)])
    homeworks_by_year = {year: list(Homework.query.filter(Homework.year == year)) for year in years}
    return render_template('homeworks.html', years=years, homeworks_by_year=homeworks_by_year)


@app.route('/homeworks/<hw_id>')
@login_required
def homework(hw_id):
    homework = Homework.query.get(hw_id)
    return render_template('homework_page.html', homework=homework)


@app.route('/tasks/<task_id>')
@login_required
def task(task_id):
    task = Task.query.get(task_id)
    homework = Homework.query.get(task.homework_id)
    return render_template('task_page.html', task=task, homework=homework)


@app.route('/admin')
@roles_required('Admin')
def admin_page():
    return render_template('admin.html')
