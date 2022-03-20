import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from K_values import parameters
from timeit import default_timer as timer

PARS = parameters()

#def
t_span = np.array([1950,2050])
my_times = np.linspace(t_span[0], t_span[1], 101)
my_prod = PARS.get_P_prod(my_times)
my_waste = PARS.get_P_waste(my_times)
my_f_disc = PARS.get_f_disc(my_times)
my_f_incin = PARS.get_f_incin(my_times)
my_f_rec = PARS.get_f_rec(my_times)
my_f_disc_2 = np.ones(len(my_times))-my_f_incin - my_f_rec
my_control_1 =  my_f_disc + my_f_rec + my_f_incin
my_control_2 = my_f_disc_2 + my_f_rec + my_f_incin
#myy = [get_P_prod(x) for x in myx]

#get_P_prod(2015)


plt.plot(my_times,my_prod, "-", label="prod")
plt.plot(my_times,my_waste, "-", label="waste")
plt.legend()
plt.show()

plt.plot(my_times,my_f_disc, "-", label="f_disc")
plt.plot(my_times,my_f_disc_2, "-", label="f_disc_2")
plt.plot(my_times,my_f_incin, "-", label="f_incin")
plt.plot(my_times,my_f_rec, "-", label="f_rec")
plt.plot(my_times,my_control_1, "-.", label="control1")
plt.plot(my_times,my_control_2, "-.", label="control2")
plt.legend()
plt.show()


def boxmodel(t,y, PARS):
    prod = PARS.get_P_prod(t)
    waste = PARS.get_P_waste(t)
    f_rec = PARS.get_f_rec(t)
    f_inc = PARS.get_f_incin(t)
    f_disc = 1 - f_rec - f_inc

    dUse_dt = prod+f_rec*waste-f_inc*waste-f_disc*waste
    return(np.array([dUse_dt]))

def boxmodel2(t,y, PARS):
    P_use = y[0]
    P_disc = y[1]
    MP_disc = y[2]
    sMP_disc = y[3]
    P_SurfOce = y[4]
    MP_SurfOce = y[5]
    sMP_SurfOce = y[6]
    MP_DeepOce = y[7]
    sMP_DeepOce = y[8]
    sMP_atm = y[9]
    sMP_soil = y[10]
    P_beach =y[11]
    MP_beach = y[12]
    MP_sed = y[13]
    sMP_sed = y[14]

    P_prod = PARS.get_P_prod(t)
    P_waste = PARS.get_P_waste(t)
    f_rec = PARS.get_f_rec(t)
    f_inc = PARS.get_f_incin(t)
    f_disc = 1 - f_rec - f_inc

    dP_use_dt = P_prod + f_rec * P_waste - f_inc * P_waste - f_disc * P_waste
    dP_disc_dt = f_disc * P_waste*(1 - PARS.f_MP) - PARS.k_P_Disc_to_river * P_disc - PARS.k_Disc_P_to_MP * P_disc
    dMP_disc_dt = f_disc * P_waste*PARS.f_MP + PARS.k_Disc_P_to_MP * P_disc - PARS.k_MP_Disc_to_river * MP_disc - PARS.k_Disc_MP_to_sMP * MP_disc
    dsMP_disc_dt = PARS.k_Disc_MP_to_sMP * MP_disc - PARS.k_sMP_Disc_to_river * sMP_disc - PARS.k_Disc_sMP_to_atm * sMP_disc
    dP_SurfOce_dt = PARS.k_P_Disc_to_river * P_disc - PARS.k_SurfOce_P_beach * P_SurfOce
    dMP_SurfOce_dt = PARS.k_MP_Disc_to_river * MP_disc - PARS.k_SurfOce_MP_beach * MP_SurfOce - PARS.k_SurfOce_MP_CoastSed * MP_SurfOce * PARS.f_shelf - PARS.k_MP_surf_to_deep_oce * MP_SurfOce
    dsMP_SurfOce_dt = PARS.k_sMP_Disc_to_river * sMP_disc + PARS.k_sMP_atm_to_oce * sMP_atm + PARS.k_sMP_soil_to_oce * sMP_soil - PARS.k_sMP_oce_to_atm * sMP_SurfOce - PARS.k_sMPsed * sMP_SurfOce * PARS.f_shelf - PARS.k_sMP_surf_to_deep_oce * sMP_SurfOce
    dMP_DeepOce_dt = -PARS.k_MP_surf_to_deep_oce * MP_SurfOce * PARS.f_pelagic - PARS.k_DeepOce_MP_to_sMP * MP_DeepOce
    dsMP_DeepOce_dt = PARS.k_sMP_surf_to_deep_oce * sMP_SurfOce * PARS.f_pelagic + PARS.k_DeepOce_MP_to_sMP * MP_DeepOce
    dsMP_atm_dt = PARS.k_Disc_sMP_to_atm * sMP_disc + PARS.k_sMP_atm_to_oce * sMP_SurfOce - PARS.k_sMP_atm_to_soil * sMP_atm - PARS.k_sMP_atm_to_oce * sMP_atm
    dsMP_soil_dt = PARS.k_sMP_atm_to_soil * sMP_atm - PARS.k_sMP_soil_to_atm * sMP_soil - PARS.k_sMP_soil_to_oce * sMP_soil
    dP_beach_dt = PARS.k_SurfOce_P_beach * P_SurfOce
    dMP_beach_dt = PARS.k_SurfOce_MP_beach * MP_SurfOce
    dMP_sed_dt = PARS.k_SurfOce_MP_CoastSed * MP_SurfOce * PARS.f_shelf
    dsMP_sed_dt = PARS.k_SurfOce_sMP_CoastSed * sMP_SurfOce * PARS.f_shelf

    return(np.array([dP_use_dt, dP_disc_dt, dMP_disc_dt, dsMP_disc_dt, dP_SurfOce_dt, dMP_SurfOce_dt, dsMP_SurfOce_dt, dMP_DeepOce_dt,
                     dsMP_DeepOce_dt, dsMP_atm_dt, dsMP_soil_dt, dP_beach_dt, dMP_beach_dt, dMP_sed_dt, dsMP_sed_dt]))


# soln = solve_ivp(fun=lambda t, y: boxmodel(t, y, PARS), t_span = t_span, y0 = use_0, t_eval=my_times)
# t=soln.t
# P_use =soln.y[0]

#print(use_0)
use_0 = np.zeros(15)
t_span = np.array([1950,2050])
my_times = np.linspace(t_span[0], t_span[1], 101)

print(f"Starting to compute box model from {t_span[0]} to {t_span[1]}...")
start = timer()
soln = solve_ivp(fun=lambda t, y: boxmodel2(t, y, PARS), t_span = t_span, y0 = use_0, t_eval=my_times)
end = timer()
print(end-start)

t = soln.t
P_use = soln.y[0]
P_disc = soln.y[1]
MP_disc = y[2]
    # sMP_disc = y[3]
    # P_SurfOce = y[4]
    # MP_SurfOce = y[5]
    # sMP_SurfOce = y[6]
    # MP_DeepOce = y[7]
    # sMP_DeepOce = y[8]
    # sMP_atm = y[9]
    # sMP_soil = y[10]
    # P_beach =y[11]
    # MP_beach = y[12]
    # MP_sed = y[13]
    # sMP_sed = y[14]


# plt.plot(t,P_use, "-", label="P_use")
# plt.legend()
# plt.show()
