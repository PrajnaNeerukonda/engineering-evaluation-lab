# Engineering Evaluation Lab

A Python-based engineering evaluation framework that tests, compares, and scores multiple implementations against a shared set of test cases.

## Project Overview

This project demonstrates how to evaluate competing implementations using automated tests, generated test cases, candidate-level scoring, and continuous integration and deployment.

The framework uses transaction-data cleaning as a sample task. It evaluates three candidate implementations against 13 test cases, including duplicate transaction IDs, missing fields, zero amounts, negative amounts, and invalid transactions.

## Live Dashboard

**[View the live evaluation dashboard](https://prajneerukonda.github.io/engineering-evaluation-lab/)**

The dashboard displays candidate scores and test-by-test pass/fail results.

## Current Results

| Candidate | Pass Rate | Observation |
|---|---:|---|
| Candidate A | 100% | Passed all 13 test cases |
| Candidate B | 69.2% | Failed duplicate-handling scenarios |
| Candidate C | 92.3% | Failed the zero-amount scenario |

*Results reflect the current benchmark run and may change as the evaluation suite evolves.*

## Key Features

- **Automated evaluation:** Run multiple candidate implementations against a common test suite.
- **Test-case generation:** Generate test cases covering normal inputs and edge cases.
- **Candidate scoring:** Calculate pass rates and compare implementation quality.
- **Failure reporting:** Capture expected-versus-actual output differences.
- **Continuous integration:** Execute Python tests using GitHub Actions.
- **Continuous deployment:** Publish evaluation reports and the dashboard through GitHub Pages.

## Technology Stack

- Python
- pytest
- JSON
- GitHub Actions
- GitHub Pages
- HTML and CSS

## Repository Structure

```text
engineering-evaluation-lab/
├── .github/
│   └── workflows/
├── benchmarks/
│   ├── compare_candidates.py
│   └── summary.py
├── evaluation/
│   ├── evaluate.py
│   └── test_generator.py
├── tasks/
├── tests/
├── reports/
├── index.html
└── README.md
```

## Run Locally

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

### 4. Generate and run the evaluation

```bash
python evaluation/test_generator.py
python evaluation/evaluate.py
python benchmarks/compare_candidates.py
python benchmarks/summary.py
```

## Evaluation Methodology

Each candidate receives the same set of test cases. The framework compares the candidate's output against the expected result and calculates its pass rate.

The test suite covers:

- Normal transactions
- Duplicate IDs and duplicate handling
- Zero and negative amounts
- Missing transaction IDs and amounts
- Empty input lists
- Mixed valid and invalid records
- Duplicate IDs with different amounts

## Future Improvements

- Add execution-time and resource-usage measurements.
- Categorize failures by severity and test type.
- Add configurable evaluation tasks and scoring criteria.
- Expand the dashboard with performance charts and failure analysis.
- Add regression testing across multiple benchmark runs.

## Disclaimer

This is a portfolio project for demonstrating software testing and AI evaluation engineering concepts. The current benchmark uses transaction-data cleaning as its example task.
