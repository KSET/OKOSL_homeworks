from app import db
from app.models import Homework, Task, Subtask


def add_homework():
    ordinal_number = int(input('ordinal number: '))
    year = int(input('year: '))
    task_len = int(input('task number: '))
    print()

    tasks = []
    for task in range(1, task_len+1):
        print(f'Task num {task}')
        solution_filename = input('solution_filename: ')
        task_text = input('task_text: ')
        subtask_len = int(input('subtask number: '))

        subtasks = []
        for subtask in range(1, subtask_len+1):
            print(f'subtask {subtask}')
            subtask_text = input('subtask text: ')
            max_points = float(input('max points: '))
            subtasks.append(Subtask(subtask_number=subtask, subtask_text=subtask_text, max_points=max_points))

        tasks.append(Task(task_number=task, task_text=task_text, subtasks = subtasks, solution_filename=solution_filename))

    homework = Homework(ordinal_number=ordinal_number, year=year, tasks=tasks)
    db.session.add(homework)
    db.session.commit()

if __name__ == "__main__":
    add_homework()
