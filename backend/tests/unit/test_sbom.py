from sbom import generate_sbom


def test_generate_sbom_parses_json(mocker):

    mock_run = mocker.patch(
        "sbom.subprocess.run"
    )

    mock_run.return_value.stdout = """
    {
        "artifacts": []
    }
    """

    result = generate_sbom(
        "/tmp/repo"
    )

    assert "artifacts" in result