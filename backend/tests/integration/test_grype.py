import pytest
import shutil

from utils import clone_repo
from sbom import generate_sbom
from vuln import scan_vulnerabilities


@pytest.mark.integration
def test_grype_scan_runs():

    path = clone_repo(
        "https://github.com/siem125/CSS-S6-Flavor1"
    )

    try:

        sbom = generate_sbom(path)

        vulns = scan_vulnerabilities(sbom)

        assert isinstance(vulns, dict)

        assert "matches" in vulns

    finally:
        shutil.rmtree(path, ignore_errors=True)