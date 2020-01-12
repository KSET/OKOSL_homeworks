import subprocess

def generate_report(solved_homework):
    '''Generates report.txt file in homework repository and pushes it

    Returns:
    float:Points scored'''

    points_scored = 0.

    with open(solved_homework.repo_path+'/report.txt', 'w') as report:
        report.write(solved_homework.homework.get_slug()+' Report\n\n\n')

        for i, solution in enumerate(solved_homework.solutions):
            report.write('Subtask '+str(i+1)+'\n')
            report.write('Solution:\n')
            report.write(solution.solution_text)
            report.write('Remark:\n')
            report.write(solution.solution_group.final_remark.text+'\n')
            report.write('Maximum points: '+str(solution.solution_group.subtask.max_points)+'\n')
            points = solution.solution_group.subtask.max_points * solution.solution_group.final_remark.score_percentage
            report.write('Points scored: '+str(points)+'\n')
            points_scored += points
            report.write('\n')

        report.write('\nTotal points scored: '+str(points_scored))

    _push_report(solved_homework)

    return points_scored


def _push_report(solved_homework):
    subprocess.run(['git', '-C', solved_homework.repo_path, 'add', 'report.txt'])
    subprocess.run(['git', '-C', solved_homework.repo_path, 'checkout', '-b', 'report'])
    subprocess.run(['git', '-C', solved_homework.repo_path, 'commit', '-m', 'Add report'])
    subprocess.run(['git', '-C', solved_homework.repo_path, 'push', '--set-upstream', 'origin', 'report'])

# def generate summary(homework):
