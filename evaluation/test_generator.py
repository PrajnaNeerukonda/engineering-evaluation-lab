
import json
from pathlib import Path


def generate_test_cases():
    """
    Generate test cases automatically for transaction cleaning.
    """

    test_cases = [
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
    ]

    return test_cases


def save_test_cases(test_cases):
    """Save generated test cases as a JSON file."""

    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "generated_test_cases.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(test_cases, file, indent=4)

    print(f"Generated {len(test_cases)} test cases.")

    print(f"Test cases saved to: {output_file}")


if __name__ == "__main__":
    cases = generate_test_cases()

    save_test_cases(cases)

    print("\nGenerated test case names:")

    for number, case in enumerate(cases, start=1):
        print(f"{number}. {case['name']}")
