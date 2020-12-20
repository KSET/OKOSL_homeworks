import requests
import json

URL = 'https://edu.kset.org/api/v1/repos/migrate/'
GITEA_API_HEADERS = {'Authorization': 'token <token>',
        'Content-Type': 'application/json'}

for i in range(273, 275):
    response = requests.post(
            URL,
            headers=GITEA_API_HEADERS,
            json = {
                "clone_addr": "<template_repo_url>",
                "mirror": False,
                "private": True,
                "repo_name": "<repo_name>",
                "uid": i})
    print(response.text)

