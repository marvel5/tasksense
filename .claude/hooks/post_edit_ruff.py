"""PostToolUse hook: auto-fix and format an edited Python file, report what ruff cannot fix."""

import json
import subprocess
import sys
from pathlib import Path


def ruff(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "ruff", *args], capture_output=True, text=True, check=False
    )


def main() -> int:
    payload = json.load(sys.stdin)
    file_path = payload.get("tool_input", {}).get("file_path", "")
    if not file_path.endswith(".py") or not Path(file_path).exists():
        return 0

    ruff("check", "--fix", "--quiet", file_path)
    ruff("format", "--quiet", file_path)
    result = ruff("check", "--output-format", "concise", file_path)
    if result.returncode != 0:
        print(f"ruff found issues it cannot auto-fix:\n{result.stdout}", file=sys.stderr)
        return 2  # exit code 2 feeds stderr back to Claude
    return 0


if __name__ == "__main__":
    sys.exit(main())
