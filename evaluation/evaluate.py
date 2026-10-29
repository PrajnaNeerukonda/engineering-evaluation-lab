import json
from pathlib import Path


def create_scorecard(
    implementation_name,
    total_tests,
    passed_tests,
    failed_tests,
):
    """Create a simple, structured evaluation scorecard."""

    score = (
        passed_tests / total_tests * 100
        if total_tests > 0
        else 0
    )

    return {
        "implementation": implementation_name,
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "score": round(score, 2),
        "status": "PASS" if failed_tests == 0 else "FAIL",
    }


def save_scorecard(scorecard):
    """Save the scorecard as a JSON report."""

    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    report_path = reports_dir / "scorecard.json"

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(scorecard, file, indent=4)

    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    scorecard = create_scorecard(
        implementation_name="transaction_cleaning_v1",
        total_tests=5,
        passed_tests=2,
        failed_tests=3,
    )

    print(json.dumps(scorecard, indent=4))
    save_scorecard(scorecard)
