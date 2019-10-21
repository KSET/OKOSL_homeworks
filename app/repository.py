import requests
import json
import os
import subprocess
from config import Config
from app import app, db
from app.models import *
from sqlalchemy.orm.exc import NoResultFound

class Repository(SolvedHomework):

    def clone_n_parse(homework):
        name = homework.get_slug()
        repos_root = Config.REPOS_ROOT+'/'+name
        try:
            os.mkdir(repos_root)
        except FileExistsError:
            pass

        repositories = Repository.clone(Repository.search(name), repos_root, homework)

        for repo in repositories:
            Repository.parse(repo)


    def search(name):
        repos = []

        response_len = Config.GITEA_API_PAGE_SIZE
        page = 1
        while response_len == Config.GITEA_API_PAGE_SIZE:
            response = requests.get(
                Config.GITEA_API_URL+'/repos/search',
                headers = Config.GITEA_API_HEADERS,
                params = {'q': name, 'limit':Config.GITEA_API_PAGE_SIZE, 'page':page})
            json_response = json.loads(response.text)['data']
            page += 1
            response_len = len(json_response)
            response_repos = filter(lambda r:r['name'] == name, json_response)
            
            repos.extend(response_repos)

        return repos

 
    def clone(repos, repos_root, homework):
        repositories = []
        for repo in repos:
            try:
                student = Student.query.filter(
                    Student.jmbag == repo['owner']['login']).one()
            except NoResultFound:
                app.logger.warning(f'Student not found; repo {repo["html_url"]} has student with JMBAG "{repo["owner"]["login"]}"')
                continue

            clone_location = repos_root+'/'+repo['owner']['login']

            if os.path.exists(clone_location):
                try:
                    solved_hw = SolvedHomework.query.filter(SolvedHomework.repo_path == clone_location).one()
                except NoResultFound:
                    solved_hw = SolvedHomework(student = student, homework = homework, repo_path = clone_location)
                    db.session.add(solved_hw)
            else:
                solved_hw = SolvedHomework(student = student, homework = homework, repo_path = clone_location)
                db.session.add(solved_hw)
            
            repositories.append(solved_hw)

            subprocess.run(['git', 'clone',
                '--quiet',
                repo['ssh_url'],
                clone_location])

        db.session.commit()

        return repositories


    
    def parse(sh):
        if len(sh.solutions) > 0:
            return

        for task in sh.homework.tasks:

            solution_texts = Repository.parse_file(sh.repo_path+'/'+task.solution_filename, len(task.subtasks))

            for i in range(len(task.subtasks)):
                existing = db.session.query(Solution).join(SolutionGroup).\
                        filter(Solution.solution_text == solution_texts[i], SolutionGroup.subtask_id == task.subtasks[i].id).first()
                if existing:
                    sh.solutions.append(existing)
                else:
                    new_solution_group = SolutionGroup(subtask=task.subtasks[i])
                    new_solution = Solution(solution_text=solution_texts[i], solution_group=new_solution_group)
                    db.session.add(new_solution_group)
                    sh.solutions.append(new_solution)
            
            db.session.commit()

    
    def parse_file(filename, subtasks_count):
        try:
            with open(filename, 'r') as f:
                lines = list(filter(None,[x.rstrip() for x in f.readlines()]))
                lines = [x+'\n' for x in lines]
        # If file is not found for current task, return empty solutions
        except FileNotFoundError:
            # For each subtask check if there already is an empty solution
            return ['']*subtasks_count
        
        #delimeter indices
        indices = [i for i,x in enumerate(lines) if x=='#!#!#!#!#!#!#\n']
        solutions = []
        
        for i in range(len(indices)-1):
            solutions.append('')
            for line in lines[indices[i]+1:indices[i+1]]:
                if line[0] != '#':
                    solutions[i] += line

        # If there are less solutions than needed, append empty solutions
        while len(solutions) < subtasks_count:
            solutions.append('')

        # Discard any 'solutions' exceeding the number of subtasks
        return solutions[:subtasks_count]
