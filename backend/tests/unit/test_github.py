from github import set_commit_status


def test_set_commit_status(mocker):

    mock_post = mocker.patch(
        "github.requests.post"
    )

    mock_post.return_value.json.return_value = {
        "id": 123
    }

    result = set_commit_status(
        "owner/repo",
        "abc123",
        "success"
    )

    mock_post.assert_called_once()

    assert result["id"] == 123