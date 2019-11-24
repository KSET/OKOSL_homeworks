from .models import Homework, Task, Subtask, SolutionGroup
from flask import request, url_for


def get_hw_crumb(*args, **kwargs):
    hw_id = request.view_args['hw_id']
    hw = Homework.query.get(hw_id)
    return [{'text': hw.get_slug(), 'url': url_for('homework', hw_id=hw_id)}]


def get_task_crumb(*args, **kwargs):
    task_id = request.view_args['task_id']
    task = Task.query.get(task_id)
    hw_id = task.homework.id
    return [{'text': f'Task {task.task_number}', 'url': url_for('task', hw_id=hw_id, task_id=task_id)}]


def get_subtask_crumb(*args, **kwargs):
    subtask_id = request.view_args['subtask_id']
    subtask = Subtask.query.get(subtask_id)
    task = subtask.task
    hw = task.homework
    return [{
        'text': f'Subtask {subtask.subtask_number}',
        'url': url_for('subtask', hw_id=hw.id, task_id=task.id, subtask_id=subtask_id)
        }]


def get_solution_group_crumb(*args, **kwargs):
    sg_id = request.view_args['solution_group_id']
    sg = SolutionGroup.query.get(sg_id)
    subtask = sg.subtask
    task = subtask.task
    hw = task.homework
    return [{
        'text': f'SolutionGroup {sg.id}',
        'url': url_for('solution_group', hw_id=hw.id, task_id=task.id,
                       subtask_id=subtask.id, solution_group_id=sg_id)
        }]


def get_crumbs(*args, **kwargs):
    breadcrumbs = []
    if 'hw_id' in request.view_args:
        print("HW CRUMB GEN")
        hw_id = request.view_args['hw_id']
        hw = Homework.query.get(hw_id)
        breadcrumbs.append({
            'text': hw.get_slug(),
            'url': url_for('homework', hw_id=hw_id)
                            })
        if 'task_id' in request.view_args:
            print("TASK CRUMB GEN")
            task_id = request.view_args['task_id']
            task = Task.query.get(task_id)
            breadcrumbs.append({
                'text': f'Task {task.task_number}',
                'url': url_for('task', hw_id=hw_id, task_id=task_id)
                })
            if 'subtask_id' in request.view_args:
                print("SUBTASK CRUMB GEN")
                subtask_id = request.view_args['subtask_id']
                subtask = Subtask.query.get(subtask_id)
                breadcrumbs.append({
                    'text': f'Subtask {subtask.subtask_number}',
                    'url': url_for('subtask', hw_id=hw_id, task_id=task_id, subtask_id=subtask_id)
                    })
                if 'solution_group_id' in request.view_args:
                    print("SG CRUMB GEN")
                    sg_id = request.view_args['solution_group_id']
                    sg = SolutionGroup.query.get(sg_id)
                    breadcrumbs.append({
                        'text': f'SolutionGroup {sg.id}',
                        'url': url_for('solution_group', hw_id=hw_id, task_id=task_id,
                                       subtask_id=subtask_id, solution_group_id=sg_id)
                        })

    return breadcrumbs