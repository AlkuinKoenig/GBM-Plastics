import numpy as np
import json
from datetime import datetime

#NOTE that in the manuscript large microplastics and small micropalstics are termed LMP and SMP; in the model below they are still called MP and sMP
#saving k values within a class because it's convenient
class boxmodel_parameters:    
    f_MP = 0.14  # Lau Winnie et al. 2020, Science: fraction of MP waste that is 'primary MP'
    f_shelf = 0.08
    f_ocean = 0.92
    M_P_discard = 4900 * (1 - f_MP)  # Geyer et al. 2017, Science Advances: Total discarded plastic pool of 4900 Tg multipled by (1-0.14) from Lau20
    M_MP_discard = 4900 * f_MP  # Geyer17: Total discarded plastic pool of 4900 Tg multipled by (0.14) from Lau20; this represents primary discarded MP
    M_sMP_discard = 524 # unknown, but estimated by one single iteration, because needed to calculate k_Disc sMP to atm
    M_P_SurfOcean = 0.23  # Eriksen et al. 2014, PLOS-One
    M_MP_SurfOcean = 0.036  # Eriksen et al. 2014, PLOS-One
    M_sMP_SurfOcean = 0.0028  # Poulain et al. 2018, ES&T
    M_MPsMP_DeepOcean = 82  # this study, based on observations
    M_sMP_atmo = 0.0036  # Brahney et al. 2021, PNAS
    M_sMP_soil = 28  # this study, based on observations
    M_P_beach = 1.32  #  this study, based on observations
    M_MP_beach = 0.53  # this study, based on observations
    M_P_ShelfSed = 50.6  #  this study, based on observations
    M_MP_ShelfSed = 65.3 #  this study, based on observations
    M_Incinerated = 800  # Geyer17 mass of all plastics in year 2015, incinerated since 1950
    M_recycled = 750  # Geyer17 mass of all plastics in year 2015, recycled since 1950

    # only a few fluxes are observed and used to derive k values; The non-observed fluxes are computed in the model, to print them to file later in the code
    #F_Pinuse_to_MPdisc
    #F_Pinuse_to_Pdisc
    #F_Pinuse_to_CO2
    #F_Pinuse_recyled
    #F_Disc_P_to_disc
    #MP_F_Disc_MP_to_disc_sMP
    #F_P_river
    #F_MP_river
    #F_sMP_river_from_disc
    #F_sMP_river_from_soil
    #F_river_tot = 0.0064  # base case value 0.0064 from Weis et al. 2021
    F_river_tot = 8.5  #approximate river total plastics flux in Tg/y based on Jambeck et al. 2015 Science (midpoint value between 4 and 13)
    #F_Ocean_P_to_MP
    #F_Ocean
    #MP_to_sMP
    F_sMP_oce_to_atm = 8.6  # Brahney et al., 2021, PNAS
    F_sMP_atm_to_oce = 7.6  # this study, estimated as total deposition from Brahney et al., 2021, PNAS minus deposition to land
    #F_P_beaching
    #F_MP_beaching
    #F_beach_P_to_MP
    #F_MP_surf_to_deep_oce
    #F_sMP_surf_to_deep_oce
    #F_MP_surf_to_sediments
    #F_sMP_surf_to_sediments
    #F_sMP_soil_to_atm
    F_sMP_atm_to_soil = 1.15  # this study, based on extrapolated observations
    F_sMP_DiscInuse_to_atm = 0.183  # Brahney et al. 2021 sum of road emissions (from in use reservoir) + population + agricultural dust (from discarded sMP reservoir)

    # all k have units of 1/y; since F=kM, often k values are calculated as k=F/M
    LB19 = 0.03  # Plastics degradation rate in 'per year' untis From Lebreton et al. 2019, NCOMMS. Below this rate is applied to P to LMP degradation adn LMP to SMP degradation in all environments
    k_SurfOce_P_to_MP = LB19
    k_SurfOce_MP_to_sMP = LB19
    k_beach_P_to_MP = LB19
    k_beach_MP_to_sMP = LB19
    
    k_DeepOce_MP_to_sMP = LB19
    CF1 = 1  # Correction Factor to fit a lower terrestrial fragmentation rate; not currently used and therefore set to 1
    k_Disc_P_to_MP = LB19 / CF1
    k_Disc_MP_to_sMP = LB19 / CF1

    k_P_surf_to_deep_oce = 0 #not included in model because we assume open ocean P to be buoyant, but approx 1367 y-1, based on Long et al. 2015, ES&T: sMP sinking rate of 375 m/d=136700 m/y and a mixed layer depth of 100m: 136700/100=1367 y-1
    k_MP_surf_to_deep_oce = 196  # based on Long et al. 2015, ES&T: sMP sinking rate of 53.8 m/d=19637 m/y and a mixed layer depth of 100m: 19637/100=196 1/y
    k_sMP_surf_to_deep_oce = 32.5  # based on Long et al. 2015, ES&T: sMP sinking rate of 8.91 m/d=3251 m/y and a mixed layer depth of 100m
    f_P_river = 0.5 # based on Weis et al. 2021 Science SI
    f_MPsMP_river = 1 - f_P_river
    k_P_Disc_to_river = F_river_tot * f_P_river / M_P_discard  #
    k_MP_Disc_to_river = F_river_tot * f_MPsMP_river / M_MP_discard  #
    k_sMP_Disc_to_river = k_MP_Disc_to_river  # assumed equal to MP behavior

    k_Disc_sMP_to_atm = F_sMP_DiscInuse_to_atm / M_sMP_discard
    k_SurfOce_P_beach = 0.77 / 5 * 26  # from Onink21 who estimated 77% beaching of P within 5 years since release from rivers; 26 is a fitting constant
    k_SurfOce_MP_beach = k_SurfOce_P_beach
    k_SurfOce_P_ShelfSed = 1367  # as above, based on Long et al. 2015, assuming the global Coastal ocean (over shelf) is 100m deep.
    k_SurfOce_MP_ShelfSed = 196  # as above, based on Long et al. 2015, assuming the global Coastal ocean (over shelf) is 100m deep.
    k_SurfOce_sMP_ShelfSed = 32.5  # as above, based on Long et al. 2015, assuming the global Coastal ocean (over shelf) is 100m deep.
    k_DeepOce_MP_DeepSed = 0.00123  # fitted
    k_DeepOce_sMP_DeepSed = 0.000203  # fitted
    
    k_sMP_oce_to_atm = F_sMP_oce_to_atm / M_sMP_SurfOcean
    k_sMP_soil_to_atm = k_Disc_sMP_to_atm
    k_sMP_atm_to_oce = F_sMP_atm_to_oce / M_sMP_atmo
    k_sMP_atm_to_soil = F_sMP_atm_to_soil / M_sMP_atmo
    k_sMP_soil_to_oce = k_sMP_Disc_to_river
    k_P_beached_to_oce = 0  # beached P return to ocean not included in model
    k_MP_beached_to_oce = 0  # beached MP return to ocean not included in model


###now saving this as a json. Creating the timestamp
now = datetime.now()
current_time = now.strftime("%Y%m%d_%H%M")

outdir = "./"
fname = "PARS_BASE_V2_" + current_time + ".json"

print(f"\nSaving base case to {outdir + fname}")


#first, get the variables from boxmodel_parameters class as dictionary
pardict =  {k:v for k, v in boxmodel_parameters.__dict__.items() if not (k.startswith('__')
                                                             and k.endswith('__'))}

#saving this as json.
with open(outdir + fname, "w") as write_file:
    json.dump(pardict, write_file, indent = 4)

