import requests
import json
import os
import subprocess
from config import Config
from app import app, db
import app.models as models
from sqlalchemy.orm.exc import NoResultFound

class Repository(models.SolvedHomework):

    def clone_n_parse(homework):
        name = homework.name+'_'+str(homework.year)+'-'+str(homework.ordinal_number)
        repo_location = Config.REPOS_ROOT+'/'+name
        os.mkdir(repo_location)

        Repository.clone(Repository.search(name), repo_location)


    def search(name):
        response = requests.get(
                Config.GITEA_API_URL+'/repos/search',
                headers = Config.GITEA_API_HEADERS,
                params = {'q': name})

        # Filter out any repositories whose name doesn't match completely
        return filter(lambda r:r['name'] == name, json.loads(response.text)['data'])

 
    def clone(repos, repo_location):
        SolvedHomeworks = []
        for repo in repos:
            try:
                student = models.Student.query.filter(
                    models.Student.jmbag == repo['owner']['login']).one()
            except NoResultFound:
                app.logger.warning(f'Student not found; repo {repo["html_url"]} has student with JMBAG {repo["owner"]["login"]}')
                continue

            subprocess.run(['git', 'clone',
                '--quiet',
                repo['ssh_url'],
                repo_location+'/'+repo['owner']['login']])


    
    def parse(repos):
        pass
