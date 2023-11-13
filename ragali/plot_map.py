import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import ipywidgets


def scatter_line(
    da, vmax=None, vmin=0, cmap='viridis', linewidth=2, pad_width=1, ax=None, add_time_slider=False
):
    if ax is None:
        fig, ax = plt.subplots()
    if vmax is None:
        vmax = np.max(da.values)

    x0 = np.atleast_1d(da.site_0_lon.values)
    y0 = np.atleast_1d(da.site_0_lat.values)
    x1 = np.atleast_1d(da.site_1_lon.values)
    y1 = np.atleast_1d(da.site_1_lat.values)

    lines = LineCollection(
        [((x0[i], y0[i]), (x1[i], y1[i])) for i in range(len(x0))],
        norm=Normalize(vmin=vmin, vmax=vmax),
        cmap=cmap,
        linewidth=linewidth,
        linestyles='solid',
        capstyle='round',
        path_effects=[
            pe.Stroke(linewidth=linewidth + pad_width, foreground='k', capstyle='round'),
            pe.Normal(),
        ]
    )
    ax.add_collection(lines)
    ax.autoscale()

    if add_time_slider is False:
        if 'time' in da.dims:
            if not np.isscalar(da.time.values):
                raise ValueError('time dimension of `da` must have zero length if no '
                                 'time slider is added to the plot')
        lines.set_array(da)
    else:
        lines.set_array(da.isel(time=0).values)

        def update(t=da.time.isel(time=0).values):
            lines.set_array(da.sel(time=t).values)
            plt.draw()

        ipywidgets.interact(
            update,
            t=ipywidgets.SelectionSlider(options=da.time.values)
        )

    return lines
