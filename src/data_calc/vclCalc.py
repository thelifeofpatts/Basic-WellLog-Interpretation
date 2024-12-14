import numpy as np

def vclgr(gr_log, gr_clean, gr_clay, correction=None):

    igr=(gr_log-gr_clean)/(gr_clay-gr_clean)
    vclgr_larionov_young=0.083*(2**(3.7*igr)-1)
    vclgr_larionov_old=0.33*(2**(2*igr)-1)
    vclgr_clavier=1.7-(3.38-(igr+0.7)**2)**0.5
    vclgr_steiber=0.5*igr/(1.5-igr)

    if correction == "young":
        vclgr=vclgr_larionov_young
    elif correction == "older":
        vclgr=vclgr_larionov_old
    elif correction=="clavier":
        vclgr=vclgr_clavier
    elif correction=="steiber":
        vclgr=vclgr_steiber
    else:
        vclgr=igr
    return vclgr


def vclsp(sp_log, sp_clean, sp_clay):
    vclsp=(sp_log-sp_clean)/(sp_clay-sp_clean)
    return vclsp


def vclrt(rt_log, rt_clean, rt_clay):
    vrt = np.where( (rt_log == 0) | (rt_clean == rt_clay),
      np.nan,
      (rt_clay/rt_log)*(rt_clean-rt_log)/(rt_clean-rt_clay)
    )

    vclrt = np.where(rt_log > 2* rt_clay,
        0.5 * (2 * vrt)** (0.67*(vrt+1)),
        vrt
    )
    return vclrt

def vclnd(neut_log,den_log,neut_clean1,den_clean1,neut_clean2,den_clean2,neut_clay,den_clay):
    term1 = (den_clean2-den_clean1)*(neut_log-neut_clean1)-(den_log-den_clean1)*(neut_clean2-neut_clean1)
    term2 =(den_clean2-den_clean1)*(neut_clay-neut_clean1)-(den_clay-den_clean1)*(neut_clean2-neut_clean1)
    vclnd = term1/term2
    return vclnd