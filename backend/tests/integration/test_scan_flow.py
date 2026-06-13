import pytest

from service import run_scan


@pytest.mark.integration
def test_full_scan_flow():

    result = run_scan(
        "https://github.com/siem125/CSS-S6-Flavor1"
    )

    assert "status" in result

    assert "duration" in result

    assert "severity_breakdown" in result

    assert "vulnerability_count" in result