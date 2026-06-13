import pytest
import shutil

from utils import clone_repo
from sbom import generate_sbom


@pytest.mark.integration
def test_generate_real_sbom():

    path = clone_repo(
        "https://github.com/siem125/CSS-S6-Flavor1"
    )

    try:
        sbom = generate_sbom(path)

        assert isinstance(sbom, dict)

        # Syft output bevat vrijwel altijd artifacts
        assert "artifacts" in sbom

    finally:
        shutil.rmtree(path, ignore_errors=True)