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
    plt.show()
