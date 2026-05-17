import subprocess
import tempfile
import os

def clone_repo(repo_url: str) -> str:
    temp_dir = tempfile.mkdtemp()
    token = os.getenv("GITHUB_TOKEN")

    # inject token into the repo_url for authentication
    auth_url = repo_url.replace(
        "https://",
        f"https://x-access-token:{token}@"
    )

    subprocess.run(
        ["git", "clone", auth_url, temp_dir],
        check=True
    )

    return temp_dir