
import json
import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run pytest and collect the actual test results."""

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_data_cleaning.py",
            "--tb=no",
            "-q",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    output = result.stdout + result.stderr

    # Find pytest's summary, such as "5 passed in 0.03s".
    passed = 0
    failed = 0
    errors = 0

    for line in output.splitlines():
        if " passed" in line or " failed" in line or " error" in line:
            for part in line.split():
                if part.isdigit():
                    if "passed" in line:
                        passed = int(part)
                    if "failed" in line:
                        failed = int(part)
                    if "error" in line:
                        errors = int(part)

    total = passed + failed + errors

    score = (
        round(passed / total * 100, 2)
        if total > 0
        else 0
    )

    scorecard = {
        "implementation": "transaction_cleaning",
        "total_tests": total,
        "passed_tests": passed,
        "failed_tests": failed,
        "errors": errors,
        "score": score,
        "status": "PASS" if total > 0 and failed == 0 and errors == 0 else "FAIL",
    }

    return scorecard, result.returncode


def save_scorecard(scorecard):
    """Save the results as a JSON report."""

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    report_path = reports_dir / "scorecard.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(scorecard, file, indent=4)

    print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    scorecard, test_exit_code = run_tests()

    print("\n=== Evaluation Scorecard ===")
    print(json.dumps(scorecard, indent=4))

    save_scorecard(scorecard)

    if test_exit_code != 0:
        sys.exit(1)
