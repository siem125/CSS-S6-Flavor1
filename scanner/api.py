from fastapi import FastAPI, Request
from pydantic import BaseModel
from scanner.service import run_scan
from scanner.github import set_commit_status

app = FastAPI()


class ScanRequest(BaseModel):
    repo_url: str

#manual scanning of a given repo
@app.post("/scan")
def scan_repo(request: ScanRequest):
    return run_scan(request.repo_url)


#automatic scan from github
@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    event = request.headers.get("X-GitHub-Event")

    # Only react to relevant events
    if event not in ["push", "pull_request"]:
        return {"status": "ignored"}

    repo_url = payload["repository"]["clone_url"]
    repo_name = payload["repository"]["full_name"]

    # Extract commit SHA
    if event == "push":
        sha = payload.get("after")
    else:
        sha = payload["pull_request"]["head"]["sha"]

    result = run_scan(repo_url)

    state = "failure" if result["block"] else "success"

    set_commit_status(repo_name, sha, state)

    return {
        "event": event,
        "repo": repo_url,
        "sha": sha,
        "result": result
    }