
import json
import math
import statistics
import time
from pathlib import Path

from compare_candidates import CANDIDATES

ROOT_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT_DIR / "reports"
REPORT_FILE = REPORTS_DIR / "performance_benchmark.json"

DATASET_SIZE = 10_000
WARMUP_RUNS = 3
BENCHMARK_RUNS = 25


def generate_dataset(size=DATASET_SIZE):
    """Generate deterministic synthetic transaction records."""
    transactions = []

    for i in range(size):
        transaction = {
            "transaction_id": i // 2 if i % 10 == 0 else i,
            "amount": 0 if i % 100 == 0 else (i % 500) + 1,
        }

        # Include missing fields to exercise realistic edge cases.
        if i % 137 == 0:
            transaction.pop("transaction_id")

        if i % 149 == 0:
            transaction.pop("amount")

        transactions.append(transaction)

    return transactions


def reference_clean(transactions):
    """Independent reference implementation for correctness checks."""
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


def percentile(values, percentile_value):
    """Return a nearest-rank percentile."""
    ordered = sorted(values)
    index = max(
        0,
        math.ceil(percentile_value / 100 * len(ordered)) - 1,
    )
    return ordered[index]


def benchmark_candidate(name, function, transactions, expected):
    """Measure repeated runtime and check output correctness."""
    # Correctness is checked separately from the timed measurements.
    actual = function(transactions)

    correct = actual == expected

    # Warm up the function before collecting timings.
    for _ in range(WARMUP_RUNS):
        function(transactions)

    timings_ms = []

    for _ in range(BENCHMARK_RUNS):
        start = time.perf_counter()
        function(transactions)
        elapsed_ms = (time.perf_counter() - start) * 1000
        timings_ms.append(elapsed_ms)

    median_ms = statistics.median(timings_ms)
    average_ms = statistics.mean(timings_ms)
    p95_ms = percentile(timings_ms, 95)
    minimum_ms = min(timings_ms)
    maximum_ms = max(timings_ms)

    median_seconds = median_ms / 1000
    throughput = (
        len(transactions) / median_seconds
        if median_seconds > 0
        else None
    )

    return {
        "candidate": name,
        "correct": correct,
        "input_records": len(transactions),
        "expected_output_records": len(expected),
        "median_execution_time_ms": round(median_ms, 6),
        "average_execution_time_ms": round(average_ms, 6),
        "p95_execution_time_ms": round(p95_ms, 6),
        "min_execution_time_ms": round(minimum_ms, 6),
        "max_execution_time_ms": round(maximum_ms, 6),
        "throughput_input_records_per_second": (
            round(throughput, 2) if throughput is not None else None
        ),
        "benchmark_runs": BENCHMARK_RUNS,
        "warmup_runs": WARMUP_RUNS,
    }


def main():
    transactions = generate_dataset()
    expected = reference_clean(transactions)

    results = [
        benchmark_candidate(
            name,
            function,
            transactions,
            expected,
        )
        for name, function in CANDIDATES.items()
    ]

    # Correct implementations rank before incorrect implementations.
    # Within each group, median runtime is used as a tie-breaker.
    results.sort(
        key=lambda result: (
            result["correct"],
            -result["median_execution_time_ms"],
            result["candidate"],
        ),
        reverse=True,
    )

    for rank, result in enumerate(results, start=1):
        result["performance_rank"] = rank

    report = {
        "benchmark": "transaction_cleaning",
        "dataset_size": len(transactions),
        "expected_output_records": len(expected),
        "benchmark_runs": BENCHMARK_RUNS,
        "warmup_runs": WARMUP_RUNS,
        "ranking_rule": (
            "Correctness first, then lower median execution time."
        ),
        "results": results,
    }

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    with REPORT_FILE.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print(f"Performance report saved to: {REPORT_FILE.relative_to(ROOT_DIR)}")
    print(f"Input records: {len(transactions)}")
    print(f"Expected output records: {len(expected)}")
    print(f"Measured runs per candidate: {BENCHMARK_RUNS}")

    for result in results:
        print(
            f"Rank #{result['performance_rank']}: "
            f"{result['candidate']} | "
            f"Correct: {result['correct']} | "
            f"Median: {result['median_execution_time_ms']:.6f} ms | "
            f"P95: {result['p95_execution_time_ms']:.6f} ms | "
            f"Throughput: "
            f"{result['throughput_input_records_per_second']} records/s"
        )


if __name__ == "__main__":
    main()
