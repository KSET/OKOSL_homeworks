from app import app, db
from flask import render_template  # , flash
from flask_user import login_required, roles_required, current_user
from .models import Homework, Task, Subtask, SolutionGroup, Remark  # , Solution, Remark
from .forms import RemarkForm
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


@app.route('/tasks/<task_id>/subtask_<subtask_id>')
@login_required
def subtask(task_id, subtask_id):
    subtask = Subtask.query.get(subtask_id)
    task = Task.query.get(task_id)
    homework = Homework.query.get(task.homework_id)
    return render_template('subtask_page.html', subtask=subtask, task=task, homework=homework)


@app.route('/tasks/<task_id>/subtask_<subtask_id>/solution_group_<sg_id>', methods=['GET', 'POST'])
@login_required
def solution_group(task_id, subtask_id, sg_id):
    solution_group = SolutionGroup.query.get(sg_id)
    subtask = Subtask.query.get(subtask_id)
    task = Task.query.get(task_id)
    form = RemarkForm()

    if form.validate_on_submit():
        author = current_user
        remark_text = form.remark_text.data
        remark_score_percentage = form.remark_score_percentage.data
        remark = Remark(author=author,
                        text=remark_text,
                        score_percentage=remark_score_percentage,
                        solution_group=solution_group
                        )

        db.session.add(remark)
        db.session.commit()
        return render_template('solution_group_page.html',
                               form=form,
                               solution_group=solution_group,
                               subtask=subtask,
                               task=task,
                               homework=homework
                               )
    return render_template('solution_group_page.html',
                           form=form,
                           solution_group=solution_group,
                           subtask=subtask,
                           task=task,
                           homework=homework
                           )


@app.route('/admin')
@roles_required('Admin')
def admin_page():
    return render_template('admin.html')
