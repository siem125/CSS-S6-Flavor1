from service import run_scan

def test_run_scan(mocker):

    # mocker.patch(
    #     "service.clone_repo",
    #     return_value="/tmp/repo"
    # )

    # mocker.patch(
    #     "service.generate_sbom",
    #     return_value={}
    # )

    mocker.patch(
        "service.scan_vulnerabilities",
        return_value={
            "matches": [
                {
                    "vulnerability": {
                        "severity": "Critical"
                    }
                }
            ]
        }
    )

    mocker.patch(
        "service.evaluate_policy",
        return_value={
            "block": True
        }
    )

    mocker.patch(
        "service.shutil.rmtree"
    )

    result = run_scan(
        "https://github.com/test/repo"
    )

    assert result["status"] == "failure"