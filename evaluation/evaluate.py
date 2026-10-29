
import json
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from benchmarks.compare_candidates import (
    candidate_a,
    candidate_b,
    candidate_c,
)

ROOT_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT_DIR / "reports"
TEST_CASES_FILE = REPORTS_DIR / "generated_test_cases.json"


def load_test_cases():
    """Load generated test cases, creating the report if necessary."""

    if not TEST_CASES_FILE.exists():
        generator = ROOT_DIR / "evaluation" / "test_generator.py"

        result = subprocess.run(
            [sys.executable, str(generator)],
            cwd=ROOT_DIR,
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Test generation failed:\n{result.stdout}\n{result.stderr}"
            )

    with TEST_CASES_FILE.open("r", encoding="utf-8") as file:
        test_cases = json.load(file)

    if not isinstance(test_cases, list) or not test_cases:
        raise ValueError("Generated test cases must be a non-empty JSON list.")

    for index, test in enumerate(test_cases, start=1):
        if not isinstance(test, dict):
            raise ValueError(f"Test case {index} must be a JSON object.")

        for key in ("name", "input", "expected"):
            if key not in test:
                raise ValueError(
                    f"Test case {index} is missing the '{key}' field."
                )

        if not isinstance(test["input"], list):
            raise ValueError(
                f"Test case {index} must have a list as its input."
            )

    return test_cases


def evaluate_candidate(name, function, test_cases):
    """Evaluate one implementation against every generated test case."""

    passed = 0
    results = []

    for test in test_cases:
        error = None

        try:
            # Copy inputs so a candidate cannot modify the test fixture.
            test_input = [item.copy() for item in test["input"]]
            actual = function(test_input)
            expected = test["expected"]
            success = actual == expected

        except Exception as exc:
            actual = None
            expected = test["expected"]
            success = False
            error = f"{type(exc).__name__}: {exc}"

        if success:
            passed += 1
            failure_reason = None
        elif error:
            failure_reason = f"Candidate raised an exception: {error}"
        else:
            failure_reason = (
                "Actual output does not match expected output."
            )

        results.append({
            "test": test["name"],
            "status": "PASS" if success else "FAIL",
            "expected": expected,
            "actual": actual,
            "failure_reason": failure_reason,
        })

    total = len(test_cases)
    failed = total - passed

    return {
        "candidate": name,
        "passed": passed,
        "failed": failed,
        "total": total,
        "score": round(passed / total * 100, 2) if total else 0,
        "results": results,
    }


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
    """Run tests, compare candidates, and create evaluation reports."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    test_cases = load_test_cases()

    candidates = {
        "Candidate A": candidate_a,
        "Candidate B": candidate_b,
        "Candidate C": candidate_c,
    }

    # Evaluate all candidates against exactly the same test cases.
    comparisons = [
        evaluate_candidate(name, function, test_cases)
        for name, function in candidates.items()
    ]

    # Rank by score, then by number of passing tests.
    comparisons.sort(
        key=lambda report: (report["score"], report["passed"]),
        reverse=True,
    )

    for rank, report in enumerate(comparisons, start=1):
        report["rank"] = rank

    # Candidate A is the intended correct implementation.
    reference_result = next(
        report for report in comparisons
        if report["candidate"] == "Candidate A"
    )

    pytest_result = run_pytest()

    scorecard = {
        "implementation": "transaction_cleaning",
        "total_tests": reference_result["total"],
        "passed_tests": reference_result["passed"],
        "failed_tests": reference_result["failed"],
        "errors": sum(
            1
            for result in reference_result["results"]
            if result["failure_reason"]
            and "raised an exception" in result["failure_reason"]
        ),
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
    }

    save_json("candidate_comparison.json", comparisons)
    save_json("scorecard.json", scorecard)

    print("\n=== Candidate Evaluation Summary ===")
    print(f"Generated test cases: {len(test_cases)}")

    for report in comparisons:
        print(
            f"Rank #{report['rank']}: {report['candidate']} | "
            f"{report['score']}% | "
            f"{report['passed']}/{report['total']} passed"
        )

    print("\n=== Pytest Suite ===")
    print(pytest_result["output"])

    print("\n=== Evaluation Scorecard ===")
    print(json.dumps(scorecard, indent=4))

    # Intentional bugs in Candidates B and C do not fail the workflow.
    # The workflow fails if Candidate A or the fixed pytest suite fails.
    if scorecard["status"] != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
