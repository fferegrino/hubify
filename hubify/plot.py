import calendar
from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import seaborn as sns
from matplotlib.axes import Axes


def plot_heatmap(ax: Optional[Axes], heatmap: np.ndarray):
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

    ax.set_facecolor("#ebedf0")

    return ax


def set_xy_labels(ax: Axes, start_date: datetime, week_number: int):

    # X-axis
    all_sundays = [start_date + timedelta(weeks=wk) for wk in range(week_number)]
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
