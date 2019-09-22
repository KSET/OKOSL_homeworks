import requests
import json
import os
import subprocess

class Repos():
    def __init__(self, homework_name):
        self.homework_name = homework_name
        self.api_url = 'https://'+os.environ['GITEA_HOST']+'/api/v1'
        self.headers = {'Authorization': 'token '+os.environ['GITEA_TOKEN']}
        self.repo_location = os.environ['REPO_LOCATION']+'/'+homework_name
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

