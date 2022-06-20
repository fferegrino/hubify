import calendar
from datetime import timedelta

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def hubify(time_series, plot_title=None):
    # Data transformation
    day_by_day = time_series.dt.floor("d")
    grouped = day_by_day.groupby(day_by_day).count()
    grouped = grouped.rename_axis("date").rename("events").reset_index()
    grouped["weekday"] = grouped["date"].dt.weekday
    grouped["week"] = grouped["date"].dt.week

    starting_year = grouped["date"].dt.year.min()
    # TODO: not all years have 52 weeks
    grouped["continuous_week"] = (grouped["week"] - grouped["week"].min()) + (
        (grouped["date"].dt.year - starting_year) * 52
    )

    # Generate a heatmap from the time series data
    heatmap = np.full((7, grouped["continuous_week"].max() + 1), np.nan)

    for _, row in grouped.iterrows():
        heatmap[row["weekday"]][row["continuous_week"]] = row["events"]

    # Plot the timestamp
    fig = plt.figure(figsize=(20, 5))
    ax = plt.subplot()
    sns.heatmap(
        heatmap,
        ax=ax,
        cbar=False,
        linecolor="white",
        cmap="Greens",
        square=True,
        linewidth=2,
    )

    # Change Y labels
    y_labels = ["Mon", "", "Wed", "", "Fri", "", "Sun"]
    ax.set_yticklabels(y_labels, rotation=0)

    # Get the monday for the first week of the graph
    min_date = grouped["date"].min()
    first_monday = min_date - timedelta(min_date.weekday())
    all_mondays = [first_monday + timedelta(weeks=wk) for wk in range(grouped["continuous_week"].max() + 1)]
    x_labels = [calendar.month_abbr[monday.month] for monday in all_mondays]
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
    ax.set_xticklabels(true_x_labels)

    # Set more plot details
    if plot_title:
        ax.set_title(plot_title, fontsize=20, pad=40)
    ax.xaxis.tick_top()
    ax.set_facecolor("#ebedf0")
    ax.tick_params(axis="both", which="both", length=0)

    plt.show()
