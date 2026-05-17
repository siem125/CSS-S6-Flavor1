import shutil
import time

from utils import clone_repo
from sbom import generate_sbom
from vuln import scan_vulnerabilities
from policy import evaluate_policy


def run_scan(repo_url: str) -> dict:
    start = time.time()

    path = clone_repo(repo_url)

    try:
        sbom = generate_sbom(path)

        vulns = scan_vulnerabilities(sbom)

        policy_result = evaluate_policy(vulns)

        duration = round(time.time() - start, 2)

        return {
            "repo_url": repo_url,
            "status": "failure" if policy_result["block"] else "success",
            "block": policy_result["block"],
            "reason": policy_result.get("reason"),
            "duration": duration,
            "vulnerability_count": len(vulns),
            "vulnerabilities": vulns
        }

    finally:
        shutil.rmtree(path, ignore_errors=True)