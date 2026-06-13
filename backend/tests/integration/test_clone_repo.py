import pytest
import shutil
from utils import clone_repo


@pytest.mark.integration
def test_clone_public_repo():

    repo = "https://github.com/siem125/CSS-S6-Flavor1"

    path = clone_repo(repo)

    try:
        assert path is not None
        assert len(path) > 0
    finally:
        shutil.rmtree(path, ignore_errors=True)