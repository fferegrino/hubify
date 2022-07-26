__version__ = "0.3.0"

from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Union

import pandas as pd
from matplotlib.axes import Axes

from hubify.heatmap import make_heatmap
from hubify.seaborn import plot_matplotlib
from hubify.utils import get_cmap


def hubify(
    time_series: Union[pd.Series, List[datetime]],
    plot_title: Union[str, None] = None,
    start_date: datetime = None,
    end_date: datetime = None,
    trim: bool = False,
    buckets: int = 4,
    cmap: Union[Tuple[str, str], str, None] = None,
    ax: Optional[Axes] = None,
) -> Axes:
    """
    Create a  GitHub-like visualization for your time series data
    :param time_series: The data to plot
    :param plot_title: Plot's title
    :param start_date: The initial date to show for the plot
    :param end_date: The last date to show for the plot
    :param trim: If true, the entire time series data will be plotted, ignoring both `start_date` and `end_date`
    :param buckets: An integer specifying the number of buckets to divide the data into, pass -1 if you do not want data to be divided in buckets
    :param cmap: Could be either a tuple of colors in hex format (low, high) or a matplotlib color map
    :param ax: The axes to draw the plot on, if none is provided, it will use the current active axes
    :return: The axes where the plot was drawn
    """
    if trim:
        start_date = time_series.min()
        end_date = time_series.max()
    else:
        end_date = end_date or datetime.today().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        start_date = start_date or end_date - timedelta(days=366)

    if start_date > end_date:
        raise ValueError("start_date cannot be greater than end_data")

    time_series = pd.Series(time_series)
    colormap = get_cmap(cmap)

    heatmap, true_start_date, true_end_date = make_heatmap(time_series, buckets, start_date, end_date)

    ax = plot_matplotlib(heatmap, colormap, plot_title, true_start_date, ax)

    return ax
