from fastapi import FastAPI
from pydantic import BaseModel
from scanner.service import run_scan

app = FastAPI()


class ScanRequest(BaseModel):
    repo_url: str


@app.post("/scan")
def scan_repo(request: ScanRequest):
    return run_scan(request.repo_url)