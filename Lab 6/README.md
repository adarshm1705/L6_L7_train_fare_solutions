# Lab 6: Code and Branch Coverage Analysis

## Objective
The objective of this lab is to understand the difference between **Code (Line) Coverage** and **Branch Coverage**, use Python's `coverage` and `pytest` libraries to measure and improve test coverage, and design targeted test suites to achieve **100% Line and Branch Coverage** for the `train_fare.py` application.

---

## Line Coverage vs. Branch Coverage

| Coverage Type | Definition | Key Question Answered | Limitations |
| :--- | :--- | :--- | :--- |
| **Line (Statement) Coverage** | Measures the percentage of executable code statements executed at least once during test execution. | *"Did execution pass through this line of code at least once?"* | Can give a false sense of security; does not check whether conditional branches were evaluated to both `True` and `False`. |
| **Branch Coverage** | Measures whether every decision branch (e.g. `if`, `elif`, `else`) evaluates to both `True` and `False`. | *"Did every control structure evaluate to all possible logical paths?"* | Requires testing boundary conditions, negative cases, and fallthroughs. |

---

## Coverage Progression Summary

| Stage | Test File | Tests Passed | Statement (Line) Coverage | Branch Coverage | Missing Lines / Branches |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Initial Baseline** | `test_train_fare.py` (starter) | 2 / 2 | **45%** | **40%** | Lines 6, 8, 11, 17, 19, 21, 23-25, 30-38 |
| **Code Coverage Milestone** | `CodeCoverageTest_train_fare.py` | 13 / 13 | **100%** (31/31) | **100%** | None (All 31 statements executed) |
| **Branch Coverage Milestone** | `BranchCoverageTest_train_fare.py` | 30 / 30 | **100%** (31/31) | **100%** (22/22) | None (All 22 branches fully exercised) |

---

## Detailed Logic & Decision Branch Analysis

### 1. `base_fare(travel_class, distance_km)`
* Rates per km: `{"SL": 1, "3A": 2, "2A": 3, "1A": 5}`
* Minimum fare clamp: `50`
* **Branches Tested:**
  * `travel_class not in RATE_PER_KM`: Tested `True` (raises `ValueError("unknown class")`) and `False` (all valid classes `SL`, `3A`, `2A`, `1A`).
  * `distance_km <= 0`: Tested `True` (boundary: `0`, `-10`, raises `ValueError("invalid distance")`) and `False` (`1`, `100`).
  * `fare < 50`: Tested `True` (`fare = 20, 49` -> clamped to `50`) and `False` (boundary: `50`, `51`).

### 2. `concession(age, gender, is_tatkal)`
* **Branches Tested:**
  * `is_tatkal`: Tested `True` (returns `0` for all demographics) and `False`.
  * `age < 5`: Tested `True` (`age = 2, 4` -> returns `100`) and `False` (boundary: `5`).
  * `age <= 12`: Tested `True` (`age = 5, 8, 12` -> returns `50`) and `False` (boundary: `13`).
  * `age >= 60`: Tested `True` (boundary: `60, 75`) and `False` (boundary: `59`).
  * `gender == "F"`: Tested `True` for senior women (`50%`) and `False` for senior men/others (`40%`).
  * Fallthrough: Tested general adult age range `13 <= age < 60` (returns `0`).

### 3. `tatkal_charge(travel_class, fare)`
* Minimum charge clamp: `100` | Maximum charge clamp: `400`
* **Branches Tested:**
  * `travel_class == "SL"` (`charge = fare // 10`):
    * `charge < 100`: `fare = 500, 990` -> returns `100`
    * Lower boundary: `fare = 1000` -> returns `100`
    * Normal range `[100, 400]`: `fare = 2000, 2500` -> returns `200, 250`
    * Upper boundary: `fare = 4000` -> returns `400`
    * `charge > 400`: `fare = 4010, 5000` -> returns `400`
  * `travel_class != "SL"` (`charge = fare * 3 // 10`):
    * `charge < 100`: `fare = 200` (`60 < 100`) -> returns `100`
    * Lower boundary: `fare = 334` -> returns `100`
    * Normal range `[100, 400]`: `fare = 1000` (`300`) -> returns `300`
    * Upper boundary: `fare = 1334` -> returns `400`
    * `charge > 400`: `fare = 2000` (`600 > 400`) -> returns `400`

---

## Commands to Run Tests & Generate Reports

### Run Line Coverage
```bash
coverage run -m pytest CodeCoverageTest_train_fare.py
coverage report -m
```

### Run Branch Coverage
```bash
coverage run --branch -m pytest BranchCoverageTest_train_fare.py
coverage report -m
```

### Run Full Combined Test Suite
```bash
coverage run --branch -m pytest test_train_fare.py
coverage report -m
```

---

## Deliverables
* **Code Coverage Test File:** `CodeCoverageTest_train_fare.py` (and alias `CodeCoverageTest_train_fare_application.py`)
* **Branch Coverage Test File:** `BranchCoverageTest_train_fare.py` (and alias `BranchCoverageTest_train_fare_application.py`)
* **Combined Test File:** `test_train_fare.py`
* **Terminal Output Screenshots:**
  * `screenshots/01_initial_coverage_missing_paths.png`
  * `screenshots/02_code_coverage_100_percent.png`
  * `screenshots/03_branch_coverage_100_percent.png`
* **PDF Report:** `Lab6_Coverage_Analysis_Report.pdf`
