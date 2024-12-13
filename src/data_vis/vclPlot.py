import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.gridspec as gridspec
from matplotlib import gridspec

def vcl_plot(logs, depth_start, depth_end, gr_clean=None, gr_clay=None,
             neut_clean1=None, den_clean1=None, neut_clean2=None,
             den_clean2=None, neut_clay=None, den_clay=None,
             sp_clean=None, sp_clay=None, rhob_axis=[1.5,2.8], nphi_axis=[0,1]):
    """
    Plot volume of clay from different methods with handling for missing data

    Parameters:
    -----------
    logs : pandas DataFrame
        Well log data containing depth and measurement curves
    depth_start, depth_end : float
        Depth range for plotting
    *_clean, *_clay : float, optional
        Clean and clay points for different methods
    """

    # Create figure and gridspec
    fig = plt.figure(figsize=(12, 10))
    fig.suptitle('Volume of clay from different methods', fontsize=14)
    fig.subplots_adjust(top=0.90, wspace=0.3, hspace=0.3)

    gs = gridspec.GridSpec(4, 3)

    # Initialize subplots
    ax1 = fig.add_subplot(gs[:, 0])  # All rows, column 1
    ax2 = fig.add_subplot(gs[0, 1])  # Row 1, column 2
    ax3 = fig.add_subplot(gs[1, 1])  # Row 2, column 2b
    ax4 = fig.add_subplot(gs[2, 1])  # Row 3, column 2
    ax5 = fig.add_subplot(gs[3, 1])  # Row 4, column 2
    ax6 = fig.add_subplot(gs[:, 2], sharey=ax1)  # All rows, column 3

    # Check for depth column
    depth_col = next((col for col in ['DEPT', 'DEPTH', 'MD'] if col in logs.columns), None)
    if depth_col is None:
        raise ValueError("No depth column found in logs")

    # Plot GR and SP (if available)
    ax1.invert_yaxis()
    ax1.grid(True)
    ax1.set_ylabel('DEPTH')

    if 'GR' in logs.columns:
        ax1.plot(logs.GR, logs[depth_col], color='green')
        ax1.set_xlabel('GR [api]', color='green')

    if 'SP' in logs.columns:
        ax11 = ax1.twiny()
        ax11.plot(logs.SP, logs[depth_col], color='blue')
        ax11.set_xlabel("SP [mV]", color='blue')

    if ' DR' in logs.columns:
        ax12 = ax1.twiny()
        ax12.plot(logs.DR, logs[depth_col], color='purple')
        ax12.set_xlabel('RT [ohm]', color='purple')

    # Histograms
    curves_to_plot = {
        'GR': ('green', ax2, 'GR [api]'),
        'SP': ('blue', ax3, 'SP [mV]'),
        'DR': ('gray', ax4, 'DR [m.ohm]')
    }

    for curve, (color, ax, xlabel) in curves_to_plot.items():
        if curve in logs.columns:
            ax.hist(logs[curve].dropna(), bins=15, color=color)
            ax.set_xlabel(xlabel)
            ax.set_ylabel('Frequency')

    # N-D Crossplot (if both NPHI and RHOB are available)
    if all(curve in logs.columns for curve in ['NPHI', 'RHOB']):
        points = ax5.scatter(logs.NPHI, logs.RHOB,
                           c=logs.GR if 'GR' in logs.columns else 'blue',
                           s=5, cmap="viridis")
        cbar = plt.colorbar(points)
        cbar.set_label('GR [API]', rotation=90, size=5)
        ax5.set_xlabel('NPHI [%]')
        ax5.set_ylabel('RHOB [g/cc]')
        # ax5.invert_yaxis()
        # ax5.invert_xaxis()
        ax5.grid(True)

        # Add axis limits (set constraints here)
        ax5.set_xlim(nphi_axis)  # Example for NPHI, adjust based on your data
        ax5.set_ylim(rhob_axis)

        # Plot clean and clay points if provided
        if all(v is not None for v in [neut_clean1, den_clean1, neut_clean2, den_clean2]):
            ax5.plot([neut_clean1, neut_clean2], [den_clean1, den_clean2],
                    marker='o', color='black', linewidth=1)
            ax5.text(neut_clean1, den_clean1, 'clean point 1', fontsize=6,
                    bbox=dict(boxstyle="round", fc="white", ec="0.5", alpha=0.8))
            ax5.text(neut_clean2 - 0.1, den_clean2 + 0.5, 'clean point 2', fontsize=6,
                    bbox=dict(boxstyle="round", fc="white", ec="0.5", alpha=0.8))

        if neut_clay is not None and den_clay is not None:
            ax5.plot(neut_clay, den_clay, 'ro', color='black', linewidth=1)
            ax5.text(neut_clay, den_clay, 'clay point', fontsize=6,
                    bbox=dict(boxstyle="round", fc="white", ec="0.5", alpha=0.8))

    # Plot VCL values
    vcl_curves = {
        'VCLGR': ('green', 'VCLGR'),
        'VCLND': ('red', 'VCLND'),
        'VCLSP': ('blue', 'VCLSP'),
        'VCLRT': ('purple', 'VCLRT')
    }

    for curve, (color, label) in vcl_curves.items():
        if curve in logs.columns:
            ax6.plot(logs[curve], logs[depth_col], label=label, color=color)

    ax6.legend(loc='best', fontsize='x-small')
    ax6.set_xlim(0, 1)
    ax6.set_ylim(depth_start, depth_end)
    ax6.invert_yaxis()
    ax6.grid(True)
    ax6.set_xlabel('VCL [v.v]')

    # return fig