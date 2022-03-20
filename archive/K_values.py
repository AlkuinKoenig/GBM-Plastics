import numpy as np
class parameters:
    f_MP = 0.14  # Lau20: fraction of MP waste that is 'primary MP'
    f_shelf = 0.08
    f_ocean = 0.92
    M_P_discard = 4900 * (1 - f_MP)  # Geyer17: Total discarded plastic pool of 4900 Tg multipled by (1-0.14) from Lau20
    M_MP_discard = 4900 * f_MP  # Geyer17: Total discarded plastic pool of 4900 Tg multipled by (0.14) from Lau20; this represents primary discarded MP
    M_sMP_discard = 75  # unknown, but estimated by iteration, because needed to calculate k_Disc sMP to atm
    M_P_SurfOcean = 0.23  # Eriksen14
    M_MP_SurfOcean = 0.036  # Eriksen14
    M_sMP_SurfOcean = 0.0028  # Poulain18
    M_MPsMP_DeepOcean = 80  # this study, based on observations
    M_sMP_atmo = 0.0036  # Brahney21
    M_sMP_soil = 29  # this study, based on observations
    #M_P_beach  # unknown
    M_MP_beach = 0.52  # this study, based on observations
    #M_P_sed  # not in model at the moment
    M_MP_sed = 0.001
    #M_sMP_sed  # unknown
    M_Incinerated = 800  # Geyer17 mass of all plastics in year 2015, incinerated since 1950
    M_recycled = 750  # Geyer17 mass of all plastics in year 2015, recycled since 1950

    # only a few fluxes are observed and used to derive k values; I include the other fluxes in the model, to print them file later in the code
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
    F_river_tot = 0.0064  # base case value 0.0064 from Weiss21
    #F_Ocean_P_to_MP
    #F_Ocean
    #MP_to_sMP
    F_sMP_oce_to_atm = 8.6  # Brahney21
    F_sMP_atm_to_oce = 7.6  # Brahney21
    #F_P_beaching
    #F_MP_beaching
    #F_beach_P_to_MP
    #F_MP_surf_to_deep_oce
    #F_sMP_surf_to_deep_oce
    #F_MP_surf_to_sediments
    #F_sMP_surf_to_sediments
    #F_sMP_soil_to_atm
    F_sMP_atm_to_soil = 1.15  # derived from Brahney21 global deposition
    F_sMP_DiscInuse_to_atm = 0.183  # Brahney21 sum of road emissions (in use) + population + agricultural dust

    # all k have units of 1/y; since F=kM, often k values are calculated as k=F/M
    LB19 = 0.03
    k_SurfOce_P_to_MP = LB19  # From Lebreton19
    k_SurfOce_MP_to_sMP = LB19
    k_beach_P_to_MP = LB19
    k_DeepOce_MP_to_sMP = LB19
    CF1 = 5  # Correction Factor to fit a lower terrestrial fragmentation rate; see main text
    k_Disc_P_to_MP = LB19 / CF1
    k_Disc_MP_to_sMP = LB19 / CF1

    k_P_surf_to_deep_oce = 0  # P sinking not included in model; all P floats
    k_MP_surf_to_deep_oce = 196  # based on Long15: sMP sinking rate of 53.8 m/d=19637 m/y and a mixed layer depth of 100m: 19637/100=196 1/y
    k_sMP_surf_to_deep_oce = 32.5  # based on Long15: sMP sinking rate of 8.91 m/d=3251 m/y and a mixed layer depth of 100m
    k_P_Disc_to_river = F_river_tot / 2 / M_P_discard  # factor 2 to account for 50% river plastics = P, and 50% = MP. sMP unknown
    k_MP_Disc_to_river = F_river_tot / 2 / M_MP_discard  # factor 2 to account for 50% river plastics = P, and 50% = MP. sMP unknown
    k_sMP_Disc_to_river = k_MP_Disc_to_river  # assumed equal to MP behavior

    k_Disc_sMP_to_atm = F_sMP_DiscInuse_to_atm / M_sMP_discard
    k_SurfOce_P_beach = 0.77 / 5  # from Onink21 who estimated 77% beaching of P within 5 years since release from rivers
    k_SurfOce_MP_beach = k_SurfOce_P_beach
    k_SurfOce_P_CoastSed = 0  # sinking and sedimentation of P not included in the model
    k_SurfOce_MP_CoastSed = 196  # as above, based on Long15, assuming the coastal ocean (over shelf) is 100m deep.
    k_SurfOce_sMP_CoastSed = 32.5  # as above, based on Long15, assuming the coastal ocean (over shelf) is 100m deep.

    k_sMP_oce_to_atm = F_sMP_oce_to_atm / M_sMP_SurfOcean
    k_sMP_soil_to_atm = k_Disc_sMP_to_atm
    k_sMP_atm_to_oce = F_sMP_atm_to_oce / M_sMP_atmo
    k_sMP_atm_to_soil = F_sMP_atm_to_soil / M_sMP_soil
    k_sMP_soil_to_oce = k_sMP_Disc_to_river
    k_P_beached_to_oce = 0  # beached P return to ocean not included in model
    k_MP_beached_to_oce = 0  # beached MP return to ocean not included in model

    def get_P_prod(self,time):
        P_prod = np.where(time < 1950, 0, (0.1045809 * time ** 2 - 409.084300 * time + 400055.2))
        return (P_prod)

    def get_P_waste(self,time):
        P_waste = np.where(time < 1950, 0,
                           0.000438727092 * time ** 3 - 2.52227209 * time ** 2 + 4831.80835 * time - 3084191.67)
        return (P_waste)

    def get_f_disc(self,time):  # Would it not be better to say that "everything not incinerated or recycled is discarded"
        # this way f_disc + f_incin + f_rec sum 1
        f_disc = np.where(time < 1980, 1, -0.000000017315 * time ** 3 + 0.0000624932 * time ** 2 - 0.0553287 * time)
        return (f_disc)

    def get_f_incin(self,time):
        f_incin = np.where(time < 1980, 0,
                           0.000000010866 * time ** 3 - 0.000040095 * time ** 2 + 0.0367815 * time)  # before 1980=0; since 1980 use equation
        return (f_incin)

    def get_f_rec(self,time):
        f_rec = np.where(time < 1989, 0, 0.00712723 * time - 14.1653)  # before 1989=0; since 1989 use equation
        return (f_rec)

    #####place holders
    k_sMPsed = 0
    f_pelagic = 0