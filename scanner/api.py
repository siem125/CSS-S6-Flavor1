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

    #Show extracted data
    print("Incoming event:", event)
    print("Repo:", repo_name)
    print("SHA:", sha)

    #Scan error handling
    try:
        #set initial commit status to pending
        set_commit_status(repo_name, sha, "pending")

        result = run_scan(repo_url)

        state = "failure" if result["block"] else "success"

    except Exception as e:
        print("SCAN ERROR:", e)

        result = {"error": str(e)}
        state = "failure"

    #update the commit status to the result(or if error fail it)
    response = set_commit_status(repo_name, sha, state)
    print("GitHub response:", response)

    return {
        "event": event,
        "repo": repo_url,
        "sha": sha,
        "result": result,
        "state": state
    }