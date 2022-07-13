from datetime import datetime

import numpy
import pandas as pd

from hubify.hubify import group_by_day, prepare_base_heatmap, prepare_events


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

    actual = prepare_events(input_data)

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
