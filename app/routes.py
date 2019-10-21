from app import app, db
from flask import render_template  # , flash
from flask_user import login_required, roles_required, current_user
from .models import Homework, Task, Subtask, SolutionGroup, Remark  # , Solution, Remark
from .forms import RemarkForm, FinalRemarkForm
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
    remark_form = RemarkForm()
    final_remark_form = FinalRemarkForm()
    author = current_user
    remark_added = False
    final_remark_added = False

    if remark_form.validate_on_submit() and remark_form.submit_remark.data:
        target_form = remark_form
        remark_added = True
    elif final_remark_form.validate_on_submit() and final_remark_form.submit_final_remark.data:
        target_form = final_remark_form
        final_remark_added = True

    if remark_added or final_remark_added:
        remark_text = target_form.remark_text.data
        remark_score_percentage = target_form.remark_score_percentage.data
        remark = Remark(author=author,
                        text=remark_text,
                        score_percentage=remark_score_percentage,
                        solution_group=solution_group
                        )

        if remark_added:
            db.session.add(remark)
            db.session.commit()
        else:
            if solution_group.final_remark is not None:
                db.session.delete(solution_group.final_remark)
            solution_group.final_remark = remark
            db.session.add(solution_group)
            db.session.commit()
    return render_template('solution_group_page.html',
                           remark_form=remark_form,
                           final_remark_form=final_remark_form,
                           solution_group=solution_group,
                           subtask=subtask,
                           task=task,
                           homework=homework
                           )


# @app.route('/tasks/<task_id>/subtask_<subtask_id>/solution_group_<sg_id>', methods=['POST'])
# @login_required
# def add_remark(task_id, subtask_id, sg_id):
#     flash("Adding remark")
#     print("Adding remark")
#     form = RemarkForm()
#     author = current_user

#     if form.validate_on_submit():
#         remark_text = form.remark_text.data
#         remark_score_percentage = form.remark_score_percentage.data
#         remark = Remark(author=author,
#                         text=remark_text,
#                         score_percentage=remark_score_percentage,
#                         solution_group=solution_group
#                         )
#         db.session.add(remark)
#         db.session.commit()
#         flash("Remark added!", 'success')
#     return redirect(url_for('solution_group', task_id=task_id, subtask_id=subtask_id, sg_id=sg_id))


# @app.route('/tasks/<task_id>/subtask_<subtask_id>/solution_group_<sg_id>', methods=['POST'])
# @login_required
# def add_final_remark(task_id, subtask_id, sg_id):
#     flash("Adding final remark")
#     print("Adding final remark")
#     form = FinalRemarkForm()
#     author = current_user

#     if form.validate_on_submit():
#         remark_text = form.remark_text.data
#         remark_score_percentage = form.remark_score_percentage.data
#         remark = Remark(author=author,
#                         text=remark_text,
#                         score_percentage=remark_score_percentage,
#                         solution_group=solution_group
#                         )
#         solution_group.final_remark = remark
#         db.session.add(solution_group)
#         db.session.commit()
#         flash("Final remark added!", 'success')
#     return redirect(url_for('solution_group', task_id=task_id, subtask_id=subtask_id, sg_id=sg_id))


@app.route('/admin')
@roles_required('Admin')
def admin_page():
    return render_template('admin.html')
