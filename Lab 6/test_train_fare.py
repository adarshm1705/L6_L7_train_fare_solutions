"""
test_train_fare.py

Starter test file extended to achieve 100% Code and Branch Coverage.
Includes original test cases and covers all classes, boundaries, and concessions.
"""

import pytest
from train_fare import base_fare, concession, tatkal_charge


# ==========================================
# Original Example Test Cases
# ==========================================

def test_sleeper_fare():
    assert base_fare("SL", 500) == 500


def test_adult_no_concession():
    assert concession(30, "M", False) == 0


# ==========================================
# Extended Test Cases for 100% Coverage
# ==========================================

def test_base_fare_all_classes():
    assert base_fare("3A", 100) == 200
    assert base_fare("2A", 100) == 300
    assert base_fare("1A", 100) == 500


def test_base_fare_minimum_fare_clamp():
    # SL * 20 = 20 < 50 => clamped to 50
    assert base_fare("SL", 20) == 50
    # Boundary exactly 50
    assert base_fare("SL", 50) == 50
    # Boundary above 50
    assert base_fare("SL", 51) == 51


def test_base_fare_exceptions():
    with pytest.raises(ValueError, match="unknown class"):
        base_fare("NON_EXISTENT", 100)
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", 0)
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", -10)


def test_concession_tatkal():
    assert concession(3, "M", is_tatkal=True) == 0
    assert concession(70, "F", is_tatkal=True) == 0


def test_concession_infant_and_child():
    # Infant (< 5)
    assert concession(2, "M", False) == 100
    assert concession(4, "F", False) == 100
    # Child (5 <= age <= 12)
    assert concession(5, "M", False) == 50
    assert concession(8, "F", False) == 50
    assert concession(12, "M", False) == 50


def test_concession_adult():
    # Adult boundaries (13 <= age < 60)
    assert concession(13, "M", False) == 0
    assert concession(59, "F", False) == 0


def test_concession_senior():
    # Senior female (>= 60)
    assert concession(60, "F", False) == 50
    assert concession(75, "F", False) == 50
    # Senior male (>= 60)
    assert concession(60, "M", False) == 40
    assert concession(80, "M", False) == 40


def test_tatkal_charge_sleeper():
    # Below min clamp
    assert tatkal_charge("SL", 500) == 100
    # Boundary min clamp
    assert tatkal_charge("SL", 1000) == 100
    # Normal range
    assert tatkal_charge("SL", 2000) == 200
    # Boundary max clamp
    assert tatkal_charge("SL", 4000) == 400
    # Above max clamp
    assert tatkal_charge("SL", 5000) == 400


def test_tatkal_charge_ac_classes():
    # Below min clamp
    assert tatkal_charge("3A", 200) == 100
    # Boundary min clamp
    assert tatkal_charge("2A", 334) == 100
    # Normal range
    assert tatkal_charge("1A", 1000) == 300
    # Boundary max clamp
    assert tatkal_charge("3A", 1334) == 400
    # Above max clamp
    assert tatkal_charge("2A", 2000) == 400
