import os
import json
from requests import get
from requests.auth import HTTPBasicAuth
from pprint import pprint

if not os.path.exists('articles'):
    os.makedirs('articles')

with open('config.json') as j:
    config = json.load(j)

base = 'https://api.github.com'
headers = {'Accept': 'application/vnd.github.com.v3+json'}

owner = 'SteveRoche'
repo = 'iecse-swacch-bharat'

auth = HTTPBasicAuth(config['username'], config['password'])

pulls_url = f'{base}/repos/{owner}/{repo}/pulls'

pulls_json = get(pulls_url, headers=headers, params={'per_page': 100}, auth=auth).json()

users = [ {'username': doc['user']['login'], 'pull_num': doc['number']} for doc in pulls_json ]
c = 0
for user in users:
    files_url = f"{base}/repos/{owner}/{repo}/pulls/{user['pull_num']}/files"
    files_json = get(files_url, headers=headers, auth=auth).json()
    for f in files_json:
        if 'patch' in f and 'filename' in f:
            filename = f['filename']
            raw_diff = f['patch']
            clean = [ line.strip('+')+'\n' for line in raw_diff.split('\n')[1:] ]
            print(f'Writing to {filename}')
            with open(f'articles/{filename}', 'w') as f:
                c += 1
                f.writelines(clean)

print(f"Fetched articles of {c} users")
