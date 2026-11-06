"""
test_train_fare.py - Fuzz Testing Suite using Hypothesis

Uses property-based testing (@given) with random Unicode strings and None
to verify robustness against crashes, unhandled exceptions, and invalid inputs.
"""

import pytest
from hypothesis import given, strategies as st
try:
    from processor import parse_pnr, journey_distance, berth_type
except ImportError:
    from train_fare import parse_pnr, journey_distance, berth_type


# =========================================================================
# 1. Hypothesis Property-Based Fuzz Tests (No-Crash Guarantees)
# =========================================================================

@given(st.text() | st.none())
def test_parse_pnr_no_crash(s):
    """
    Hypothesis test ensuring parse_pnr handles arbitrary strings
    and None without crashing with unhandled exceptions.
    """
    try:
        parse_pnr(s)
    except Exception as e:
        assert False, f"parse_pnr crashed with: {e}"


@given(st.text() | st.none())
def test_journey_distance_no_crash(s):
    """
    Hypothesis test ensuring journey_distance handles arbitrary strings
    and None without crashing with unhandled exceptions.
    """
    try:
        journey_distance(s)
    except Exception as e:
        assert False, f"journey_distance crashed with: {e}"


@given(st.text() | st.none())
def test_berth_type_no_crash(s):
    """
    Hypothesis test ensuring berth_type handles arbitrary strings
    and None without crashing with unhandled exceptions.
    """
    try:
        berth_type(s)
    except Exception as e:
        assert False, f"berth_type crashed with: {e}"


# =========================================================================
# 2. Functional Unit Tests (Valid and Known Invalid Cases)
# =========================================================================

def test_parse_pnr_valid_cases():
    """Verify correct PNR parsing on standard valid inputs."""
    assert parse_pnr("4521367890") == (4, 521367890)
    assert parse_pnr("1234567890") == (1, 234567890)
    assert parse_pnr("  4521367890  ") == (4, 521367890)  # Leading/trailing spaces


def test_parse_pnr_invalid_cases():
    """Verify safe handling (returns None) on malformed inputs."""
    assert parse_pnr("") is None
    assert parse_pnr(None) is None
    assert parse_pnr("12345") is None  # Too short (< 10 digits)
    assert parse_pnr("12345678901") is None  # Too long (> 10 digits)
    assert parse_pnr("452136789a") is None  # Contains alphabetic char
    assert parse_pnr("45213 67890") is None  # Internal spaces


def test_journey_distance_valid_cases():
    """Verify journey distance calculation on valid CSV inputs."""
    assert journey_distance("0,120,340") == 340
    assert journey_distance("10,50") == 40
    assert journey_distance(" 0 , 150 , 300 ") == 300


def test_journey_distance_invalid_cases():
    """Verify safe handling (returns None) on invalid CSV formats."""
    assert journey_distance("") is None
    assert journey_distance(None) is None
    assert journey_distance("100") is None  # Single station
    assert journey_distance("300,100") is None  # Decreasing distance
    assert journey_distance("0,abc,300") is None  # Non-numeric
    assert journey_distance("0,,300") is None  # Empty element


def test_berth_type_valid_cases():
    """Verify coach and berth layout mapping for valid seats."""
    # 45 % 8 = 5 -> MB
    assert berth_type("S3-45") == ("S3", "MB")
    # 41 % 8 = 1 -> LB
    assert berth_type("b1-41") == ("B1", "LB")
    # 48 % 8 = 0 -> SU
    assert berth_type("A1-48") == ("A1", "SU")
    # 47 % 8 = 7 -> SL
    assert berth_type("S1-47") == ("S1", "SL")


def test_berth_type_invalid_cases():
    """Verify safe handling (returns None) on invalid coach/seat formats."""
    assert berth_type("") is None
    assert berth_type(None) is None
    assert berth_type("S3") is None  # Missing hyphen
    assert berth_type("S3-") is None  # Missing seat number
    assert berth_type("-45") is None  # Missing coach
    assert berth_type("S3-45-extra") is None  # Multiple hyphens
    assert berth_type("S3-abc") is None  # Non-numeric seat
    assert berth_type("S3-0") is None  # Zero seat number
    assert berth_type("S3--5") is None  # Negative seat number
