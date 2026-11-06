"""
CodeCoverageTest_train_fare.py

Test suite designed to achieve 100% Statement (Line) Coverage
for train_fare.py. Every executable statement in the application
is exercised at least once.
"""

import pytest
from train_fare import base_fare, concession, tatkal_charge


# ==========================================
# 1. Tests for base_fare
# ==========================================

def test_base_fare_unknown_class():
    """Test unknown travel class raises ValueError."""
    with pytest.raises(ValueError, match="unknown class"):
        base_fare("INVALID_CLASS", 100)


def test_base_fare_invalid_distance():
    """Test non-positive distance raises ValueError."""
    with pytest.raises(ValueError, match="invalid distance"):
        base_fare("SL", 0)


def test_base_fare_minimum_fare_applied():
    """Test fare below minimum threshold (50) is clamped to 50."""
    # SL rate is 1, distance 20 => 20 < 50, so fare becomes 50
    assert base_fare("SL", 20) == 50


def test_base_fare_normal_fare():
    """Test regular calculation when fare >= 50."""
    # 3A rate is 2, distance 100 => 200 >= 50
    assert base_fare("3A", 100) == 200


# ==========================================
# 2. Tests for concession
# ==========================================

def test_concession_tatkal():
    """Test tatkal booking gives zero concession regardless of age/gender."""
    assert concession(70, "F", is_tatkal=True) == 0


def test_concession_infant():
    """Test child under age 5 gets 100% concession."""
    assert concession(3, "M", is_tatkal=False) == 100


def test_concession_child():
    """Test child aged between 5 and 12 gets 50% concession."""
    assert concession(10, "M", is_tatkal=False) == 50


def test_concession_senior_female():
    """Test senior citizen female (age >= 60) gets 50% concession."""
    assert concession(65, "F", is_tatkal=False) == 50


def test_concession_senior_male():
    """Test senior citizen male (age >= 60) gets 40% concession."""
    assert concession(65, "M", is_tatkal=False) == 40


def test_concession_adult():
    """Test general adult (age 13 to 59) gets no concession."""
    assert concession(30, "M", is_tatkal=False) == 0


# ==========================================
# 3. Tests for tatkal_charge
# ==========================================

def test_tatkal_charge_sleeper_min_clamp():
    """Test Sleeper tatkal charge clamped to minimum 100."""
    # fare = 500 // 10 = 50 < 100 => 100
    assert tatkal_charge("SL", 500) == 100


def test_tatkal_charge_ac_max_clamp():
    """Test AC class tatkal charge clamped to maximum 400."""
    # fare = 2000 * 3 // 10 = 600 > 400 => 400
    assert tatkal_charge("3A", 2000) == 400


def test_tatkal_charge_sleeper_normal():
    """Test Sleeper tatkal charge within normal bounds [100, 400]."""
    # fare = 2000 // 10 = 200
    assert tatkal_charge("SL", 2000) == 200
