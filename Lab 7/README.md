# Lab 7: Fuzzing for Input Validation Bugs

## Objective
The objective of this lab is to explore **Fuzz Testing** as an essential security and quality assurance technique by identifying and fixing input validation vulnerabilities and unhandled crashes in `train_fare.py` using Python's **Hypothesis** property-based testing library.

---

## What is Fuzzing & Why Hypothesis?

* **Fuzz Testing:** A dynamic testing technique where semi-random, unexpected, boundary, or malformed inputs are automatically fed into a program to find unhandled exceptions, memory errors, or security flaws.
* **Why Fuzzing over Manual Unit Tests?**
  * Manual tests test what the developer *expects*.
  * Fuzz testing tests what the developer *never anticipated* (e.g. empty strings, `None`, Unicode control sequences, extreme lengths, partial delimiters).
* **Hypothesis Framework:** Automatically generates hundreds of randomized test inputs according to specified strategies (e.g. `st.text() | st.none()`) and **minimizes (shrinks)** failing inputs to the simplest reproduction case (e.g. `s=''`).

---

## Bugs Discovered via Hypothesis Fuzzing

| Function | Malformed Input | Unhandled Exception in Buggy Code | Root Cause |
| :--- | :--- | :--- | :--- |
| **`parse_pnr(pnr)`** | `None`<br>`""`<br>`"abc"`<br>`"1"` | `TypeError`<br>`IndexError: string index out of range`<br>`ValueError`<br>`ValueError` | Assumed non-empty string with at least 2 characters, all numeric, with no type or length validation. |
| **`journey_distance(csv)`** | `None`<br>`""`<br>`"100"`<br>`"0,,300"`<br>`"300,100"` | `AttributeError: 'NoneType' object has no attribute 'split'`<br>`ValueError: invalid literal for int()`<br>Invalid single-station calculation<br>`ValueError`<br>Negative distance calculation | Directly called `.split(',')` without checking `None` or length; directly passed raw strings to `int()`. |
| **`berth_type(seat)`** | `None`<br>`""`<br>`"S3"`<br>`"S3-45-extra"`<br>`"S3-abc"`<br>`"S3-0"` | `AttributeError`<br>`ValueError: not enough values to unpack`<br>`ValueError: not enough values to unpack`<br>`ValueError: too many values to unpack`<br>`ValueError: invalid literal for int()`<br>Seat number 0 allowed | Assumed exactly one hyphen delimiter, valid coach name, and positive integer seat number without defensive parsing. |

---

## Defensive Hardening Applied

### 1. Hardened `parse_pnr(pnr)`
* Checks `isinstance(pnr, str)`.
* Strips leading and trailing whitespace.
* Ensures length is exactly 10 digits (`len(pnr) == 10 and pnr.isdigit()`).
* Returns `(int(pnr[0]), int(pnr[1:]))` if valid; returns `None` safely if invalid.

### 2. Hardened `journey_distance(distances_csv)`
* Checks `isinstance(distances_csv, str)`.
* Splits by comma and verifies at least 2 station distance entries (`len(parts) >= 2`).
* Safely parses integers, ensuring non-empty and valid integer formats.
* Validates that distances are non-decreasing (`distances[-1] >= distances[0]`).
* Returns `distances[-1] - distances[0]` if valid; returns `None` safely if invalid.

### 3. Hardened `berth_type(seat)`
* Checks `isinstance(seat, str)`.
* Splits by `'-'` and verifies exactly 2 components (`len(parts) == 2`).
* Validates non-empty coach name and positive integer seat number (`seat_num > 0`).
* Returns `(coach.upper(), BERTHS[seat_num % 8])` if valid; returns `None` safely if invalid.

---

## Lab Execution Steps & Outputs

### Step 2: Run Buggy Application
```bash
python train_fare.py
```
* **Valid input:** Successfully produces output.
* **Malformed input (e.g. empty string):** Crashes with `IndexError: string index out of range`.
* **Screenshot:** `screenshots/step2_run_buggy_application.png`

### Step 4: Run Fuzz Tests Against Buggy Code
```bash
pytest test_train_fare.py
```
* **Result:** All 3 Hypothesis property-based fuzz tests fail with minimal falsifying examples (`s=''`).
* **Screenshot:** `screenshots/step4_fuzz_tests_failing.png`

### Step 5: Run Defensively Hardened Application
```bash
python train_fare.py
```
* **Result:** Successfully handles both valid inputs and invalid/malformed inputs, returning `None` gracefully without crashing.
* **Screenshot:** `screenshots/step5_run_fixed_application.png`

### Step 6: Re-Run Fuzz Tests Against Hardened Code
```bash
pytest test_train_fare.py
```
* **Result:** All tests **PASSED** (100% success across hundreds of fuzzing iterations).
* **Screenshot:** `screenshots/step6_fuzz_tests_passing.png`

---

## Deliverables
1. **Fixed Application Python Script:** `train_fare.py` (and alias `processor.py`)
2. **Updated Fuzz Test Code:** `test_train_fare.py` (and alias `test_processor.py`)
3. **Preserved Buggy Application:** `train_fare_buggy.py`
4. **Terminal Output Screenshots:** Saved in `screenshots/`
5. **PDF Deliverable Document:** `Lab7_Fuzz_Testing_Report.pdf`
