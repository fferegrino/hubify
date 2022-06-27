import pandas as pd

from hubify.hubify import calculate_continuous_week


def test_simple_week_number():
    input_frame = pd.DataFrame(
        (2022, 1),
        (2022, 2),
    )

    expected_series = pd.Series([1, 2])

    actual_series = calculate_continuous_week(input_frame)

    pd.testing.assert_series_equal(expected_series, actual_series)
