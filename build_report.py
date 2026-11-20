
import json
import os
from datetime import datetime, timezone
from pathlib import Path

source = Path("pytest-report.json")

raw = (
    json.loads(source.read_text(encoding="utf-8"))
    if source.exists()
    else {}
)

tests = []

for item in raw.get("tests", []):
    outcome = item.get("outcome", "unknown")
    call = item.get("call", {})

    longrepr = (
        call.get("crash", {}).get("message")
        or call.get("longrepr", "")
    )

    result = (
        "passed" if outcome == "passed"
        else "failed" if outcome in ("failed", "error")
        else outcome
    )

    tests.append({
        "name": item.get("nodeid", "unknown"),
        "result": result,
        "failure_message": (
            str(longrepr) if result == "failed" else ""
        )
    })

total = len(tests)
passed = sum(t["result"] == "passed" for t in tests)
failed = sum(t["result"] == "failed" for t in tests)

report = {
    "repository": os.environ.get("GITHUB_REPOSITORY", "local"),
    "branch": os.environ.get("GITHUB_REF_NAME", "local"),
    "commit_sha": os.environ.get("GITHUB_SHA", "local"),
    "pipeline_run_id": os.environ.get("GITHUB_RUN_ID", "local"),
    "execution_timestamp": datetime.now(timezone.utc).isoformat(),
    "tests": tests,
    "total": total,
    "passed": passed,
    "failed": failed,
    "overall_status": (
        "passed" if failed == 0 and total > 0 else "failed"
    )
}

Path("test-report.json").write_text(
    json.dumps(report, indent=2),
    encoding="utf-8"
)

print(json.dumps(report, indent=2))
