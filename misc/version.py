
import requests

def get_latest_commit_sha():
    url = f"https://api.github.com/repos/AmoreForever/pc-controller-bot/commits"
    response = requests.get(url)
    if response.status_code == 200:
        if commits := response.json():
            latest_commit = commits[0]
            sha = latest_commit['sha']
            return sha[:7]  # Сокращенный хэш
    return None

version = "1 1 2"

