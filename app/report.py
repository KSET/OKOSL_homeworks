import subprocess
from app import db
from app.models import SolvedHomework

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
            points = solution.solution_group.subtask.max_points *\
                    solution.solution_group.final_remark.score_percentage
            report.write('Points scored: '+str(points)+'\n')
            points_scored += points
            report.write('\n')

        report.write('\nTotal points scored: '+str(points_scored))

    _push_report(solved_homework)

    return points_scored


def _push_report(solved_homework):
    subprocess.run(['git', '-C', solved_homework.repo_path,
                    'add', 'report.txt'], check=True)
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

def plagiarism_summary(homework, treshold=0):
    """Returns a sorted list of JMBAG student pairs and a number of shared SGs"""
    results = plagiarism_results(homework)
    results.sort(key=lambda x: x[1], reverse=True)

    summary = []
    for (sh_1, sh_2), count in results:
        if count >= treshold:
            summary.append(((sh_1.student.jmbag, sh_2.student.jmbag), count))

    return summary


def plagiarism_results(homework):
    '''Returns number of shared SGs for each student pair'''


    solved_homeworks = list(SolvedHomework.query.filter(SolvedHomework.homework == homework))

    results = []
    for index, sh_1 in enumerate(solved_homeworks):
        for sh_2 in solved_homeworks[index+1:]:
            results.append(((sh_1, sh_2), _plagiarism_check(sh_1, sh_2)))
    
    return results


def _plagiarism_check(solved_homework_1, solved_homework_2):
    """Return a number of shared SGs for two given Solved Homeworks 

    Doesn't count SG as shared if either student has an empty solution
    """

    counter = 0
    for sol_1, sol_2 in zip(solved_homework_1.solutions, solved_homework_2.solutions):
        if (sol_1.solution_text != ''
                and sol_2.solution_text != ''
                and sol_1.solution_group == sol_2.solution_group):
            counter += 1

    return counter

