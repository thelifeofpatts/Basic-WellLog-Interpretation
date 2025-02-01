import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import scipy

def interpretation_plot(logs, core_selected_data, fig_height, depth_start, depth_end, SP_min, SP_max, CALI_min, CALI_max, GR_min, GR_max, DR_min, DR_max, MR_min, MR_max, SR_min, SR_max, RHOB_min, RHOB_max, NPHI_min, NPHI_max, DT_min, DT_max, perm,fill):
    fig, ax = plt.subplots(nrows=1, ncols=7, figsize=(12,fig_height), sharey=True)
    fig.suptitle("Interpretation Plot", fontsize=22)
    fig.subplots_adjust(top=0.85,wspace=0.2)

    depth_range = depth_end - depth_start
    if depth_range > 5000:
      major_tick_interval = 1000
      minor_tick_interval = 100
    elif depth_range > 1000:
      major_tick_interval = 500
      minor_tick_interval = 50
    else:
      major_tick_interval = 100
      minor_tick_interval = 10

    #General setting for all axis
    for axes in ax:
        axes.set_ylim (depth_start,depth_end)
        axes.invert_yaxis()
        axes.yaxis.grid(True, which='minor', linestyle=':')
        axes.yaxis.grid(True, which='major', linestyle='-', linewidth='1')
        axes.yaxis.set_major_locator(ticker.MultipleLocator(major_tick_interval))
        axes.yaxis.set_minor_locator(ticker.MultipleLocator(minor_tick_interval))
        axes.get_xaxis().set_visible(False)


    #1st track: GR, SP, CALI track
    if 'SP' in logs.columns:
      ax01=ax[0].twiny()
      if SP_min != "auto" and SP_max != "auto":
        ax01.set_xlim(SP_min,SP_max)
      ax01.plot(logs.SP, logs.DEPT, label='SP[mV]', color='blue')
      ax01.set_xlabel('SP[mV]',color='blue')
      ax01.tick_params(axis='x', colors='blue')
    if 'CALI' in logs.columns:
      ax02=ax[0].twiny()
      if CALI_min != "auto" and CALI_max != "auto":
        ax02.set_xlim(CALI_min,CALI_max)
      ax02.grid(True)
      ax02.plot(logs.CALI, logs.DEPT, '--', label='CALI[in]', color='black')
      ax02.spines['top'].set_position(('outward',40))
      ax02.set_xlabel('CALI[in]',color='black')
      ax02.tick_params(axis='x', colors='black')
    if 'GR' in logs.columns:
      ax03=ax[0].twiny()
      if GR_min != "auto" and GR_max != "auto":
        ax03.set_xlim(GR_min,GR_max)
      ax03.plot(logs.GR, logs.DEPT, label='GR[api]', color='green')
      ax03.spines['top'].set_position(('outward',80))
      ax03.set_xlabel('GR[api]',color='green')
      ax03.tick_params(axis='x', colors='green')



    #2nd track: Resistivities
    ax11=ax[1].twiny()
    if DR_min != "auto" and DR_max != "auto":
        ax11.set_xlim(DR_min,DR_max)
    ax11.set_xscale('log')
    ax11.grid(True, which="both")
    ax11.spines['top'].set_position(('outward',80))
    ax11.set_xlabel('DR[m.ohm]', color='red')
    ax11.plot(logs.DR, logs.DEPT, label='DR[m.ohm]', color='red')
    ax11.tick_params(axis='x', colors='red')

    ax12=ax[1].twiny()
    if MR_min != "auto" and MR_max != "auto":
        ax12.set_xlim(MR_min,MR_max)
    ax12.set_xscale('log')
    ax12.plot(logs.MR, logs.DEPT, label='MR[m.ohm]', color='purple')
    ax12.spines['top'].set_position(('outward',40))
    ax12.set_xlabel('MR[m.ohm]', color='purple')
    ax12.tick_params(axis='x', colors='purple')

    ax13=ax[1].twiny()
    if SR_min != "auto" and SR_max != "auto":
        ax13.set_xlim(SR_min,SR_max)
    ax13.set_xscale('log')
    ax13.plot(logs.SR, logs.DEPT, '--',label='SR[m.ohm]', color='black')
    ax13.spines['top'].set_position(('outward',0))
    ax13.set_xlabel('SR[m.ohm]',color='black')
    ax13.tick_params(axis='x', colors='black')



    #3rd track: DT, RHOB, NPHI track
    # ax21=ax[2].twiny()
    # ax21.grid(True)
    # if DT_min != "auto" and DT_max != "auto":
    #     ax21.set_xlim(DT_min,DT_max)
    # ax21.spines['top'].set_position(('outward',0))
    # ax21.set_xlabel('DT[us/ft]')
    # ax21.plot(logs.DT, logs.DEPT, label='DT[us/ft]', color='blue')
    # ax21.set_xlabel('DT[us/ft]', color='blue')
    # ax21.tick_params(axis='x', colors='blue')

    ax22=ax[2].twiny()
    if NPHI_min != "auto" and NPHI_max != "auto":
        ax22.set_xlim(NPHI_min,NPHI_max)
    ax22.invert_xaxis()
    ax22.plot(logs.NPHI, logs.DEPT, label='NPHI[%]', color='green')
    ax22.spines['top'].set_position(('outward',40))
    ax22.set_xlabel('NPHI[%]', color='green')
    ax22.tick_params(axis='x', colors='green')

    ax23=ax[2].twiny()
    if RHOB_min != "auto" and RHOB_max != "auto":
        ax23.set_xlim(RHOB_min,RHOB_max)
    ax23.plot(logs.RHOB, logs.DEPT ,label='RHOB[g/cc]', color='red')
    ax23.spines['top'].set_position(('outward',80))
    ax23.set_xlabel('RHOB[g/cc]',color='red')
    ax23.tick_params(axis='x', colors='red')



    #4th track: SW
    ax31=ax[3].twiny()
    ax31.grid(True)
    ax31.set_xlim(1,0)
    if fill == "yes":
        # ax31.fill_betweenx(logs.DEPT,logs.SWarchie,logs.SWwaxman,color='lightgreen',label='waxman - archie')
        # ax31.fill_betweenx(logs.DEPT,logs.SWarchie,logs.SWindonesia,color='lightblue',label='indonesia - archie')
        ax31.fill_betweenx(logs.DEPT,logs.SWarchie,logs.SWsimandoux,color='red',label='simandoux - archie')
    ax31.plot(logs.SWarchie, logs.DEPT, label='SW[Archie]', color='black',linewidth=1)
    ax31.spines['top'].set_position(('outward',0))
    ax31.set_xlabel('SW Archie [frac]', color='black')
    ax31.tick_params(axis='x', colors='black')

    # ax32=ax[3].twiny()
    # ax32.set_xlim(1,0)
    # ax32.plot(logs.SWwaxman, logs.DEPT, label="SW[Waxman]",color="red")
    # ax32.spines['top'].set_position(('outward',40))
    # ax32.set_xlabel('SW Waxman [frac]', color='red')
    # ax32.tick_params(axis='x', colors='red')

    # ax33=ax[3].twiny()
    # ax33.set_xlim(1,0)
    # ax33.plot(logs["SWindonesia"], logs.DEPT, label="SW[Indonesia]",color="blue")
    # ax33.spines['top'].set_position(('outward',80))
    # ax33.set_xlabel('SW Indonesia [frac]', color='blue')
    # ax33.tick_params(axis='x', colors='blue')

    ax32=ax[3].twiny()
    ax32.set_xlim(1,0)
    ax32.plot(logs["SWsimandoux"], logs.DEPT, label="SW[simandoux]",color="green")
    ax32.spines['top'].set_position(('outward',40))
    ax32.set_xlabel('SW simandoux [frac]', color='green')
    ax32.tick_params(axis='x', colors='green')


    #4th track: Permeability
    ax41=ax[4].twiny()
    ax41.plot(logs[perm], logs.DEPT, label="perm",color="green")
    ax41.spines['top'].set_position(('outward',0))
    ax41.set_xlabel('PERM [mD]', color='green')
    ax41.tick_params(axis='x', colors='green')

    ax42=ax[4].twiny()
    ax42.scatter(core_selected_data.core_perm, core_selected_data.DEPT, label='C_PERM', color='red',linewidths=0.5)
    ax42.spines['top'].set_position(('outward',40))
    ax42.set_xlabel('PERM-CORE', color='red')
    ax42.tick_params(axis='x', colors='red')



    #5th track: PHIE, BVW
    ax51=ax[5].twiny()
    ax51.grid(True)
    ax51.set_xlim(1,0)
    ax51.plot(logs.PHIE, logs.DEPT, label='PHIE', color='black', linewidth=0.5, alpha=0.5)
    ax51.fill_betweenx(logs.DEPT,0,logs.BVW,color='lightblue', alpha=0.5)
    ax51.spines['top'].set_position(('outward',0))
    ax51.set_xlabel('PHIE-LOG', color='black')
    ax51.tick_params(axis='x', colors='black')

    ax52=ax[5].twiny()
    ax52.set_xlim(1,0)
    ax52.plot(logs.BVW, logs.DEPT, label='BVW', color='black', alpha=0.5)
    ax52.fill_betweenx(logs.DEPT,logs.PHIE, logs.BVW,color='green',alpha=0.2)
    ax52.scatter(core_selected_data.core_por, core_selected_data.DEPT, label='C_PHIE', color='red',linewidths=0.5)
    ax52.spines['top'].set_position(('outward',40))
    ax52.set_xlabel('BVW', color='black')
    ax52.tick_params(axis='x', colors='black')

    ax53=ax[5].twiny()
    ax53.set_xlim(1,0)
    ax53.scatter(core_selected_data.core_por, core_selected_data.DEPT, label='C_PHIE', color='red',linewidths=0.5)
    ax53.spines['top'].set_position(('outward',80))
    ax53.set_xlabel('PHIE-CORE', color='red')
    ax53.tick_params(axis='x', colors='red')



    #6th track: PHIE, MATRIX, VCL
    ax60=ax[6].twiny()
    ax60.set_xlim(1,0)
    ax60.spines['top'].set_position(('outward',0))
    ax60.plot(logs.PHIE, logs.DEPT, label='PHIE', color='black',linewidth=0.5)
    ax60.set_xlabel('Porosity', color='blue')
    ax60.tick_params(axis='x', colors='blue')

    ax61=ax[6].twiny()
    ax61.set_xlim(0,1)
    ax61.spines['top'].set_position(('outward',40))
    ax61.plot(logs.VCL, logs.DEPT, label='VCL', color='green',linewidth=0.5)
    ax61.set_xlabel('VClay', color='green')
    ax61.tick_params(axis='x', colors='green')

    ax62=ax[6].twiny()
    ax62.set_xlim(1,0)
    ax62.spines['top'].set_position(('outward',80))
    ax62.fill_betweenx(logs.DEPT,0,logs.PHIE,color='lightgray',label='porosity')
    ax62.fill_betweenx(logs.DEPT,logs.PHIE,1-logs.VCL,color='orange',label='matrix')
    ax62.fill_betweenx(logs.DEPT,1-logs.VCL,1,color='lightgreen',label= 'Vclay')
    ax62.set_xlabel('Matrix', color='orange')
    ax62.tick_params(axis='x', colors='orange')
    ax62.legend(loc='lower left')

