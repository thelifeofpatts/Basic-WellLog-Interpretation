import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def custom_interpretation_plot(logs, depth_start, depth_end, *custom_logs, units):
    num_tracks = len(custom_logs)
    fig, ax = plt.subplots(nrows=1, ncols=num_tracks, figsize=(15, 20), sharey=True)
    fig.suptitle("Custom Interpretation Plot", fontsize=22)

    # Calculate top value with less free space based on the number of tracks
    top_value = 1 - 0.015 * num_tracks

    # Adjust top parameter to leave less free space at the top
    fig.subplots_adjust(top=top_value, wspace=0.2)

    units = units  # in list

    depth_range = depth_end - depth_start

    # Dynamically adjust tick intervals based on the depth range
    if depth_range > 5000:
        major_tick_interval = 1000
        minor_tick_interval = 100
    elif depth_range > 1000:
        major_tick_interval = 500
        minor_tick_interval = 50
    else:
        major_tick_interval = 100
        minor_tick_interval = 10

    # General setting for all axes
    for axes in ax:
        axes.set_ylim(depth_start, depth_end)
        axes.invert_yaxis()
        axes.yaxis.grid(True, which='minor', linestyle=':')
        axes.yaxis.grid(True, which='major', linestyle='-', linewidth='1')
        axes.yaxis.set_major_locator(ticker.MultipleLocator(major_tick_interval))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(minor_tick_interval))
        axes.get_xaxis().set_visible(False)

    # Customizing each track with unit and color
    for i, log_name in enumerate(custom_logs):
        current_ax = ax[i].twiny()
        current_ax.plot(logs[log_name], logs.DEPT, label=f'{log_name} [{units[i]}]', color='C'+str(i))
        if log_name == "DR" or log_name == "MR" or log_name == "SR":
            current_ax.set_xscale('log')
        current_ax.set_xlabel(f'{log_name} [{units[i]}]', color='C'+str(i))
        current_ax.tick_params(axis='x', colors='C'+str(i))
        current_ax.spines['top'].set_position(('outward',0))
        current_ax.legend(loc='lower right', facecolor='white', framealpha=1, fontsize=7)
    plt.show()
