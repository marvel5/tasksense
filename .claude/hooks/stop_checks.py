"""Stop hook: block finishing while mypy or pytest fail on uncommitted Python changes."""

import json
import subprocess
import sys

MAX_OUTPUT_LINES = 40


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, capture_output=True, text=True, check=False)


def tail(output: str) -> str:
    return "\n".join(output.strip().splitlines()[-MAX_OUTPUT_LINES:])


def main() -> int:
    payload = json.load(sys.stdin)
    if payload.get("stop_hook_active"):
        return 0  # already continuing because of this hook; don't loop

    changed = run("git", "status", "--porcelain", "--", "*.py")
    if not changed.stdout.strip():
        return 0

    failures = []
    mypy = run(sys.executable, "-m", "mypy", "app", "tests")
    if mypy.returncode != 0:
        failures.append(f"mypy failed:\n{tail(mypy.stdout)}")
    pytest = run(sys.executable, "-m", "pytest", "-q", "--no-header")
    if pytest.returncode != 0:
        failures.append(f"pytest failed:\n{tail(pytest.stdout)}")

    if failures:
        print(json.dumps({"decision": "block", "reason": "\n\n".join(failures)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
