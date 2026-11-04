import weather_im2650


def test_version_is_defined():
    assert isinstance(weather_im2650.__version__, str)

import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

from weather_im2650 import (
    celsius_to_fahrenheit,
    summarize_temperatures,
    clean_readings,
)

# =============================================================================
# PART 1: UNIT TESTS
# =============================================================================

@pytest.mark.parametrize("celsius, expected", [
    (-273.15, -459.67),
    (0, 32),
    (100, 212),
    (-40, -40),
    (37, 98.6)
])
def test_celsius_to_fahrenheit(celsius, expected):
    """Verifies that temperature conversions from Celsius to Fahrenheit are accurate"""
    result = celsius_to_fahrenheit(celsius)
    assert round(result, 2) == expected  

@pytest.mark.parametrize("bad_input, expected_error", [
    ("24°C", TypeError),
    (None, TypeError),
    (-275, ValueError),
    ("17", TypeError)
])
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Verifies error handling for invalid temperature types and values"""
    with pytest.raises(expected_error): 
        celsius_to_fahrenheit(bad_input)

def test_summarize_temperatures():
    """Tests statistical aggregation over a checklist containing NaN values."""
    input_temps = [30.0, float('nan'), 19.0, 25.5]
    result = summarize_temperatures(input_temps)
    assert "mean" in result or "avg" in result  # handles variance in HW6 implementations
    assert "min" in result
    assert "max" in result
    assert "n_missing" in result

# =============================================================================
# PART 2: FIXTURES
# =============================================================================

@pytest.fixture
def raw_readings():
    """Validates the structural footprint of the raw input test data fixture"""
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": ["2026-07-02", "2026-07-01", "2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })

def test_raw_readings_fixture(raw_readings):
    """Checks the fixture has the columns, number of rows, and missing values expected."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert raw_readings.shape[0] == 5
    assert raw_readings["temp_c"].isna().sum() == 1

# =============================================================================
# PART 3: TESTING DATAFRAMES
# =============================================================================

def test_clean_readings(raw_readings):
    """Tests individual data cleaning transformations on dataframes"""
    actual = clean_readings(raw_readings)
    expected = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4]
    })
    assert_frame_equal(actual, expected)
