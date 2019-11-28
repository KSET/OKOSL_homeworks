from app import app, db
from flask import render_template, jsonify, request
from flask_user import login_required, roles_required, current_user
from flask_breadcrumbs import register_breadcrumb
from .models import Homework, Task, Subtask, SolutionGroup, Solution, Remark
from .forms import RemarkForm, FinalRemarkForm
from .repository import Repository
from . import breadcrumb_generators


def render_solution_group(sg_id):
    solution_group = SolutionGroup.query.get(sg_id)
    subtask = solution_group.subtask
    task = subtask.task
    homework = task.homework
    return render_template('solution_group_list_item.html',
                           solution_group=solution_group,
                           subtask=subtask,
                           task=task,
                           homework=homework)


def create_multicollapse_list(subtask_id, solutions=True):
    subtask = Subtask.query.get(subtask_id)
    if solutions:
        multicollapse_targets = ' '.join([f'solutions-{sg.id}' for sg in subtask.solution_groups])
    else:
        multicollapse_targets = ' '.join([f'remarks-{sg.id}' for sg in subtask.solution_groups])
    return multicollapse_targets


app.jinja_env.globals.update(render_solution_group=render_solution_group)
app.jinja_env.globals.update(create_multicollapse_list=create_multicollapse_list)


@app.route('/')
@app.route('/homeworks')
@login_required
def homeworks():
    years = sorted([homework.year for homework in Homework.query.distinct(Homework.year)], reverse=True)
    homeworks_by_year = {year: list(Homework.query.filter(Homework.year == year)) for year in years}
    return render_template('homeworks.html', years=years, homeworks_by_year=homeworks_by_year)


@app.route('/homeworks/<hw_id>')
@register_breadcrumb(app, '.homework', '',
                     dynamic_list_constructor=breadcrumb_generators.get_hw_crumb)
@login_required
def homework(hw_id):
    homework = Homework.query.get(hw_id)
    return render_template('homework_page.html', homework=homework, Repository=Repository)


@app.route('/homeworks/<hw_id>/tasks/<task_id>')
@register_breadcrumb(app, '.homework.task', '',
                     dynamic_list_constructor=breadcrumb_generators.get_task_crumb)
@login_required
def task(task_id, hw_id):
    task = Task.query.get(task_id)
    homework = Homework.query.get(hw_id)
    return render_template('task_page.html', task=task, homework=homework)


@app.route('/homeworks/<hw_id>/tasks/<task_id>/subtask_<subtask_id>')
@register_breadcrumb(app, '.homework.task.subtask', '',
                     dynamic_list_constructor=breadcrumb_generators.get_subtask_crumb)
@login_required
def subtask(subtask_id, task_id, hw_id):
    subtask = Subtask.query.get(subtask_id)
    task = Task.query.get(task_id)
    homework = Homework.query.get(task.homework_id)
    # sort SGs so that the unresolved SGs are at the top because they should take priority
    solution_groups = subtask.solution_groups.order_by(SolutionGroup.final_remark_id.desc())
    return render_template('subtask_page.html',
                           subtask=subtask,
                           task=task,
                           homework=homework,
                           solution_groups=solution_groups)


@app.route('/homeworks/<hw_id>/tasks/<task_id>/subtask_<subtask_id>/solution_group_<solution_group_id>', methods=['GET', 'POST'])
@register_breadcrumb(app, '.homework.task.subtask.solution_group', '',
                     dynamic_list_constructor=breadcrumb_generators.get_solution_group_crumb)
@login_required
def solution_group(solution_group_id, subtask_id, task_id, hw_id):
    solution_group = SolutionGroup.query.get(solution_group_id)
    subtask = Subtask.query.get(subtask_id)
    task = Task.query.get(task_id)
    homework = Homework.query.get(hw_id)

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


@app.route('/ajax/<hw_id>/pull_solutions')
@login_required
def pull_solutions(hw_id):
    homework = Homework.query.get(hw_id)
    try:
        Repository.clone_n_parse(homework)
    except Exception as e:
        return jsonify({'success': False, 'error': e})

    return jsonify({'success': True})


@app.route('/ajax/<hw_id>/push_remarks')
@login_required
def push_remarks(hw_id):
    homework = Homework.query.get(hw_id)  # noqa
    try:
        # Repository.push_remarks(homework)
        pass
    except Exception as e:
        return jsonify({'success': False, 'error': e})

    return jsonify({'success': True})


@app.route('/ajax/move_solution', methods=['POST'])
@login_required
def move_solution():
    solution = Solution.query.get(int(request.json['solution_id']))
    source_sg = SolutionGroup.query.get(int(request.json['source_sg_id']))
    try:
        target_sg = SolutionGroup.query.get(int(request.json['target_sg_id']))
    except TypeError:
        target_sg = None
    subtask = source_sg.subtask
    messages = {}

    if target_sg is None:
        target_sg = SolutionGroup(subtask=subtask)
        db.session.add(target_sg)
        db.session.flush()
        messages['target_added'] = True
        messages['target_sg_id'] = target_sg.id
    solution.solution_group_id = target_sg.id

    if source_sg.solutions.count() == 0:
        for remark in source_sg.remarks:
            target_sg.remarks.append(Remark(text=remark.text,
                                            score_percentage=remark.score_percentage,
                                            author=remark.author,
                                            date=remark.date,
                                            solution_group=target_sg
                                            )
                                     )
            db.session.delete(remark)
        db.session.delete(source_sg)
        messages['source_removed'] = True
    else:
        db.session.add(source_sg)

    db.session.add(target_sg)
    db.session.add(solution)
    try:
        db.session.commit()
    except Exception as e:
        print(e)
        messages['success'] = False
        messages['error'] = str(e)
        return jsonify({'success': False})
    messages['success'] = True
    return jsonify(messages)


@app.route('/ajax/add_solution_group', methods=['POST'])
@login_required
def add_solution_group():
    sg_id = int(request.json['sg_id'])
    html = render_solution_group(sg_id)
    return jsonify({'sg_html': html})


@app.route('/admin')
@roles_required('Admin')
def admin_page():
    return render_template('admin.html')
