
import json
from pathlib import Path


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


# Candidate C: Bug - removes zero amounts
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


# Same test cases for every candidate
test_cases = [
    {
        "name": "Remove duplicate transactions",
        "input": [
            {"transaction_id": 1, "amount": 100},
            {"transaction_id": 1, "amount": 100},
        ],
        "expected": [
            {"transaction_id": 1, "amount": 100},
        ],
    },
    {
        "name": "Keep zero amount",
        "input": [
            {"transaction_id": 2, "amount": 0},
        ],
        "expected": [
            {"transaction_id": 2, "amount": 0},
        ],
    },
    {
        "name": "Remove missing values",
        "input": [
            {"transaction_id": None, "amount": 100},
        ],
        "expected": [],
    },
    {
        "name": "Keep first duplicate",
        "input": [
            {"transaction_id": 5, "amount": 100},
            {"transaction_id": 5, "amount": 250},
        ],
        "expected": [
            {"transaction_id": 5, "amount": 100},
        ],
    },
    {
        "name": "Handle empty input",
        "input": [],
        "expected": [],
    },
]


def evaluate_candidate(name, function):
    passed = 0
    results = []

    for test in test_cases:
        try:
            actual = function(test["input"])
            success = actual == test["expected"]
            error = None
        except Exception as exc:
            success = False
            error = str(exc)

        if success:
            passed += 1

        results.append({
            "test": test["name"],
            "status": "PASS" if success else "FAIL",
            "error": error,
        })

    total = len(test_cases)

    return {
        "candidate": name,
        "passed": passed,
        "failed": total - passed,
        "total": total,
        "score": round(passed / total * 100, 2),
        "results": results,
    }


if __name__ == "__main__":
    candidates = {
        "Candidate A": candidate_a,
        "Candidate B": candidate_b,
        "Candidate C": candidate_c,
    }

    reports = []

    for name, function in candidates.items():
        report = evaluate_candidate(name, function)
        reports.append(report)

        print(f"{name}: {report['score']}%")

    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "candidate_comparison.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(reports, file, indent=4)

    print(f"Report saved to: {output_file}")
