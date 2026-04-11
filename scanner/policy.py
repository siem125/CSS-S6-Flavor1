def evaluate_policy(vuln_data: dict) -> dict:
    matches = vuln_data.get("matches", [])

    critical = []
    high = []

    for m in matches:
        severity = m["vulnerability"]["severity"]

        if severity == "Critical":
            critical.append(m)
        elif severity == "High":
            high.append(m)

    block = len(critical) > 0 or len(high) > 5

    return {
        "block": block,
        "critical": len(critical),
        "high": len(high),
        "total": len(matches)
    }