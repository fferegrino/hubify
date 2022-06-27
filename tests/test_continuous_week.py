import pandas as pd

from hubify.hubify import calculate_continuous_week


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
