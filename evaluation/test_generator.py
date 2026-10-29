
import json
import random
from pathlib import Path


def reference_clean_transactions(transactions):
    """
    Reference implementation defining the expected transaction-cleaning
    behavior. Keeps the first valid transaction for each transaction ID.
    """

    cleaned = []
    seen_ids = set()

    for transaction in transactions:
        transaction_id = transaction.get("transaction_id")
        amount = transaction.get("amount")

        # Remove records with missing IDs or amounts.
        if transaction_id is None or amount is None:
            continue

        # Keep only the first valid record for each transaction ID.
        if transaction_id in seen_ids:
            continue

        seen_ids.add(transaction_id)
        cleaned.append(transaction.copy())

    return cleaned


def generate_baseline_test_cases():
    """Return the eight core scenarios used by the evaluation project."""

    return [
        {
            "name": "Normal transaction",
            "input": [{"transaction_id": 1, "amount": 100}],
            "expected": [{"transaction_id": 1, "amount": 100}],
        },
        {
            "name": "Duplicate transaction IDs",
            "input": [
                {"transaction_id": 1, "amount": 100},
                {"transaction_id": 1, "amount": 100},
            ],
            "expected": [{"transaction_id": 1, "amount": 100}],
        },
        {
            "name": "Zero transaction amount",
            "input": [{"transaction_id": 2, "amount": 0}],
            "expected": [{"transaction_id": 2, "amount": 0}],
        },
        {
            "name": "Missing transaction ID",
            "input": [{"transaction_id": None, "amount": 100}],
            "expected": [],
        },
        {
            "name": "Missing transaction amount",
            "input": [{"transaction_id": 3, "amount": None}],
            "expected": [],
        },
        {
            "name": "Empty transaction list",
            "input": [],
            "expected": [],
        },
        {
            "name": "Negative transaction amount",
            "input": [{"transaction_id": 4, "amount": -50}],
            "expected": [{"transaction_id": 4, "amount": -50}],
        },
        {
            "name": "Keep first duplicate transaction",
            "input": [
                {"transaction_id": 5, "amount": 100},
                {"transaction_id": 5, "amount": 250},
            ],
            "expected": [{"transaction_id": 5, "amount": 100}],
        },
    ]


def generate_random_test_cases(count=20, seed=42):
    """
    Generate reproducible random transaction-cleaning test cases.

    Using a fixed seed makes debugging and reproducing failures easier.
    """

    rng = random.Random(seed)
    test_cases = []

    amount_options = [
        None, -100, -1, 0, 1, 25, 100, 500
    ]

    for case_number in range(1, count + 1):
        transactions = []

        # Generate between zero and eight transactions per test case.
        transaction_count = rng.randint(0, 8)

        for _ in range(transaction_count):
            transaction = {
                "transaction_id": rng.choice(
                    [None, 1, 2, 3, 4, 5, 6, 7]
                ),
                "amount": rng.choice(amount_options),
            }

            # Sometimes omit a field entirely to test missing keys.
            if rng.random() < 0.10:
                transaction.pop("transaction_id", None)

            if rng.random() < 0.10:
                transaction.pop("amount", None)

            transactions.append(transaction)

        # Compute expected output using the reference implementation.
        expected = reference_clean_transactions(transactions)

        test_cases.append({
            "name": f"Random transaction case {case_number:02d}",
            "input": transactions,
            "expected": expected,
        })

    return test_cases


def generate_test_cases(random_count=20, seed=42):
    """Combine baseline scenarios with dynamically generated cases."""

    baseline_cases = generate_baseline_test_cases()
    random_cases = generate_random_test_cases(
        count=random_count,
        seed=seed,
    )

    return baseline_cases + random_cases


def save_test_cases(test_cases):
    """Save generated test cases as a JSON file."""

    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "generated_test_cases.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(test_cases, file, indent=4)

    print(f"Baseline test cases: 8")
    print(f"Random test cases: {len(test_cases) - 8}")
    print(f"Total test cases: {len(test_cases)}")
    print(f"Test cases saved to: {output_file}")


if __name__ == "__main__":
    cases = generate_test_cases(random_count=20, seed=42)

    save_test_cases(cases)

    print("\nFirst five test case names:")

    for number, case in enumerate(cases[:5], start=1):
        print(f"{number}. {case['name']}")
