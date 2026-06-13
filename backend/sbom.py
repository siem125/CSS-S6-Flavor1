import subprocess
import json
import shutil

if not shutil.which("syft"):
    raise RuntimeError(
        "Syft executable not found in PATH"
    )

def generate_sbom(path: str) -> dict:
    result = subprocess.run(
        ["syft", path, "-o", "json"],
        capture_output=True,
        text=True
    )

    return json.loads(result.stdout)