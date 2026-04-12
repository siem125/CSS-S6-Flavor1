from fastapi import APIRouter, Request
from scanner.service import run_scan

router = APIRouter()


@router.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()

    event = request.headers.get("X-GitHub-Event")

    # We care about push + PR
    if event not in ["push", "pull_request"]:
        return {"status": "ignored"}

    repo_url = payload["repository"]["clone_url"]

    result = run_scan(repo_url)

    return {
        "event": event,
        "repo": repo_url,
        "result": result
    }