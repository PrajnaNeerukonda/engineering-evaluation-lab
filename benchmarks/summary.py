
import json
from pathlib import Path


def generate_summary(report_path):
    """Read candidate results and rank candidates by score."""

    report_file = Path(report_path)

    if not report_file.exists():
        raise FileNotFoundError(
            f"Evaluation report not found: {report_file}"
        )

    with report_file.open("r", encoding="utf-8") as file:
        candidates = json.load(file)

    if not isinstance(candidates, list):
        raise ValueError("Expected a list of candidate reports.")

    # Highest score first; candidate name breaks ties consistently.
    candidates.sort(
        key=lambda candidate: (
            -candidate.get("score", 0),
            candidate.get("candidate", ""),
        )
    )

    print("\n" + "=" * 55)
    print("       ENGINEERING EVALUATION SUMMARY")
    print("=" * 55)

    if not candidates:
        print("No candidates found.")
        return

    for rank, candidate in enumerate(candidates, start=1):
        name = candidate.get("candidate", "Unknown")
        score = candidate.get("score", 0)
        passed = candidate.get("passed", 0)
        failed = candidate.get("failed", 0)
        total = candidate.get("total", 0)

        print(f"\nRank: #{rank} - {name}")
        print(f"Score: {score}%")
        print(f"Tests passed: {passed}/{total}")
        print(f"Tests failed: {failed}/{total}")

        failed_tests = [
            result
            for result in candidate.get("results", [])
            if result.get("status") == "FAIL"
        ]

        if failed_tests:
            print("Failed tests:")

            for test in failed_tests:
                test_name = test.get("test", "Unnamed test")
                reason = test.get(
                    "failure_reason",
                    "No failure details available."
                )

                print(f"  - {test_name}")
                print(f"    Reason: {reason}")
        else:
            print("Failed tests: None")

    winner = candidates[0]

    print("\n" + "=" * 55)
    print(f"TOP-RANKED CANDIDATE: {winner.get('candidate', 'Unknown')}")
    print(f"TOP SCORE: {winner.get('score', 0)}%")
    print("=" * 55)


if __name__ == "__main__":
    report_path = (
        Path(__file__).resolve().parent.parent
        / "reports"
        / "candidate_comparison.json"
    )

    try:
        generate_summary(report_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}")
        raise SystemExit(1)
