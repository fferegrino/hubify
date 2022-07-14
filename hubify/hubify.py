import calendar
from datetime import timedelta
from typing import Optional, Union

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes


def group_by_day(time_series: pd.Series) -> pd.DataFrame:
    """
    Groups a time series by day of ocurrence and returns the results as a dataframe with columns "date" and "events"
    """
    day_by_day = time_series.dt.floor("d")
    grouped = day_by_day.groupby(day_by_day).count()
    grouped = grouped.rename_axis("date").rename("events").reset_index()
    return grouped


def prepare_events(events: pd.DataFrame) -> pd.DataFrame:
    # Select the minimum year and week in the dataframe
    min_sunday = events["date"].min() - timedelta(events["date"].min().weekday() + 1)
    days_from_initial_sunday = (events["date"] - min_sunday).dt.days
    events["week"] = days_from_initial_sunday // 7
    events["week"] = events["week"] - events["week"].min()
    events["weekday"] = (events["date"].dt.weekday + 1) % 7
    return events[["date", "events", "week", "weekday"]]


def prepare_base_heatmap(grouped: pd.DataFrame) -> np.array:
    # Generate a heatmap from the time series data
    heatmap = np.full((7, grouped["week"].max() + 1), np.nan)
    for _, row in grouped.iterrows():
        heatmap[row["weekday"]][row["week"]] = row["events"]
    return heatmap


def plot_heatmap(ax, prepared_df, heatmap, plot_title):
    # Plot the timestamp
    ax = sns.heatmap(
        heatmap,
        ax=ax,
        cbar=False,
        linecolor="white",
        cmap="Greens",
        square=True,
        linewidth=2,
    )
    set_xy_labels(ax, prepared_df["date"].min(), prepared_df["continuous_week"].max())

    ax.set_facecolor("#ebedf0")
    if plot_title:
        ax.set_title(plot_title, fontsize=20, pad=40)


def set_xy_labels(ax, min_date, week_number):

    # X-axis
    first_sunday = min_date if min_date.weekday() == 6 else min_date - timedelta(min_date.weekday() + 1)
    all_sundays = [first_sunday + timedelta(weeks=wk) for wk in range(week_number)]
    x_labels = [calendar.month_abbr[monday.month] for monday in all_sundays]
    true_x_labels = []
    current_x_label = ""
    for x_label in x_labels:
        if current_x_label != x_label:
            true_x_labels.append(x_label)
            current_x_label = x_label
        else:
            true_x_labels.append("")
    if current_x_label != x_label:
        true_x_labels.append(x_label)
    ax.set_xticks([wk + 0.5 for wk in range(week_number)], true_x_labels)
    ax.xaxis.tick_top()

    # Y-axis
    y_labels = ["", "Mon", "", "Wed", "", "Fri", ""]
    ax.set_yticklabels(y_labels, rotation=0)

    ax.tick_params(axis="both", which="both", length=0)


def hubify(time_series: pd.Series, plot_title: Union[str, None] = None, ax: Optional[Axes] = None):
    """
    Create a GitHub like plot of your time series data.

    :param time_series: A pandas series of type `datetime64` with the timestamps for the events to plot
    :param plot_title: The title of the plot
    :param ax: The Axes in which the heatmap should be drawn, uses the currently-active Axes if none is provided
    """
    grouped = group_by_day(time_series)
    prepared_df = prepare_events(grouped)

    heatmap = prepare_base_heatmap(prepared_df)

    plot_heatmap(ax, prepared_df, heatmap, plot_title)
