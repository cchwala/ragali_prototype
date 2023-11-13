import matplotlib.pyplot as plt


def plot_cml_ts(ds, vars_to_plot, wet_as_shaded=True, fig_width=18, fig_height=None):
    N_plots = len(vars_to_plot)
    fig, axs = plt.subplots(N_plots, 1, figsize=(fig_width, N_plots * 2 + 2), sharex=True)
    for i, var in enumerate(vars_to_plot):
        axs[i].plot(ds[var].time.values, ds[var].values)
