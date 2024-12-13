import seaborn as sns
import matplotlib.pyplot as plt

def boxplot(data, columns_to_plot, columns_unit):
    # Define the list of columns you want to create subplots for
    columns = columns_to_plot #["GR", "CALI", "SP", "DR", "MR", "SR", "NPHI", "RHOB", "DT"]
    units = columns_unit #["in", "API", "mV", "ohm/m", "ohm.m", "ohm.m", "v/v", "g/cm³", "us/ft"]

    # Get unique wells and assign colors
    wells = data['WELL'].unique()
    colors = sns.color_palette('viridis', n_colors=len(wells))

    # Set the figure size for the overall plot
    plt.figure(figsize=(16, 12))

    # Create subplots for each selected column
    for i, column in enumerate(columns, 1):
        plt.subplot(3, 3, i)  # Create a 3x3 grid of subplots

        # Plot boxplots for each well with different colors
        for well, color in zip(wells, colors):
            well_data = data[data['WELL'] == well]
            sns.boxplot(x=well_data[column], y=data["WELL"], color=color)

        plt.title(f'Boxplot for {column}', fontsize=12)  # Set the title for the subplot
        plt.xlabel(f'{column} [{units[i-1]}]', fontsize=10)  # Set the x-axis label with the corresponding unit
        plt.ylabel('Frequency', fontsize=10)  # Set the y-axis label as 'Frequency'

    # Add an overall title for the set of subplots
    plt.suptitle("DATA DISTRIBUTION (BOX PLOT)\n", fontsize=16, fontweight='bold')

    # Create a custom legend outside the subplots
    legend_handles = [plt.Line2D([0], [0], marker='o', color='w', label=well, markerfacecolor=color, markersize=10) for well, color in zip(wells, colors)]
    plt.legend(handles=legend_handles, title='WELL', bbox_to_anchor=(1.05, 1), loc='upper left')

    # Adjust the layout and display the plot
    plt.tight_layout()
    plt.show()


def histplot(data, columns_to_plot, columns_unit):
    # Get unique wells and assign colors
    wells = data['WELL'].unique()
    colors = sns.color_palette('viridis', n_colors=len(wells))

    # Create subplots for histograms
    fig, axes = plt.subplots(3, 3, figsize=(12, 10))
    fig.suptitle('DATA DISTRIBUTION (HISTOGRAM PLOT) \n', fontsize=14, fontweight='bold')
    fig.subplots_adjust(top=0.95, wspace=0.3, hspace=0.3)

    # List of columns and their corresponding units
    columns = columns_to_plot
    units = columns_unit

    for i, ax in enumerate(axes.flat):
        if i < len(columns):
            column_name = columns[i]
            column_unit = units[i]  # Specify the unit for the column
            ax.set_title(column_name)

            # Plot histograms for each well with different colors
            for well, color in zip(wells, colors):
                well_data = data[data['WELL'] == well]
                sns.histplot(well_data[column_name].dropna(), bins=50, color=color, ax=ax, kde=True, label=well)

            ax.set_xlabel(f"{column_name} [{column_unit}]")  # Include the specified unit in the x-axis label
            ax.legend(title='WELL')

    # Remove empty subplots if there are more plots than columns
    if len(columns) < len(axes.flat):
        for i in range(len(columns), len(axes.flat)):
            fig.delaxes(axes.flat[i])

    # Adjust the layout and display the plot
    plt.tight_layout()
    plt.show()

def densityplot(data, columns_to_plot, columns_unit):
    wells = data['WELL'].unique()
    colors = sns.color_palette('viridis', n_colors=len(wells))  # Add this line

    # Group the data by 'WELL' and create subplots
    fig, axes = plt.subplots(3, 3, figsize=(12, 10))
    fig.suptitle('DATA DISTRIBUTION (DENSITY PLOT)\n', fontsize=16)
    fig.subplots_adjust(top=0.95, wspace=0.3, hspace=0.3)

    # List of columns and their corresponding units
    columns = columns_to_plot
    units = columns_unit

    for i, ax in enumerate(axes.flat):
        if i < len(columns):
            column_name = columns[i]
            column_unit = units[i]  # Specify the unit for the column
            ax.set_title(column_name)

            # Plot density plots for each well with different colors
            for well, color in zip(wells, colors):
                well_data = data[data['WELL'] == well]
                well_data[column_name].plot(kind='kde', ax=ax, label=well, color=color)

            ax.set_xlabel(f"{column_name} [{column_unit}]")  # Include the specified unit in the x-axis label
            ax.set_ylabel("Frequency")
            ax.legend(title='WELL')

    # Remove any remaining empty subplots
    if len(columns) < len(axes.flat):
        for i in range(len(columns), len(axes.flat)):
            fig.delaxes(axes.flat[i])

    plt.tight_layout()
    plt.show()
