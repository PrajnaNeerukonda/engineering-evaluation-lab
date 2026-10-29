
import json
import subprocess
import sys

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from benchmarks.compare_candidates import (
    evaluate_candidates,
    load_test_cases,
    save_comparison,
)

REPORTS_DIR = ROOT_DIR / "reports"


def run_pytest():
    """Run the existing fixed pytest suite."""

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests/test_data_cleaning.py",
            "--tb=no",
            "-q",
        ],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        check=False,
    )

    return {
        "exit_code": result.returncode,
        "output": (result.stdout + result.stderr).strip(),
        "status": "PASS" if result.returncode == 0 else "FAIL",
    }


def save_json(filename, data):
    """Save a JSON report in the reports directory."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / filename

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Report saved to: {report_path.relative_to(ROOT_DIR)}")


def main():
    """Run evaluation and generate all required reports."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Generate or load the shared test cases.
    test_cases = load_test_cases()

    # Evaluate and rank all candidates using the same test cases.
    comparisons = evaluate_candidates(test_cases)

    # Preserve the full detailed candidate results.
    save_comparison(comparisons)

    # Run the independent pytest regression suite.
    pytest_result = run_pytest()

    # Candidate A is the intended correct reference implementation.
    reference_result = next(
        report
        for report in comparisons
        if report["candidate"] == "Candidate A"
    )

    errors = sum(
        1
        for result in reference_result["results"]
        if result["failure_reason"]
        and result["failure_reason"].startswith(
            "Candidate raised an exception:"
        )
    )

    scorecard = {
        "implementation": "transaction_cleaning",
        "total_tests": reference_result["total"],
        "passed_tests": reference_result["passed"],
        "failed_tests": reference_result["failed"],
        "errors": errors,
        "score": reference_result["score"],
        "status": (
            "PASS"
            if reference_result["failed"] == 0
            and pytest_result["exit_code"] == 0
            else "FAIL"
        ),
        "pytest_suite": pytest_result,
        "top_ranked_candidate": comparisons[0]["candidate"],
        "top_score": comparisons[0]["score"],
        "candidate_count": len(comparisons),
        "generated_test_count": len(test_cases),
    }

    save_json("scorecard.json", scorecard)

    print("\n=== Candidate Evaluation Summary ===")
    print(f"Generated test cases: {len(test_cases)}")

    for report in comparisons:
        print(
            f"Rank #{report['rank']}: {report['candidate']} | "
            f"{report['score']:.2f}% | "
            f"{report['passed']}/{report['total']} passed"
        )

    print("\n=== Pytest Suite ===")
    print(pytest_result["output"] or "No pytest output.")

    print("\n=== Evaluation Scorecard ===")
    print(json.dumps(scorecard, indent=4))

    # Intentional bugs in B and C should not fail the workflow.
    # Fail only if the reference implementation or regression suite fails.
    if scorecard["status"] != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
