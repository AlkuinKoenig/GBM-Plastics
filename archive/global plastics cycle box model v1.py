
import numpy as np
import matplotlib.pyplot as plt


#Known M and F for the year 2015 used to estimate k values

M_produced=8300 #Geyer17 mass of all plastics in year 2015 produced since 1950
M_P_use=2600 #Geyer17 mass of all plastics in year 2015 still in use since 1950
f_MP=0.14 #Lau20: fraction of MP waste that is 'primary MP'
f_shelf=0.08
f_ocean=0.92
M_P_discard=4900*(1-f_MP) #Geyer17: Total discarded plastic pool of 4900 Tg multipled by (1-0.14) from Lau20
M_MP_discard=4900*f_MP #Geyer17: Total discarded plastic pool of 4900 Tg multipled by (0.14) from Lau20; this represents primary discarded MP
M_sMP_discard=75 #unknown, but estimated by iteration, because needed to calculate k_Disc sMP to atm
M_P_SurfOcean=0.23 #Eriksen14
M_MP_SurfOcean=0.036 #Eriksen14
M_sMP_SurfOcean=0.0028 #Poulain18
M_MPsMP_DeepOcean=80 #this study, based on observations
M_sMP_atmo=0.0036 #Brahney21
M_sMP_soil=29 #this study, based on observations
M_P beach #unknown
M_MP_beach=0.52 #this study, based on observations
M_P_sed #not in model at the moment
M_MP_sed=0.001
M_sMP_sed #unknown
M_Incinerated=800 #Geyer17 mass of all plastics in year 2015, incinerated since 1950
M_recycled=750 #Geyer17 mass of all plastics in year 2015, recycled since 1950

#only a few fluxes are observed and used to derive k values; I include the other fluxes in the model, to print them file later in the code
F_Pinuse to MPdisc
F_Pinuse to Pdisc
F_Pinuse to CO2
F_Pinuse recyled
F_Disc P to disc MP
F_Disc MP to disc sMP
F_P river
F_MP river
F_sMP river_from disc
F_sMP river_from soil
F_river_tot=0.0064 #base case value 0.0064 from Weiss21
F_Ocean P to MP
F_Ocean MP to sMP
F_sMP_oce to atm=8.6 # Brahney21
F_sMP_atm to oce=7.6 # Brahney21
F_P beaching
F_MP beaching
F_beach P to MP
F MP surf to deep oce
F sMP surf to deep oce
F MP surf to sediments
F sMP surf to sediments
F_sMP_soil to atm
F sMP atm to soil=1.15 # derived from Brahney21 global deposition
F sMP DiscInuse to atm=0.183 # Brahney21 sum of road emissions (in use) + population + agricultural dust

# all k have units of 1/y; since F=kM, often k values are calculated as k=F/M
LB19=0.03
k_SurfOce_P_to_MP=LB19 # From Lebreton19
k_SurfOce_MP_to_sMP=LB19
k_beach_P_to_MP=LB19
k_DeepOce_MP_to_sMP=LB19
CF1=5 #Correction Factor to fit a lower terrestrial fragmentation rate; see main text
k_Disc_P_to_MP=LB19/CF1
k_Disc_MP_to_sMP=LB19/CF1

k_P_surf_to_deep_oce=0 # P sinking not included in model; all P floats
k_MP_surf_to_deep_oce=196 #based on Long15: sMP sinking rate of 53.8 m/d=19637 m/y and a mixed layer depth of 100m: 19637/100=196 1/y 
k_sMP_surf_to_deep_oce=32.5 #based on Long15: sMP sinking rate of 8.91 m/d=3251 m/y and a mixed layer depth of 100m
k_P_Disc_to_river=F_river_tot/2/M_P_discard # factor 2 to account for 50% river plastics = P, and 50% = MP. sMP unknown
k_MP_Disc_to_river=F_river_tot/2/M_MP_discard # factor 2 to account for 50% river plastics = P, and 50% = MP. sMP unknown
k_sMP_Disc to river=k_MP_Disc_to_river #assumed equal to MP behavior

k_Disc_sMP_to_atm=F_sMP_DiscInuse_to_atm/M_sMP_discard
k_SurfOce_P_beach=0.77/5 #from Onink21 who estimated 77% beaching of P within 5 years since release from rivers
k_SurfOce_MP_beach=k_SurfOce_P_beach
k_SurfOce_P_CoastSed=0 #sinking and sedimentation of P not included in the model
k_SurfOce_MP_CoastSed=196 #as above, based on Long15, assuming the coastal ocean (over shelf) is 100m deep.
k_SurfOce_sMP_CoastSed=32.5 #as above, based on Long15, assuming the coastal ocean (over shelf) is 100m deep.