def pickett_plot(logs, vcl_limit, a, rwa, m, n, z):
    plt.figure(figsize=(7,6))
    plt.title('Pickett Plot'+ ' for VCL < '+ str(int(vcl_limit*100)) + '%' + " and Rw = " + str(rwa) + " ohm.m")
    c = logs[z][logs.VCL<vcl_limit]
    plt.scatter(logs.DR[logs.VCL<vcl_limit], logs.PHIE[logs.VCL<vcl_limit],c=c, s=20, cmap="plasma")
    cbar = plt.colorbar()
    cbar.set_label(f'{z}')
    plt.xlim(0.1,1000)
    plt.ylim(0.01,1)
    plt.ylabel('PHIE [v/v]')
    plt.xlabel('DR [m.ohm]')
    plt.gca().xaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))
    plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))
    plt.gca().set_xscale('log')
    plt.gca().set_yscale('log')

    #calculate the saturation lines
    sw_plot=(1.0,0.8,0.6,0.4,0.2)
    phie_plot=(0.01,1)
    rt_plot=np.zeros((len(sw_plot),len(phie_plot)))

    for i in range (0,len(sw_plot)):
        for j in range (0,len(phie_plot)):
            rt_result=((a*rwa)/(sw_plot[i]**n)/(phie_plot[j]**m))
            rt_plot[i,j]=rt_result
    for i in range(0,len(sw_plot)):
        plt.plot(rt_plot[i],phie_plot, label='SW '+str(int(sw_plot[i]*100))+'%')
        plt.legend (loc='best')

    plt.grid(True, which='both',ls='-',color='gray')