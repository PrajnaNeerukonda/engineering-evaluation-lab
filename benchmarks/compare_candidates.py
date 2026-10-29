
import copy
import json
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT_DIR / "reports"
TEST_CASES_FILE = REPORTS_DIR / "generated_test_cases.json"
REPORT_FILE = REPORTS_DIR / "candidate_comparison.json"


# Candidate A: Correct implementation
def candidate_a(transactions):
    cleaned = []
    seen_ids = set()

    for transaction in transactions:
        transaction_id = transaction.get("transaction_id")
        amount = transaction.get("amount")

        if transaction_id is None or amount is None:
            continue

        if transaction_id in seen_ids:
            continue

        seen_ids.add(transaction_id)
        cleaned.append(transaction)

    return cleaned


# Candidate B: Bug - does not remove duplicates
def candidate_b(transactions):
    cleaned = []

    for transaction in transactions:
        if (
            transaction.get("transaction_id") is not None
            and transaction.get("amount") is not None
        ):
            cleaned.append(transaction)

    return cleaned


# Candidate C: Bug - incorrectly removes zero amounts
def candidate_c(transactions):
    cleaned = []
    seen_ids = set()

    for transaction in transactions:
        transaction_id = transaction.get("transaction_id")
        amount = transaction.get("amount")

        if transaction_id is None or not amount:
            continue

        if transaction_id in seen_ids:
            continue

        seen_ids.add(transaction_id)
        cleaned.append(transaction)

    return cleaned


CANDIDATES = {
    "Candidate A": candidate_a,
    "Candidate B": candidate_b,
    "Candidate C": candidate_c,
}


def load_test_cases():
    """Load the generated test cases, creating them if necessary."""

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
                f"Test generation failed:\n"
                f"{result.stdout}\n{result.stderr}"
            )

    with TEST_CASES_FILE.open("r", encoding="utf-8") as file:
        test_cases = json.load(file)

    if not isinstance(test_cases, list) or not test_cases:
        raise ValueError(
            "Generated test cases must be a non-empty JSON list."
        )

    required_fields = {"name", "input", "expected"}

    for index, test in enumerate(test_cases, start=1):
        if not isinstance(test, dict):
            raise ValueError(f"Test case {index} must be an object.")

        missing = required_fields - test.keys()

        if missing:
            raise ValueError(
                f"Test case {index} is missing fields: "
                f"{sorted(missing)}"
            )

        if not isinstance(test["name"], str) or not test["name"].strip():
            raise ValueError(f"Test case {index} needs a valid name.")

        if not isinstance(test["input"], list):
            raise ValueError(
                f"Test case {index} input must be a list."
            )

        if not isinstance(test["expected"], list):
            raise ValueError(
                f"Test case {index} expected output must be a list."
            )

    return test_cases


def evaluate_candidate(name, function, test_cases):
    """Evaluate a candidate against the same test cases as its peers."""

    results = []
    passed = 0

    for test in test_cases:
        expected = copy.deepcopy(test["expected"])
        actual = None
        error = None

        try:
            # Prevent a candidate from modifying the original fixtures.
            test_input = copy.deepcopy(test["input"])
            actual = function(test_input)
            success = actual == expected

        except Exception as exc:
            success = False
            error = f"{type(exc).__name__}: {exc}"

        if success:
            passed += 1
            failure_reason = None
        elif error:
            failure_reason = f"Candidate raised an exception: {error}"
        else:
            failure_reason = (
                f"Expected {expected!r}, but got {actual!r}"
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


def evaluate_candidates(test_cases):
    """Evaluate and rank every candidate using the same test set."""

    reports = [
        evaluate_candidate(name, function, test_cases)
        for name, function in CANDIDATES.items()
    ]

    # Use deterministic tie-breakers.
    reports.sort(
        key=lambda report: (
            report["score"],
            report["passed"],
            report["candidate"],
        ),
        reverse=True,
    )

    for rank, report in enumerate(reports, start=1):
        report["rank"] = rank

    return reports


def save_comparison(reports):
    """Save the complete candidate comparison report."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with REPORT_FILE.open("w", encoding="utf-8") as file:
        json.dump(reports, file, indent=4)

    print(f"Report saved to: {REPORT_FILE.relative_to(ROOT_DIR)}")


def main():
    test_cases = load_test_cases()
    reports = evaluate_candidates(test_cases)
    save_comparison(reports)

    print("\n=== Candidate Comparison ===")
    print(f"Test cases used: {len(test_cases)}")

    for report in reports:
        print(
            f"Rank #{report['rank']}: {report['candidate']} | "
            f"{report['score']:.2f}% | "
            f"{report['passed']}/{report['total']} passed"
        )


if __name__ == "__main__":
    main()
