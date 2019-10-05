import requests
import json
import os
import subprocess
from config import Config
from app import db
import app.models as models

class Repository(models.SolvedHomework):

    def clone_n_parse(homework):
        homework_name = homework.name
        repo_location = Config.REPOS_ROOT+'/'+homework_name
        os.mkdir(repo_location)
        Repository.clone(Repository.search(homework.name), repo_location)


    def search(name):
        response = requests.get(
                Config.GITEA_API_URL+'/repos/search',
                headers = Config.GITEA_API_HEADERS,
                params = {'q': name})
        
        return json.loads(response.text)['data']

 
    def clone(repos, repo_location):
        for repo in repos:
            subprocess.run(['git', 'clone',
                repo['ssh_url'],
                repo_location+'/'+repo['owner']['login']])

