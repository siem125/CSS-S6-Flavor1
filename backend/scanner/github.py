import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def set_commit_status(repo_full_name: str, sha: str, state: str):
    url = f"https://api.github.com/repos/{repo_full_name}/statuses/{sha}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "state": state,  # success | failure | pending
        "context": "security-scan",
        "description": "Scan passed" if state == "success" else "Scan failed"
    }

    response = requests.post(url, json=data, headers=headers)

    return response.json()