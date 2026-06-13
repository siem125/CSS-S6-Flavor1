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

        #print(vulns)

        policy_result = evaluate_policy(vulns)

        duration = round(time.time() - start, 2)

        matches = vulns.get("matches", [])

        #Side information(bugfix vulns returning count as 4 due to matches)
        severity_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }

        for m in matches:
            sev = m["vulnerability"].get("severity", "").lower()
            if sev in severity_counts:
                severity_counts[sev] += 1

        #end matches count fix

        return {
            "repo_url": repo_url,
            "status": "failure" if policy_result["block"] else "success",
            "block": policy_result["block"],
            "reason": policy_result.get("reason"),
            "duration": duration,
            "vulnerability_count": len(matches),
            "severity_breakdown": severity_counts,
            "vulnerabilities": vulns #TODO: Maybe switch to matches
        }

    finally:
        shutil.rmtree(path, ignore_errors=True)