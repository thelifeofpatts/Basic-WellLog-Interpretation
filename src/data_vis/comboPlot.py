import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Create the figure and subplots
def combo_plot(data, top_depth, bottom_depth, figure_height,subplotadjust,SP_min,SP_max,CALI_min,CALI_max,GR_min,GR_max,DR_min,DR_max,MR_min,MR_max,SR_min,SR_max,RHOB_min,RHOB_max,NPHI_min,NPHI_max,DT_min,DT_max,smoothing_traject1,smoothing_traject2,smoothing_traject3,major_ticks_interval,minor_ticks_interval):

    logs=data[(data.DEPT >= top_depth) & (data.DEPT <= bottom_depth)]
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(12,figure_height), sharey=True) #pembuatan format 1 baris 3 kolom, width 12 height 10, dan sumbu y yang sama (sharey)
    fig.suptitle(f"LOG CURVE".upper(), fontsize=22)
    fig.subplots_adjust(top=subplotadjust,wspace=0.1)


    #General setting for all axis
    for axes in ax:
        axes.set_ylim (top_depth,bottom_depth)
        axes.invert_yaxis()
        axes.yaxis.grid(True)
        axes.yaxis.grid(True, which='minor', linestyle=':')
        axes.yaxis.grid(True, which='major', linestyle='-', linewidth='1')
        axes.yaxis.set_major_locator(ticker.MultipleLocator(major_ticks_interval))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(minor_ticks_interval))
        axes.get_xaxis().set_visible(False)

    #Smoothing the graph
    if (smoothing_traject1 == "yes"):
        logs.GR.dropna(inplace=True)
        logs.CALI.dropna(inplace=True)
        logs.SP.dropna(inplace=True)

        logs.GR = logs[["GR"]].apply(savgol_filter,  window_length=5, polyorder=3)
        logs.CALI = logs[["CALI"]].apply(savgol_filter,  window_length=5, polyorder=3)
        logs.SP = logs[["SP"]].apply(savgol_filter,  window_length=5, polyorder=3)

    if (smoothing_traject2 == "yes"):
        logs.DR.dropna(inplace=True)
        logs.MR.dropna(inplace=True)
        logs.SR.dropna(inplace=True)

        logs.DR = logs[["DR"]].apply(savgol_filter,  window_length=5, polyorder=3)
        logs.MR = logs[["MR"]].apply(savgol_filter,  window_length=5, polyorder=3)
        logs.SR = logs[["SR"]].apply(savgol_filter,  window_length=5, polyorder=3)

    if (smoothing_traject3 == "yes"):
        logs.RHOB.dropna(inplace=True)
        logs.NPHI.dropna(inplace=True)
        logs.DT.dropna(inplace=True)

        logs.RHOB = logs[["RHOB"]].apply(savgol_filter,  window_length=5, polyorder=3)
        logs.NPHI = logs[["NPHI"]].apply(savgol_filter,  window_length=5, polyorder=3)
        logs.DT = logs[["DT"]].apply(savgol_filter,  window_length=5, polyorder=3)

#First Trajectory: GR, CALI, SP
    #Gamma Ray lot
    if ("GR" in data.columns and (GR_min!=0 or GR_max!=0)):
        ax01=ax[0].twiny()
        if GR_min != "auto" and GR_max != "auto":
            ax01.set_xlim(GR_min,GR_max)
        ax01.yaxis.grid(True, which='major', linestyle='-', linewidth='1')
        ax01.yaxis.set_major_locator(ticker.MultipleLocator(50))
        ax01.plot(logs.GR, logs.DEPT, label='GR[api]', color='green')
        ax01.spines['top'].set_position(('outward',80))
        ax01.set_xlabel('GR[api]',color='green')
        ax01.tick_params(axis='x', colors='green')

    #Caliper Plot
    if ("CALI" in data.columns and (CALI_min!=0 or CALI_max!=0)):
        ax02=ax[0].twiny()
        if CALI_min != "auto" and CALI_max != "auto":
            ax02.set_xlim(CALI_min,CALI_max)
        ax02.plot(logs.CALI, logs.DEPT, '--', label='CALN[in]', color='black')
        ax02.spines['top'].set_position(('outward',40))
        ax02.set_xlabel('CALI[in]',color='black')
        ax02.tick_params(axis='x', colors='black')
        #ax02.axvline(x=7.9, linewidth=2, color='black') #digunakan untuk plot bit size ukuran 7.9 in

    #Spontaneous Potential Plot
    if ("SP" in data.columns and (SP_min!=0 or SP_max!=0)):
        ax03=ax[0].twiny()
        if SP_min != "auto" and SP_max != "auto":
            ax03.set_xlim(SP_min,SP_max)
        ax03.spines['top'].set_position(('outward',0))
        ax03.set_xlabel("SP [mV]")
        ax03.plot(logs.SP, logs.DEPT, label='SP[mV]', color='blue')
        ax03.set_xlabel('SP[mV]',color='blue')
        ax03.tick_params(axis='x', colors='blue')
        ax03.grid(True)


