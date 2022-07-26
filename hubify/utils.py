import numpy as np
from colour import Color
from matplotlib.colors import ListedColormap

EMPTY_COLOR = "#ebedf0"
LOW_COLOR = "#9be9a8"
HIGH_COLOR = "#216e39"


def get_cmap(cmap):
    cmap = cmap or (LOW_COLOR, HIGH_COLOR)
    if isinstance(cmap, tuple):
        initial = Color(cmap[0])
        end = Color(cmap[1])
        colormap = np.array([cl.rgb for cl in initial.range_to(end, 256)])

        return ListedColormap(colormap)
    else:
        return cmap
