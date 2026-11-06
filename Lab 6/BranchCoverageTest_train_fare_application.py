"""
BranchCoverageTest_train_fare.py

Comprehensive Test suite designed to achieve 100% Branch Coverage
and Boundary Value Analysis for train_fare.py.

Every decision point (if / elif / else) is evaluated to both True and False,
covering all execution pathways, edge cases, and boundary limits:
- base_fare:
    * class in RATE_PER_KM (True / False)
    * distance <= 0 (True / False, boundary distance=0, -1, 1)
    * fare < 50 (True / False, boundary fare=49, 50, 51)
    * all travel classes tested: SL (x1), 3A (x2), 2A (x3), 1A (x5)
- concession:
    * is_tatkal (True / False)
    * age < 5 (True / False, boundary age=4, 5)
    * age <= 12 (True / False, boundary age=5, 12, 13)
    * age >= 60 (True / False, boundary age=59, 60, 61)
    * gender == "F" (True / False, tested for senior female, male, other)
    * general adult fallthrough (13 <= age <= 59)
- tatkal_charge:
    * travel_class == "SL" (True / False)
    * for SL:
        - charge < 100 (charge clamped to 100)
        - charge == 100 (exact lower boundary)
        - 100 < charge < 400 (normal range)
        - charge == 400 (exact upper boundary)
        - charge > 400 (charge clamped to 400)
    * for Non-SL (3A, 2A, 1A):
        - charge < 100 (charge clamped to 100)
        - charge == 100 (exact lower boundary)
        - 100 < charge < 400 (normal range)
        - charge == 400 (exact upper boundary)
        - charge > 400 (charge clamped to 400)
"""

import pytest
from train_fare import base_fare, concession, tatkal_charge


# =======================================================================
# 1. Branch Coverage Tests: base_fare
# =======================================================================

class TestBaseFareBranchCoverage:
    """Tests all branches and boundary conditions in base_fare."""

    def test_class_not_in_rates_raises_error(self):
        """Branch: travel_class not in RATE_PER_KM -> True."""
        with pytest.raises(ValueError, match="unknown class"):
            base_fare("NON_EXISTENT_CLASS", 100)

    def test_class_in_rates_all_classes(self):
        """Branch: travel_class not in RATE_PER_KM -> False for all valid classes."""
        # SL: rate 1
        assert base_fare("SL", 100) == 100
        # 3A: rate 2
        assert base_fare("3A", 100) == 200
        # 2A: rate 3
        assert base_fare("2A", 100) == 300
        # 1A: rate 5
        assert base_fare("1A", 100) == 500

    def test_distance_zero_raises_error(self):
        """Branch: distance_km <= 0 -> True (boundary: distance = 0)."""
        with pytest.raises(ValueError, match="invalid distance"):
            base_fare("SL", 0)

    def test_distance_negative_raises_error(self):
        """Branch: distance_km <= 0 -> True (distance < 0)."""
        with pytest.raises(ValueError, match="invalid distance"):
            base_fare("SL", -10)

    def test_distance_positive_boundary(self):
        """Branch: distance_km <= 0 -> False (boundary: distance = 1)."""
        # Rate 1 * 1 = 1 < 50 => minimum fare 50
        assert base_fare("SL", 1) == 50

    def test_fare_below_minimum_clamped(self):
        """Branch: fare < 50 -> True (fare = 49)."""
        # SL rate is 1 * 49 = 49 < 50 => clamped to 50
        assert base_fare("SL", 49) == 50

    def test_fare_exact_minimum_boundary(self):
        """Branch: fare < 50 -> False (boundary: fare = 50)."""
        # SL rate is 1 * 50 = 50 => remains 50
        assert base_fare("SL", 50) == 50

    def test_fare_above_minimum(self):
        """Branch: fare < 50 -> False (fare = 51)."""
        # SL rate is 1 * 51 = 51 > 50 => remains 51
        assert base_fare("SL", 51) == 51


# =======================================================================
# 2. Branch Coverage Tests: concession
# =======================================================================

