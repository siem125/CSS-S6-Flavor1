from vuln import scan_vulnerabilities


def test_scan_vulnerabilities_parses_json(
    mocker
):

    mock_run = mocker.patch(
        "vuln.subprocess.run"
    )

    mock_run.return_value.stdout = """
    {
        "matches": []
    }
    """

    result = scan_vulnerabilities({})

    assert result["matches"] == []