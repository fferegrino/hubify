from datetime import datetime

import numpy
import pandas as pd

from hubify.hubify import calculate_continuous_week, prepare_base_heatmap, prepare_time_series


def test_simple_week_number():
    input_frame = pd.DataFrame(
        [
            (2022, 1),
            (2022, 2),
        ],
        columns=["year", "week"],
    )

    expected_series = pd.Series([1, 2])

    actual_series = calculate_continuous_week(input_frame)

    pd.testing.assert_series_equal(expected_series, actual_series, check_names=False)


def test_mid_year_week_number():
    input_frame = pd.DataFrame(
        [
            (2022, 5),
            (2022, 7),
        ],
        columns=["year", "week"],
    )

    expected_series = pd.Series([1, 3])

    actual_series = calculate_continuous_week(input_frame)

    pd.testing.assert_series_equal(expected_series, actual_series, check_names=False)


def test_muli_year_week_number():
    input_frame = pd.DataFrame(
        [
            (2022, 5),
            (2022, 7),
            (2023, 1),
        ],
        columns=["year", "week"],
    )

    expected_series = pd.Series([1, 3, 49])

    actual_series = calculate_continuous_week(input_frame)

    pd.testing.assert_series_equal(expected_series, actual_series, check_names=False)


def test_prepare_time_series():

    # Prepare
    input_data = pd.Series(
        [
            datetime(2022, 1, 3, 10, 20),
            datetime(2022, 1, 4, 23, 55),
            datetime(2022, 1, 5, 9, 5),
            datetime(2022, 1, 6),
            datetime(2022, 1, 3),
        ]
    )

    expected = pd.DataFrame(
        [
            (datetime(2022, 1, 3), 2, 0, 1, 2022),
            (datetime(2022, 1, 4), 1, 1, 1, 2022),
            (datetime(2022, 1, 5), 1, 2, 1, 2022),
            (datetime(2022, 1, 6), 1, 3, 1, 2022),
        ],
        columns=["date", "events", "weekday", "week", "year"],
    )

    # Act
    actual_result = prepare_time_series(input_data)

    # Assert
    pd.testing.assert_frame_equal(actual_result, expected)


def test_prepare_base_heatmap():
    # Prepare
    input_data = pd.DataFrame(
        [
            (datetime(2022, 1, 3), 2, 0, 1, 2022, 1),
            (datetime(2022, 1, 4), 1, 1, 1, 2022, 1),
            (datetime(2022, 1, 5), 1, 2, 1, 2022, 1),
            (datetime(2022, 1, 6), 1, 3, 1, 2022, 1),
        ],
        columns=["date", "events", "weekday", "week", "year", "continuous_week"],
    )

    expected = numpy.array(
        [
            [numpy.nan, 2],
            [numpy.nan, 1],
            [numpy.nan, 1],
            [numpy.nan, 1],
            [numpy.nan, numpy.nan],
            [numpy.nan, numpy.nan],
            [numpy.nan, numpy.nan],
        ]
    )

    # Act
    actual = prepare_base_heatmap(input_data)

    # Assert
    numpy.testing.assert_equal(actual, expected)
