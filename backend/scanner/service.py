import shutil
import time

from backend.scanner.utils import clone_repo
from backend.scanner.sbom import generate_sbom
from backend.scanner.vuln import scan_vulnerabilities
from backend.scanner.policy import evaluate_policy


def run_scan(repo_url: str) -> dict:
    start = time.time()

    path = clone_repo(repo_url)

    try:
        sbom = generate_sbom(path)
        vulns = scan_vulnerabilities(sbom)
        result = evaluate_policy(vulns)

        duration = time.time() - start

        return {
            **result,
            "duration": round(duration, 2)
        }

    finally:
        # cleanup always runs
        shutil.rmtree(path, ignore_errors=True)