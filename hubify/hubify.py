from datetime import timedelta
import calendar
import  numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def hubify(time_series):
    # Data transformation
    day_by_day = time_series.dt.floor('d')
    grouped = day_by_day.groupby(day_by_day).count()
    grouped = grouped.rename_axis('date').rename('events').reset_index()
    grouped['weekday'] = grouped['date'].dt.weekday
    grouped['week'] = grouped['date'].dt.week
    grouped['continuous_week'] = grouped['week'] - grouped['week'].min()

    # Generate a heatmap from the time series data
    heatmap = np.full((7, grouped['continuous_week'].max() + 1), np.nan)

    for _, row in grouped.iterrows():
        heatmap[row["weekday"]][row["continuous_week"]] = row["events"]

    # Plot the timestamp
    fig = plt.figure(figsize=(20, 5))
    ax = plt.subplot()
    sns.heatmap(heatmap, ax=ax)

    # Change Y labels
    y_labels = ["Mon", "", "Wed", "", "Fri", "", "Sun"]
    ax.set_yticklabels(y_labels, rotation=0)

    # Get the monday for the first week of the graph
    min_date = grouped["date"].min()
    first_monday = min_date - timedelta(min_date.weekday())
    all_mondays = [first_monday + timedelta(weeks=wk) for wk in range(grouped["continuous_week"].max() + 1)]
    x_labels = [calendar.month_abbr[monday.month] for monday in all_mondays]
    # TODO: Show only the first label for a given month
    ax.set_xticklabels(x_labels)

    plt.show()
