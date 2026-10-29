
import json
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT_DIR / "reports"
OUTPUT_FILE = REPORTS_DIR / "generated_test_cases.json"


def generate_test_cases():
    """
    Generate transaction-cleaning benchmark test cases.

    Expected behavior:
    - Remove transactions with missing IDs or amounts.
    - Remove duplicate transaction IDs.
    - Keep the first valid transaction for each ID.
    - Preserve zero and negative amounts.
    - Preserve the order of retained transactions.
    """

    return [
        {
            "name": "Normal transaction",
            "input": [
                {"transaction_id": 1, "amount": 100}
            ],
            "expected": [
                {"transaction_id": 1, "amount": 100}
            ],
        },
        {
            "name": "Duplicate transaction IDs",
            "input": [
                {"transaction_id": 1, "amount": 100},
                {"transaction_id": 1, "amount": 100},
            ],
            "expected": [
                {"transaction_id": 1, "amount": 100}
            ],
        },
        {
            "name": "Zero transaction amount",
            "input": [
                {"transaction_id": 2, "amount": 0}
            ],
            "expected": [
                {"transaction_id": 2, "amount": 0}
            ],
        },
        {
            "name": "Missing transaction ID",
            "input": [
                {"transaction_id": None, "amount": 100}
            ],
            "expected": [],
        },
        {
            "name": "Missing transaction amount",
            "input": [
                {"transaction_id": 3, "amount": None}
            ],
            "expected": [],
        },
        {
            "name": "Empty transaction list",
            "input": [],
            "expected": [],
        },
        {
            "name": "Negative transaction amount",
            "input": [
                {"transaction_id": 4, "amount": -50}
            ],
            "expected": [
                {"transaction_id": 4, "amount": -50}
            ],
        },
        {
            "name": "Keep first duplicate transaction",
            "input": [
                {"transaction_id": 5, "amount": 100},
                {"transaction_id": 5, "amount": 250},
            ],
            "expected": [
                {"transaction_id": 5, "amount": 100}
            ],
        },

        # Additional edge cases
        {
            "name": "Missing transaction ID field",
            "input": [
                {"amount": 100}
            ],
            "expected": [],
        },
        {
            "name": "Missing transaction amount field",
            "input": [
                {"transaction_id": 6}
            ],
            "expected": [],
        },
        {
            "name": "Mixed valid and invalid transactions",
            "input": [
                {"transaction_id": 7, "amount": 100},
                {"transaction_id": None, "amount": 200},
                {"transaction_id": 8, "amount": None},
                {"transaction_id": 9, "amount": 300},
            ],
            "expected": [
                {"transaction_id": 7, "amount": 100},
                {"transaction_id": 9, "amount": 300},
            ],
        },
        {
            "name": "Duplicate ID with different amounts",
            "input": [
                {"transaction_id": 10, "amount": 100},
                {"transaction_id": 10, "amount": 450},
                {"transaction_id": 11, "amount": 200},
            ],
            "expected": [
                {"transaction_id": 10, "amount": 100},
                {"transaction_id": 11, "amount": 200},
            ],
        },
        {
            "name": "Duplicate ID after invalid transaction",
            "input": [
                {"transaction_id": 12, "amount": None},
                {"transaction_id": 12, "amount": 80},
                {"transaction_id": 12, "amount": 150},
            ],
            "expected": [
                {"transaction_id": 12, "amount": 80}
            ],
        },
    ]


def save_test_cases(test_cases):
    """Save generated test cases to the reports directory."""

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(test_cases, file, indent=4)

    print(f"Generated {len(test_cases)} test cases.")
    print(f"Test cases saved to: {OUTPUT_FILE}")


def main():
    test_cases = generate_test_cases()
    save_test_cases(test_cases)

    print("\nGenerated test case names:")

    for number, test in enumerate(test_cases, start=1):
        print(f"{number}. {test['name']}")


if __name__ == "__main__":
    main()
