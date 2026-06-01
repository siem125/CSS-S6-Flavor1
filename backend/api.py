from fastapi import FastAPI, Request
from pydantic import BaseModel

from database import engine, SessionLocal
from models import Base, Scan, Vulnerability, Repo

from service import run_scan
from github import set_commit_status

import json

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse


# create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI()


class ScanRequest(BaseModel):
    repo_url: str


@dataclass
class ScanContext:
    repo_url: str
    repo_name: str | None
    sha: str | None
    event: str | None


@app.post("/scan")
def scan_repo(request: ScanRequest):
    db = SessionLocal()

    try:
        result = start_scan(
            db=db,
            repo_url=request.repo_url
        )

        return result

    finally:
        db.close()


@app.post("/webhook")
async def github_webhook(request: Request):
    db = SessionLocal()

    try:
        payload = await request.json()

        event = request.headers.get("X-GitHub-Event")

        # ignore unrelated events
        if event not in ["push", "pull_request"]:
            return {"status": "ignored"}

        repo_url = payload["repository"]["clone_url"]

        repo_name = payload["repository"]["full_name"]

        # extract SHA
        if event == "push":
            sha = payload.get("after")
        else:
            sha = payload["pull_request"]["head"]["sha"]

        # pending status
        set_commit_status(repo_name, sha, "pending")

        result = start_scan(
            db=db,
            repo_url=repo_url,
            repo_name=repo_name,
            sha=sha,
            event=event
        )

        # update github commit status
        set_commit_status(repo_name, sha, result["status"])

        return {
            "event": event,
            "repo": repo_url,
            "sha": sha,
            "result": result
        }

    except Exception as e:

        print("SCAN ERROR:", e)
        set_commit_status(repo_name, sha, "failure")
        return {"error": str(e)}
    
    finally:
        db.close()



def start_scan(db, repo_url: str, repo_name: str = None, sha: str = None, event: str = None):
    repo = get_or_create_repo(db, repo_url, repo_name)

    context = ScanContext(
        repo_url=repo.url,
        repo_name=repo.name,
        sha=sha,
        event=event
    )

    result = run_scan(context.repo_url)

    insert_scan(db, repo, context, result)

    return result



def get_or_create_repo(db, url: str, name: str = None):
    repo = db.query(Repo).filter(Repo.url == url).first()
    #If repo exists get that one
    if repo:
        return repo

    # derive name if is missing
    derived_name = name or extract_repo_name(url)

    repo = Repo(
        url=url,
        name=derived_name
    )

    db.add(repo)
    db.commit()
    db.refresh(repo)

    return repo



def insert_scan(db, repo, context: ScanContext, result):
    try:
        scan = Scan(
            repo_id=repo.id,
            sha=context.sha,
            event=context.event,
            status=result["status"],
            block=result["block"],
            reason=result["reason"],
            duration=result["duration"],
            vulnerability_count=result["vulnerability_count"]
        )

        db.add(scan)
        db.commit()
        db.refresh(scan)

        for vuln in result["vulnerabilities"]["matches"]:
            db.add(Vulnerability(
                scan_id=scan.id,
                vulnerability_id=vuln.get("vulnerability", {}).get("id"),
                severity=vuln.get("vulnerability", {}).get("severity"),
                package_name=vuln.get("artifact", {}).get("name"),
                installed_version=vuln.get("artifact", {}).get("version"),
                fixed_version=(
                    vuln.get("vulnerability", {})
                        .get("fix", {})
                        .get("versions", [None])[0]
                ),
                description=vuln.get("vulnerability", {}).get("description")
            ))

        db.commit()

    finally:
        db.close()



def extract_repo_name(url: str) -> str:
    try:
        path = urlparse(url).path.strip("/")  # e.g. "owner/repo"
        if path:
            return path.split("/")[-1]  # repo name
    except Exception:
        pass

    return url  # fallback


@app.get("/scans")
def get_scans():
    db = SessionLocal()

    try:
        scans = (
            db.query(Scan)
            .order_by(Scan.created_at.desc())
            .all()
        )

        return [
            {
                "id": s.id,
                "repo": {
                    "id": s.repo.id,
                    "name": s.repo.name,
                    "url": s.repo.url,
                },
                "sha": s.sha,
                "event": s.event,
                "status": s.status,
                "block": s.block,
                "reason": s.reason,
                "vulnerability_count": s.vulnerability_count,
                "duration": s.duration,
                "created_at": s.created_at,
            }
            for s in scans
        ]

    finally:
        db.close()



@app.get("/repos/{repo_id}")
def get_repo(repo_id: int):
    db = SessionLocal()

    try:
        repo = db.query(Repo).filter(Repo.id == repo_id).first()

        if not repo:
            return None

        return {
            "id": repo.id,
            "name": repo.name,
            "url": repo.url,
            "scans": [
                {
                    "id": s.id,
                    "sha": s.sha,
                    "status": s.status,
                    "duration": s.duration,
                    "vulnerability_count": s.vulnerability_count,
                    "created_at": s.created_at,
                    "vulnerabilities": [
                        {
                            "id": v.id,
                            "package": v.package_name,
                            "severity": v.severity,
                            "description": v.description
                        }
                        for v in s.vulnerabilities
                    ]
                }
                for s in repo.scans
            ]
        }

    finally:
        db.close()