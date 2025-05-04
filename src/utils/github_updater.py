import os
import requests
import json

GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/releases/latest"

def check_for_updates(owner, repo, current_version):
    response = requests.get(GITHUB_API_URL.format(owner=owner, repo=repo))
    
    if response.status_code == 200:
        latest_release = response.json()
        latest_version = latest_release['tag_name']
        
        if latest_version != current_version:
            download_url = latest_release['assets'][0]['url']
            download_latest_version(download_url)
            return latest_version
    return None

def download_latest_version(download_url):
    response = requests.get(download_url, allow_redirects=True)
    
    if response.status_code == 200:
        with open('projectA_latest.zip', 'wb') as file:
            file.write(response.content)
        # Here you would typically extract the zip and apply the update
        # For simplicity, we are just saving the zip file

def get_current_version():
    with open('data/version.json', 'r') as file:
        version_info = json.load(file)
        return version_info['version']