k_sMP_oce_to_atm=F_sMP_oce_to_atm/M_sMP_SurfOcean
k_sMP_soil_to_atm=k_Disc_sMP_to_atm
k_sMP_atm_to_oce=F_sMP_atm_to_oce/M_sMP_atmo
k_sMP_atm_to_soil=F_sMP_atm_to_soil/M_sMP_soil
k_sMP_soil_to_oce=k_sMP_Disc_to_river
k_P_beached_to_oce=0 #beached P return to ocean not included in model
k_MP_beached_to_oce=0 #beached MP return to ocean not included in model

#Production and waste forcing (you choose: interpolate the annual numbers, or use these approximations
P_prod=(0.1045809*time^2-409.084300*time+400055.2) #where time is 1950, 1951, ...2050
P_waste=0.000438727092*time^3-2.52227209*time^2+4831.80835*time-3084191.67 #where time is 1950, 1951, ...2050
f_disc=-0.000000017315*time^3+0.0000624932*time^2-0.0553287*time #before 1980=1; since 1980 use equation
f_incin=0.000000010866*time^3-0.000040095*time^2+0.0367815*time #before 1980=0; since 1980 use equation
f_rec=0.00712723*time-14.1653 #before 1989=0; since 1989 use equation

#ODEs (I do not know the exact python syntex for forumalating mass balance ODEs)

P_use[t]/dt=P_prod+f_rec*P_waste-f_inc*P_waste-f_disc*P_waste
d(P_disc)/dt=f_disc*P_waste×(1-f_MP)-k_P_Disc_to_river*P_disc-k_Disc_P_to_MP*P_disc
d(MP_disc)/dt=f_disc*P_waste×f_MP+k_Disc_P_to_MP*P_disc-k_MP_Disc_to_river*MP_disc-k_Disc_MP_to_sMP*MP_disc
d(sMP_disc)/dt=k_Disc_MP_to_sMP*MP_disc-k_sMP_Disc_to_river*sMP_disc-k_Disc_sMP_to_atm*sMP_disc
d(P_SurfOce)/dt=k_P_Disc_to_river*P_disc-k_SurfOce_P_beach*P_SurfOce
d(MP_SurfOce)/dt=k_MP_Disc_to_river*MP_disc-k_SurfOce_MP_beach*MP_SurfOce-k_SurfOce_MP_CoastSed*MP_SurfOce*f_shelf-k_MP_surf_to_deep_oce*MP_SurfOce
d(sMP_SurfOce)/dt=k_sMP_Disc_to_river*sMP_disc+k_sMP_atm_to_oce*sMP_atm+k_sMP_soil_to_oce*sMP_soil-k_sMP_oce_to_atm*sMP_SurfOce-k_sMPsed*sMP_SurfOce*f_shelf-k_sMP_surf_to_deep_oce*sMP_SurfOce
d(MP_DeepOce)/dt=-k_MP_surf_to_deep_oce*MP_SurfOce*f_pelagic-k_DeepOce_MP_to_sMP*MP_DeepOce
d(sMP_DeepOce)/dt=k_sMP_surf_to_deep_oce*sMP_SurfOce*f_pelagic+k_DeepOce_MP_to_sMP*MP_DeepOce
d(sMP_atm)/dt=k_Disc_sMP_to_atm*sMP_disc+k_sMP_atm_to_oce*sMP_SurfOce-k_sMP_atm_to_soil*sMP_atm-k_sMP_atm_to_oce*sMP_atm
d(sMP_soil)/dt=k_sMP_atm_to_soil*sMP_atm-k_sMP_soil_to_atm*sMP_soil-k_sMP_soil_to_oce*sMP_soil
d(P_beach)/dt=k_SurfOce_P_beach*P_SurfOce
d(MP_beach)/dt=k_SurfOce_MP_beach*MP_SurfOce
d(MP_sed)/dt=k_SurfOce_MP_CoastSed*MP_SurfOce*f_shelf
d(sMP_sed)/dt=k_SurfOce_sMP_CoastSed*sMP_SurfOce*f_shelf

# visualize data
