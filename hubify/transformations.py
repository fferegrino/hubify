from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def group_by_day(time_series: pd.Series, buckets: int = -1) -> pd.DataFrame:
    """
    Groups a time series by day of ocurrence and returns the results as a dataframe with columns "date" and "events"
    """
    day_by_day = time_series.dt.floor("d")
    grouped = day_by_day.groupby(day_by_day).count()
    grouped = grouped.rename_axis("date").rename("events").reset_index()
    return grouped


def bucketize(events: pd.Series, buckets: int) -> pd.Series:
    """
    If `buckets` > 0, this method will put the value of the series into buckets
    """
    if buckets > 0:
        evts = pd.cut(events, bins=buckets, include_lowest=True)
        return evts.map(lambda x: (x.left + x.right) / 2)
    return events


def calculate_position_heatmap(events: pd.DataFrame, min_sunday: datetime) -> pd.DataFrame:
    days_from_initial_sunday = (events["date"] - min_sunday).dt.days
    events["week"] = days_from_initial_sunday // 7
    events["weekday"] = (events["date"].dt.weekday + 1) % 7
    return events[["date", "events", "week", "weekday"]]


def prepare_base_heatmap(grouped: pd.DataFrame, weeks) -> np.array:
    # Generate a heatmap from the time series data
    heatmap = np.full((7, weeks), np.nan)
    for _, row in grouped.iterrows():
        heatmap[row["weekday"]][row["week"]] = row["events"]
    return heatmap


def pad_to_sundays(start_date, end_date):
    """
    Transform start_date and end_date to the sunday before and after respectively
    """
    start = start_date if start_date.weekday() == 6 else start_date - timedelta(days=start_date.weekday() + 1)
    end = end_date + timedelta(days=6 - (-1 if end_date.weekday() == 6 else end_date.weekday()))
    return start, end
