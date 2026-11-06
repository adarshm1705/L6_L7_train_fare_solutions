# Train Fare Solutions — Lab 6 & Lab 7

Comprehensive solutions for **Lab 6 (Code and Branch Coverage Analysis)** and **Lab 7 (Fuzzing for Input Validation Bugs)** based on the Train Fare Application.

---

## Repository Structure

```
L6_L7_train_fare_solutions/
├── .gitignore
├── README.md                                # Root repository documentation
│
├── Lab 6/                                   # Lab 6: Code & Branch Coverage Analysis
│   ├── README.md                            # Detailed Lab 6 explanation and analysis
│   ├── train_fare.py                        # Application under test
│   ├── test_train_fare.py                   # Combined comprehensive test suite (100% coverage)
│   ├── CodeCoverageTest_train_fare.py       # Code coverage test suite (100% line coverage)
│   ├── CodeCoverageTest_train_fare_application.py  # Rubric deliverable filename alias
│   ├── BranchCoverageTest_train_fare.py     # Branch coverage test suite (100% branch coverage)
│   ├── BranchCoverageTest_train_fare_application.py # Rubric deliverable filename alias
│   ├── Lab6_Coverage_Analysis_Report.pdf    # Deliverable PDF report with metrics & screenshots
│   └── screenshots/
│       ├── 01_initial_coverage_missing_paths.png
│       ├── 02_code_coverage_100_percent.png
│       └── 03_branch_coverage_100_percent.png
│
└── Lab 7/                                   # Lab 7: Fuzz Testing with Hypothesis
    ├── README.md                            # Detailed Lab 7 explanation and bug catalog
    ├── train_fare_buggy.py                  # Original buggy script preserved for reference
    ├── train_fare.py                        # Defensively hardened application script
    ├── test_train_fare.py                   # Hypothesis property-based fuzz tests
    ├── processor.py                         # Handout name alias
    ├── test_processor.py                    # Handout test alias
    ├── Lab7_Fuzz_Testing_Report.pdf         # Deliverable PDF document with screenshots
    └── screenshots/
        ├── step2_run_buggy_application.png
        ├── step4_fuzz_tests_failing.png
        ├── step5_run_fixed_application.png
        └── step6_fuzz_tests_passing.png
```

---

## Lab Summaries

### Lab 6: Code and Branch Coverage Analysis

* **Application:** Calculates base fare by travel class and distance, applies demographic concessions, and computes Tatkal surcharges.
* **Coverage Progression:**
  * **Initial Baseline:** `45%` Line Coverage, `40%` Branch Coverage (17 lines missing).
  * **Code Coverage Suite (`CodeCoverageTest_train_fare.py`):** **100% Line Coverage** (31/31 statements).
  * **Branch Coverage Suite (`BranchCoverageTest_train_fare.py`):** **100% Branch Coverage** (22/22 branches).
* **Key Concepts Illustrated:**
  * Statement coverage only ensures a line is touched; branch coverage ensures all conditional decisions (`if/else/elif`) evaluate to both `True` and `False`.
  * Comprehensive boundary value analysis on ticket classes (`SL`, `3A`, `2A`, `1A`), fare thresholds (`< 50`), age groups (`< 5`, `<= 12`, `>= 60`), genders, and Tatkal charge limits (`100` to `400`).

### Lab 7: Fuzzing for Input Validation Bugs

* **Objective:** Use the Hypothesis fuzzing framework to expose unexpected crashes in `parse_pnr`, `journey_distance`, and `berth_type`, followed by defensive programming to harden the code.
* **Bugs Discovered:**
  1. `parse_pnr`: Unhandled `IndexError` on empty strings `""`, `TypeError` on `None`, `ValueError` on non-digits.
  2. `journey_distance`: Unhandled `AttributeError` on `None`, `ValueError` on empty tokens `""`, single-station inputs, and negative distances.
  3. `berth_type`: Unhandled `AttributeError` on `None`, `ValueError` on missing delimiters or multiple hyphens, and invalid/non-numeric seat numbers.
* **Defensive Hardening:**
  * Added type validation (`isinstance(..., str)`), delimiter checks, whitespace trimming, digit verification, and logical boundaries.
  * Re-running Hypothesis tests verified that all functions are **100% crash-proof** against arbitrary inputs while preserving valid functionality.

---

## Quickstart & Commands

### Prerequisites
```bash
pip install coverage hypothesis pytest reportlab pillow
```

### Running Lab 6
```bash
cd "Lab 6"

# Run Line Coverage
coverage run -m pytest CodeCoverageTest_train_fare.py
coverage report -m

# Run Branch Coverage
coverage run --branch -m pytest BranchCoverageTest_train_fare.py
coverage report -m
```

### Running Lab 7
```bash
cd "Lab 7"

# Run interactive script
python train_fare.py

# Run Hypothesis Fuzz Tests
pytest test_train_fare.py
```
