import matplotlib.pyplot as plt
import pandas as pd

from hubify.hubify import hubify

fig, ax = plt.subplots(1, 2)

time_series = pd.read_csv("ejemplo.csv", index_col=None, header=None, parse_dates=[0])

hubify(time_series[0], plot_title="Mi gráfica especial")

plt.show()
