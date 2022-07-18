import calendar
from datetime import datetime, timedelta
from typing import Optional

import numpy as np
import seaborn as sns
from matplotlib.axes import Axes

from hubify.defaults import EMPTY_COLOR, HIGH_COLOR, LOW_COLOR


def plot_heatmap(ax: Optional[Axes], heatmap: np.ndarray, cmap):
    # Plot the timestamp
    ax = sns.heatmap(
        heatmap,
        ax=ax,
        cbar=False,
        linecolor="white",
        cmap=cmap,
        square=True,
        linewidth=2,
    )

    ax.set_facecolor(EMPTY_COLOR)

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


def plot_matplotlib(heatmap, colormap, plot_title, true_start_date, ax):
    ax = plot_heatmap(ax, heatmap, cmap=colormap)
    weeks_to_plot = heatmap.shape[1]
    set_xy_labels(ax, true_start_date, weeks_to_plot)
    if plot_title:
        ax.set_title(plot_title, fontsize=20, pad=40)
    return ax
