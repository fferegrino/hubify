def hubify(time_series):
    day_by_day = time_series.dt.floor('d')
    grouped = day_by_day.groupby(day_by_day).count()
    grouped = grouped.rename_axis('date').rename('events').reset_index()
    grouped['weekday'] = grouped['date'].dt.weekday
    grouped['week'] = grouped['date'].dt.week
