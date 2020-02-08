import subprocess
from app import db
from app.models import SolvedHomework

def generate_report(solved_homework):
    '''Generates report.txt file in homework repository and pushes it

    Returns:
    float:Points scored'''

    points_scored = 0.

    with open(solved_homework.repo_path+'/report.md', 'w') as report:
        report.write('# '+solved_homework.homework.get_slug()+' Report  \n')

        for i, solution in enumerate(solved_homework.solutions):
            report.write('## Subtask '+str(i+1)+'  \n')

            solution_text = solution.solution_text
            report.write('> '+'\n'.join([s+'  ' for s in solution_text.split('\n')])+'\n')

            report.write('Remark:   \n')
            remark = solution.solution_group.final_remark.text
            report.write('> '+'\n'.join([s+'  ' for s in remark.split('\r\n')])+'\n')

            points = solution.solution_group.subtask.max_points *\
                    solution.solution_group.final_remark.score_percentage
            max_points = solution.solution_group.subtask.max_points
            report.write('Points: '+str(points)+'/'+str(max_points)+'  \n')
            points_scored += points
            report.write('\n')

        report.write('\n**Total points scored: '+str(points_scored)+'**  ')

    #_push_report(solved_homework)

    return points_scored


def _push_report(solved_homework):
    subprocess.run(['git', '-C', solved_homework.repo_path,
                    'add', 'report.md'], check=True)
    subprocess.run(['git', '-C', solved_homework.repo_path,
                    'checkout', '-b', 'report'], check=True)
    subprocess.run(['git', '-C', solved_homework.repo_path,
                    'commit', '-m', 'Add report'], check=True)
    subprocess.run(['git', '-C', solved_homework.repo_path,
                    'push', '--set-upstream', 'origin', 'report'], check=True)

def generate_summary(homework):
    '''Returns a list of (JMGAB, points_scored) tuples for given homework'''
    if not verify_final_remarks(homework):
        raise ValueError("Some solutions don't have a final remark!")

    summary = []

    for solved_homework in db.session.query(SolvedHomework).filter(
            SolvedHomework.homework == homework):
        summary.append((solved_homework.student.jmbag, _get_points(solved_homework)))

    return summary


def verify_final_remarks(homework):
    '''Checks that all solutions have a final remark'''
    #TODO After fixing a bug that enables having empty SGs change this so that
    # instead of iterating throught all SolvedHomeworks and their solutions it
    # iterates through all SG-s instead
    for solved_homework in db.session.query(SolvedHomework).filter(
            SolvedHomework.homework == homework):
        for solution in solved_homework.solutions:
            if not solution.solution_group.final_remark:
                return False

    return True


def _get_points(solved_homework):
    points = 0

    for s in solved_homework.solutions:
        points += s.solution_group.final_remark.score_percentage *\
                s.solution_group.subtask.max_points

    return points
