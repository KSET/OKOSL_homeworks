import requests
import json
import os
import subprocess
from config import Config

class Repos():
    def __init__(self, homework_name):
        self.homework_name = homework_name
        self.api_url = 'https://'+Config.GITEA_HOST+'/api/v1'
        self.headers = {'Authorization': 'token '+Config.GITEA_TOKEN}
        self.repo_location = Config.REPOS_ROOT+'/'+homework_name
        os.mkdir(self.repo_location)
        self.repos = []

    def clone_n_parse(self):
        pass

    def search(self):
        response = requests.get(
                self.api_url+'/repos/search',
                headers = self.headers,
                params = {'q': self.homework_name})
        
        json_response = json.loads(response.text)
        self.repos = json_response['data']

    def clone(self):
        for repo in self.repos:
            subprocess.run(['git', 'clone',
                repo['ssh_url'],
                self.repo_location+'/'+repo['owner']['login']])

