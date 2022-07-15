from datetime import datetime

import numpy
import pandas as pd
import pytest

from hubify.hubify import calculate_position_heatmap, group_by_day, pad_to_sundays, prepare_base_heatmap


def test_prepare_events():
    input_data = pd.DataFrame(
        [
            (datetime(2021, 1, 1), 1),
            (datetime(2021, 1, 3), 2),
        ],
        columns=["date", "events"],
    )
    expected = pd.DataFrame(
        [
            (datetime(2021, 1, 1), 1, 0, 5),
            (datetime(2021, 1, 3), 2, 1, 0),
        ],
        columns=["date", "events", "week", "weekday"],
    )

    actual = calculate_position_heatmap(input_data)

    pd.testing.assert_frame_equal(expected, actual)


def testgroup_by_day():

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
            (datetime(2022, 1, 3), 2),
            (datetime(2022, 1, 4), 1),
            (datetime(2022, 1, 5), 1),
            (datetime(2022, 1, 6), 1),
        ],
        columns=["date", "events"],
    )

    # Act
    actual_result = group_by_day(input_data)

    # Assert
    pd.testing.assert_frame_equal(actual_result, expected)


def test_prepare_base_heatmap():
    # Prepare
    input_data = pd.DataFrame(
        [
            (
                datetime(2022, 1, 2),
                2,
                0,
                0,
            ),
            (
                datetime(2022, 1, 3),
                1,
                0,
                1,
            ),
            (
                datetime(2022, 1, 4),
                1,
                0,
                2,
            ),
            (
                datetime(2022, 1, 5),
                1,
                0,
                3,
            ),
        ],
        columns=["date", "events", "week", "weekday"],
    )

    expected = numpy.array(
        [
            [2],
            [1],
            [1],
            [1],
            [numpy.nan],
            [numpy.nan],
            [numpy.nan],
        ]
    )

    # Act
    actual = prepare_base_heatmap(input_data)

    # Assert
    numpy.testing.assert_equal(actual, expected)


@pytest.mark.parametrize(
    ["start_date", "end_date", "start_sunday", "end_sunday"],
    [
        (datetime(2021, 1, 3), datetime(2021, 1, 9), datetime(2021, 1, 3), datetime(2021, 1, 10)),
        (datetime(2021, 1, 3), datetime(2021, 1, 10), datetime(2021, 1, 3), datetime(2021, 1, 17)),
        (datetime(2021, 1, 1), datetime(2021, 12, 31), datetime(2020, 12, 27), datetime(2022, 1, 2)),
    ],
)
def test_pad_to_sundays(start_date, end_date, start_sunday, end_sunday):
    actual_start_sunday, actual_end_sunday = pad_to_sundays(start_date, end_date)
    assert actual_start_sunday == start_sunday
    assert actual_end_sunday == end_sunday
