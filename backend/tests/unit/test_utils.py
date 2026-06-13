from utils import clone_repo


def test_clone_repo_calls_git(mocker):

    mock_mkdtemp = mocker.patch(
        "utils.tempfile.mkdtemp",
        return_value="/tmp/testrepo"
    )

    mock_run = mocker.patch(
        "utils.subprocess.run"
    )

    mocker.patch(
        "utils.os.getenv",
        return_value="TOKEN123"
    )

    clone_repo(
        "https://github.com/user/repo"
    )

    mock_mkdtemp.assert_called_once()

    mock_run.assert_called_once()

    args = mock_run.call_args[0][0]

    assert args[0] == "git"
    assert args[1] == "clone"

    assert "TOKEN123" in args[2]