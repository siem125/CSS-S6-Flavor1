import subprocess
import json
import tempfile
import shutil

if not shutil.which("grype"):
    raise RuntimeError(
        "Grype executable not found in PATH"
    )

def scan_vulnerabilities(sbom: dict) -> dict:
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
        json.dump(sbom, f)
        f.flush()

        result = subprocess.run(
            ["grype", f.name, "-o", "json"],
            capture_output=True,
            text=True
        )

    return json.loads(result.stdout)