# Engineering Evaluation Lab

A Python-based engineering evaluation framework for testing, comparing, and benchmarking competing implementations against a shared set of test cases.

The project demonstrates core software evaluation concepts, including automated test generation, correctness scoring, failure analysis, performance benchmarking, and continuous integration and deployment.

## Live Dashboard

**[View the AI Engineering Evaluation Dashboard](https://prajneerukonda.github.io/engineering-evaluation-lab/)**

The dashboard presents candidate rankings, correctness scores, individual test results, failure details, and performance measurements.

## Project Overview

This project uses transaction-data cleaning as a sample engineering task. Three candidate implementations are evaluated against 13 test cases covering normal transactions, duplicate IDs, missing fields, zero amounts, negative amounts, and other edge cases.

Each candidate receives the same test cases. Its output is compared with the expected result to determine correctness and calculate its pass rate.

A separate performance benchmark evaluates the candidates using a synthetic dataset of 10,000 transaction records, with warm-up runs and repeated timing measurements.

## Current Evaluation Results

| Candidate | Passed | Failed | Pass Rate | Key Observation |
|---|---:|---:|---:|---|
| Candidate A | 13 | 0 | 100% | Correctly handles the evaluated scenarios |
| Candidate B | 9 | 4 | 69.23% | Does not remove duplicate transactions |
| Candidate C | 12 | 1 | 92.31% | Incorrectly excludes zero-amount transactions |

*Results reflect the current evaluation suite and may change when the test cases or implementations are updated.*

## Key Features

- **Automated evaluation:** Execute multiple candidate implementations against a common test suite.
- **Test-case generation:** Generate scenarios covering normal inputs and edge cases.
- **Correctness scoring:** Calculate candidate pass rates and rank implementations.
- **Failure analysis:** Report expected and actual outputs, along with failure reasons.
- **Performance benchmarking:** Measure median, mean, P95, minimum, and maximum execution time, as well as input-record throughput.
- **Interactive dashboard:** Present evaluation results and benchmark comparisons in a browser.
- **Continuous integration:** Run automated Python tests using GitHub Actions.
- **Continuous deployment:** Publish the dashboard and generated JSON reports using GitHub Pages.

## Technology Stack

- Python
- pytest
- JSON
- HTML and CSS
- JavaScript
- GitHub Actions
- GitHub Pages

## Repository Structure

```text
engineering-evaluation-lab/
├── .github/
│   └── workflows/
│       ├── python-tests.yml
│       └── static.yml
├── benchmarks/
│   ├── compare_candidates.py
│   ├── summary.py
│   └── performance_benchmark.py
├── evaluation/
│   ├── evaluate.py
│   └── test_generator.py
├── tasks/
│   └── data_cleaning.py
├── tests/
│   └── test_data_cleaning.py
├── reports/
│   ├── generated_test_cases.json
│   ├── candidate_comparison.json
│   └── performance_benchmark.json
├── index.html
└── README.md
```

*The structure above reflects the project files discussed during development. Verify the actual repository before publishing, particularly if any workflow or source filenames differ.*

## Getting Started

### Prerequisites

- Python 3.10 or later
- Git

### 1. Clone the repository

```bash
git clone https://github.com/PrajnaNeerukonda/engineering-evaluation-lab.git
cd engineering-evaluation-lab
```

### 2. Install the test dependency

```bash
python -m pip install pytest
```

### 3. Run the automated tests

```bash
python -m pytest -v
```

### 4. Generate test cases and evaluate candidates

```bash
python evaluation/test_generator.py
python evaluation/evaluate.py
python benchmarks/compare_candidates.py
python benchmarks/summary.py
```

### 5. Run the performance benchmark

From the `benchmarks` directory, execute:

```bash
python performance_benchmark.py
```

Or, from the repository root:

```bash
python benchmarks/performance_benchmark.py
```

The benchmark performs three warm-up runs and 25 measured runs per candidate, then writes the results to `reports/performance_benchmark.json`.

## Evaluation Methodology

### Correctness evaluation

Each candidate is evaluated against the same 13 generated test cases. The framework compares actual outputs with expected outputs and records the result of each test.

The pass rate is calculated as:

\[
\text{Pass Rate} =
\frac{\text{Passed Tests}}{\text{Total Tests}} \times 100
\]

### Performance evaluation

The performance benchmark generates 10,000 synthetic transaction records and evaluates each candidate against an independent reference implementation.

It records:

- Median execution time
- Mean execution time
- 95th-percentile (P95) execution time
- Minimum and maximum execution time
- Input records processed per second
- Correctness against the reference output

The performance ranking prioritizes correctness first, followed by lower median execution time. An implementation that is faster but produces incorrect output should not be considered the best overall candidate.

**Benchmark note:** These measurements are preliminary microbenchmark results. Execution times and throughput can vary across machines and runtime conditions; they should not be interpreted as guaranteed production performance.

## Engineering Concepts Demonstrated

- Test-driven evaluation of competing implementations
- Edge-case and regression testing
- Automated test generation
- Correctness-based scoring and ranking
- Expected-versus-actual output comparison
- Performance
