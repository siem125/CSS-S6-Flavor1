from service import run_scan


def test_run_scan_success(mocker):

    mocker.patch(
        "service.clone_repo",
        return_value="/tmp/repo"
    )

    mocker.patch(
        "service.generate_sbom",
        return_value={}
    )

    mocker.patch(
        "service.scan_vulnerabilities",
        return_value={
            "matches": []
        }
    )

    mocker.patch(
        "service.evaluate_policy",
        return_value={
            "block": False
        }
    )

    mocker.patch(
        "service.shutil.rmtree"
    )

    result = run_scan(
        "https://github.com/test/repo"
    )

    assert result["status"] == "success"