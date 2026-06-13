from policy import evaluate_policy


def test_no_vulnerabilities():
    result = evaluate_policy({
        "matches": []
    })

    assert result["block"] is False
    assert result["critical"] == 0
    assert result["high"] == 0
    assert result["total"] == 0


def test_high_vulnerability_blocks():
    result = evaluate_policy({
        "matches": [
            {
                "vulnerability": {
                    "severity": "High"
                }
            }
        ]
    })

    assert result["block"] is True
    assert result["high"] == 1


def test_critical_vulnerability_blocks():
    result = evaluate_policy({
        "matches": [
            {
                "vulnerability": {
                    "severity": "Critical"
                }
            }
        ]
    })

    assert result["block"] is True
    assert result["critical"] == 1


def test_medium_does_not_block():
    result = evaluate_policy({
        "matches": [
            {
                "vulnerability": {
                    "severity": "Medium"
                }
            }
        ]
    })

    assert result["block"] is False