class TestConcessionBranchCoverage:
    """Tests all branches and boundary conditions in concession."""

    def test_is_tatkal_true(self):
        """Branch: if is_tatkal -> True."""
        assert concession(3, "M", is_tatkal=True) == 0
        assert concession(10, "F", is_tatkal=True) == 0
        assert concession(70, "F", is_tatkal=True) == 0
        assert concession(30, "M", is_tatkal=True) == 0

    def test_is_tatkal_false_infant(self):
        """Branch: is_tatkal -> False, age < 5 -> True (infant 100%)."""
        assert concession(0, "M", is_tatkal=False) == 100
        assert concession(4, "F", is_tatkal=False) == 100

    def test_age_child_boundary_lower(self):
        """Branch: age < 5 -> False, age <= 12 -> True (boundary: age = 5)."""
        assert concession(5, "M", is_tatkal=False) == 50

    def test_age_child_middle(self):
        """Branch: age <= 12 -> True (middle: age = 8)."""
        assert concession(8, "F", is_tatkal=False) == 50

    def test_age_child_boundary_upper(self):
        """Branch: age <= 12 -> True (boundary: age = 12)."""
        assert concession(12, "M", is_tatkal=False) == 50

    def test_age_general_boundary_lower(self):
        """Branch: age <= 12 -> False, age >= 60 -> False (boundary: age = 13)."""
        assert concession(13, "M", is_tatkal=False) == 0

    def test_age_general_middle(self):
        """Branch: age in [13, 59] -> returns 0."""
        assert concession(35, "F", is_tatkal=False) == 0

    def test_age_general_boundary_upper(self):
        """Branch: age in [13, 59] (boundary: age = 59)."""
        assert concession(59, "M", is_tatkal=False) == 0

    def test_senior_female_boundary(self):
        """Branch: age >= 60 -> True, gender == 'F' -> True (boundary: age = 60)."""
        assert concession(60, "F", is_tatkal=False) == 50

    def test_senior_female_older(self):
        """Branch: age >= 60 -> True, gender == 'F' -> True (age = 75)."""
        assert concession(75, "F", is_tatkal=False) == 50

    def test_senior_male_boundary(self):
        """Branch: age >= 60 -> True, gender == 'F' -> False (boundary: age = 60)."""
        assert concession(60, "M", is_tatkal=False) == 40

    def test_senior_other_gender(self):
        """Branch: age >= 60 -> True, gender == 'F' -> False (other gender 'O')."""
        assert concession(70, "O", is_tatkal=False) == 40


# =======================================================================
# 3. Branch Coverage Tests: tatkal_charge
# =======================================================================

class TestTatkalChargeBranchCoverage:
    """Tests all branches and boundaries for Sleeper and Non-Sleeper classes."""

    # --- Sleeper Class (charge = fare // 10) ---

    def test_sleeper_charge_below_min(self):
        """SL Branch: charge < 100 -> True (fare = 990 -> 99 < 100 => 100)."""
        assert tatkal_charge("SL", 990) == 100

    def test_sleeper_charge_at_min_boundary(self):
        """SL Branch: charge < 100 -> False, charge == 100 (fare = 1000 -> 100)."""
        assert tatkal_charge("SL", 1000) == 100

    def test_sleeper_charge_normal_range(self):
        """SL Branch: 100 <= charge <= 400 (fare = 2500 -> 250)."""
        assert tatkal_charge("SL", 2500) == 250

    def test_sleeper_charge_at_max_boundary(self):
        """SL Branch: charge > 400 -> False, charge == 400 (fare = 4000 -> 400)."""
        assert tatkal_charge("SL", 4000) == 400

    def test_sleeper_charge_above_max(self):
        """SL Branch: charge > 400 -> True (fare = 4010 -> 401 > 400 => 400)."""
        assert tatkal_charge("SL", 4010) == 400

    # --- Non-Sleeper Classes (charge = fare * 3 // 10) ---

    def test_non_sleeper_charge_below_min(self):
        """Non-SL Branch: charge < 100 -> True (3A fare = 200 -> 60 < 100 => 100)."""
        assert tatkal_charge("3A", 200) == 100

    def test_non_sleeper_charge_at_min_boundary(self):
        """Non-SL Branch: charge < 100 -> False, charge == 100 (2A fare = 334 -> 100)."""
        assert tatkal_charge("2A", 334) == 100

    def test_non_sleeper_charge_normal_range(self):
        """Non-SL Branch: 100 <= charge <= 400 (1A fare = 1000 -> 300)."""
        assert tatkal_charge("1A", 1000) == 300

    def test_non_sleeper_charge_at_max_boundary(self):
        """Non-SL Branch: charge > 400 -> False, charge == 400 (3A fare = 1334 -> 400)."""
        assert tatkal_charge("3A", 1334) == 400

    def test_non_sleeper_charge_above_max(self):
        """Non-SL Branch: charge > 400 -> True (2A fare = 2000 -> 600 > 400 => 400)."""
        assert tatkal_charge("2A", 2000) == 400