#Second Trajectory: DR, MR, SR
    #Deep Resistivity Plot
    if ("DR" in data.columns and (DR_min!=0 or DR_max!=0)):
        ax11=ax[1].twiny()
        if DR_min != "auto" and DR_max != "auto":
            ax11.set_xlim(DR_min,DR_max)
        ax11.set_xscale('log')
        ax11.grid(visible=None, which='both')
        ax11.spines['top'].set_position(('outward',80))
        ax11.set_xlabel('Deep Resistivity [ohm.m]', color='red')
        ax11.plot(logs.DR, logs.DEPT, label='DR [ohm.m]', color='red')
        ax11.tick_params(axis='x', colors='red')

    #Medium Resistivity Plot
    if("MR" in data.columns and (MR_min!=0 or MR_max!=0)):
        ax12=ax[1].twiny()
        if MR_min != "auto" and MR_max != "auto":
            ax12.set_xlim(MR_min,MR_max)
        ax12.set_xscale('log')
        ax12.grid(visible=None, which='both')
        ax12.spines['top'].set_position(('outward',40))
        ax12.set_xlabel('Medium Resistivity [ohm.m]', color='purple')
        ax12.plot(logs.MR, logs.DEPT, label='MR [ohm.m]', color='purple')
        ax12.tick_params(axis='x', colors='purple')

    #Shallow Resistivity Plot
    if("SR" in data.columns and (SR_min!=0 or SR_max!=0)):
        ax13=ax[1].twiny()
        if SR_min != "auto" and SR_max != "auto":
            ax13.set_xlim(SR_min,SR_max)
        ax13.set_xscale('log')
        ax13.grid(visible=None, which='both')
        ax13.spines['top'].set_position(('outward',0))
        ax13.set_xlabel('Shallow Resistivity [ohm.m]',color='black')
        ax13.plot(logs.SR, logs.DEPT, '--',label='SR[ohm.m]', color='black')
        ax13.tick_params(axis='x', colors='black')


#Third Trajectory: RHOB, NPHI, DT
    #Density Plot
    if ("RHOB" in data.columns and (RHOB_min!=0 or RHOB_max!=0)):
        ax21=ax[2].twiny()
        if RHOB_min != "auto" and RHOB_max != "auto":
            ax21.set_xlim(RHOB_min,RHOB_max)
        ax21.plot(logs.RHOB, logs.DEPT ,label='RHOB[g/cc]', color='red')
        ax21.spines['top'].set_position(('outward',80))
        ax21.set_xlabel('RHOB[g/cc]',color='red')
        ax21.tick_params(axis='x', colors='red')

    #Neutron Porosity Plot
    if ("NPHI" in data.columns and (NPHI_min!=0 or NPHI_max!=0)):
        ax22=ax[2].twiny()
        if NPHI_min != "auto" and NPHI_max != "auto":
            ax22.set_xlim(NPHI_min,NPHI_max)
        ax22.invert_xaxis()
        ax22.plot(logs.NPHI, logs.DEPT, label='NPHI[%]', color='green')
        ax22.spines['top'].set_position(('outward',40))
        ax22.set_xlabel('NPHI[%]', color='green')
        ax22.tick_params(axis='x', colors='green')

    #Sonic Plot
    if ("DT" in data.columns and (DT_min!=0 or DT_max!=0)):
        ax23=ax[2].twiny()
        ax23.grid(True, which='both')
        if DT_min != "auto" and DT_max != "auto":
            ax23.set_xlim(DT_min,DT_max)
        ax23.spines['top'].set_position(('outward',0))
        ax23.set_xlabel('DT[us/ft]')
        ax23.plot(logs.DT, logs.DEPT, label='DT[us/ft]', color='blue')
        ax23.set_xlabel('DT[us/ft]', color='blue')
        ax23.tick_params(axis='x', colors='blue')

def custom_plot(logs, fig_height, depth_start, depth_end, *custom_logs, units):
    num_tracks = len(custom_logs)
    fig, ax = plt.subplots(nrows=1, ncols=num_tracks, figsize=(15, fig_height), sharey=True)
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

    # consider edge case where ax is not iterable
    if not hasattr(ax, '__iter__'):  # edge case where ax is not iterable
        ax = [ax]
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