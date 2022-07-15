import itertools
import random
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd

from hubify.hubify import hubify

# fig, ax = plt.subplots(1, 2)

# time_series = pd.read_csv("ejemplo.csv", index_col=None, header=None, parse_dates=[0])

random.seed(20)

base_date = datetime(2021, 10, 1)
# all_dates = pd.Series([
#     base_date + timedelta(days=random.randint(0, 365)) for _ in range(1000)
# ])


all_dates = pd.Series(itertools.chain(*[[base_date + timedelta(days=x) for _ in range(x + 1)] for x in range(10)]))
# breakpoint()
hubify(all_dates, plot_title="Mi gráfica especial", trim=True)

plt.show()
