import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from boxmodel_parameters import boxmodel_parameters, boxmodel_forcings
from timeit import default_timer as timer

#uncomment the following if you want to plot the curves for "P_produced, P_waste, P_recycled and P_incinerated
# FRCS = boxmodel_forcings()
# #def
# t_span = np.array([1950,2050])
# my_times = np.linspace(t_span[0], t_span[1], 10001)
# my_prod = FRCS.get_P_prod(my_times)
# my_waste = FRCS.get_P_waste(my_times)
# my_f_disc = FRCS.get_f_disc(my_times)
# my_f_incin = FRCS.get_f_incin(my_times)
# my_f_rec = FRCS.get_f_rec(my_times)
# my_f_disc_2 = np.ones(len(my_times))-my_f_incin - my_f_rec
# my_control_1 =  my_f_disc + my_f_rec + my_f_incin #do these 3 sum 1?
# my_control_2 = my_f_disc_2 + my_f_rec + my_f_incin #here they should sum 1 by definition
# plt.plot(my_times,my_prod, "-", label="prod")
# plt.plot(my_times,my_waste, "-", label="waste")
# plt.legend()
# plt.show()

# plt.plot(my_times,my_f_disc, "-", label="f_disc")
# plt.plot(my_times,my_f_disc_2, "-", label="f_disc_2")
# plt.plot(my_times,my_f_incin, "-", label="f_incin")
# plt.plot(my_times,my_f_rec, "-", label="f_rec")
# plt.plot(my_times,my_control_1, "-.", label="control1")
# plt.plot(my_times,my_control_2, "-.", label="control2")
# plt.legend()
# plt.show()


def boxmodel_V1(t, y, PARS, FRCS):
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
    sMP_beach = y[13]
    MP_sed = y[14]
    sMP_sed = y[15]

    P_prod = FRCS.get_P_prod(t)
    P_waste = FRCS.get_P_waste(t)
    f_rec = FRCS.get_f_rec(t)
    f_inc = FRCS.get_f_incin(t)
    f_disc = FRCS.get_f_disc(t)
    #f_disc = 1 - f_rec - f_inc # maybe simply define discarded = 1 - recycled - incinerated?

    #dP_use_dt = P_prod - f_inc * P_waste - f_disc * P_waste + f_rec * P_waste #I commented f_rec * P_waste, because I think recycled waste gets first removed from the used pool (because it becomes "waste"), then added again...so + recycled - recycled = 0 
    dP_use_dt = P_prod - P_waste + f_rec*P_waste #AK 16.03.2022 maybe this is more logical?
    dP_disc_dt = f_disc * P_waste*(1 - PARS.f_MP) - PARS.k_P_Disc_to_river * P_disc - PARS.k_Disc_P_to_MP * P_disc
    dMP_disc_dt = f_disc * P_waste*PARS.f_MP + PARS.k_Disc_P_to_MP * P_disc - PARS.k_MP_Disc_to_river * MP_disc - PARS.k_Disc_MP_to_sMP * MP_disc
    dsMP_disc_dt = PARS.k_Disc_MP_to_sMP * MP_disc - PARS.k_sMP_Disc_to_river * sMP_disc - PARS.k_Disc_sMP_to_atm * sMP_disc
    
    dP_SurfOce_dt = PARS.k_P_Disc_to_river * P_disc - PARS.k_SurfOce_P_beach * P_SurfOce - PARS.k_SurfOce_P_to_MP * P_SurfOce - PARS.k_P_surf_to_deep_oce *P_SurfOce#the last term is effectively 0 if all "large plastics" floats 
    dMP_SurfOce_dt = PARS.k_MP_Disc_to_river * MP_disc + PARS.k_SurfOce_P_to_MP * P_SurfOce - PARS.k_SurfOce_MP_to_sMP * MP_SurfOce - PARS.k_SurfOce_MP_beach * MP_SurfOce - PARS.k_SurfOce_MP_CoastSed * MP_SurfOce * PARS.f_shelf - PARS.k_MP_surf_to_deep_oce * MP_SurfOce * PARS.f_pelagic
    dsMP_SurfOce_dt = PARS.k_sMP_Disc_to_river * sMP_disc + PARS.k_SurfOce_MP_to_sMP * MP_SurfOce + PARS.k_sMP_atm_to_oce * sMP_atm + PARS.k_sMP_soil_to_oce * sMP_soil - PARS.k_sMP_oce_to_atm * sMP_SurfOce - PARS.k_SurfOce_sMP_CoastSed * sMP_SurfOce * PARS.f_shelf - PARS.k_sMP_surf_to_deep_oce * sMP_SurfOce * PARS.f_pelagic
    
    dMP_DeepOce_dt = +PARS.k_MP_surf_to_deep_oce * MP_SurfOce * PARS.f_pelagic - PARS.k_DeepOce_MP_to_sMP * MP_DeepOce
    dsMP_DeepOce_dt = PARS.k_sMP_surf_to_deep_oce * sMP_SurfOce * PARS.f_pelagic + PARS.k_DeepOce_MP_to_sMP * MP_DeepOce
    
    dsMP_atm_dt = PARS.k_Disc_sMP_to_atm * sMP_disc + PARS.k_sMP_oce_to_atm * sMP_SurfOce - PARS.k_sMP_atm_to_soil * sMP_atm - PARS.k_sMP_atm_to_oce * sMP_atm + PARS.k_sMP_soil_to_atm * sMP_soil
    dsMP_soil_dt = PARS.k_sMP_atm_to_soil * sMP_atm - PARS.k_sMP_soil_to_atm * sMP_soil - PARS.k_sMP_soil_to_oce * sMP_soil
    
    dP_beach_dt = PARS.k_SurfOce_P_beach * P_SurfOce - PARS.k_beach_P_to_MP * P_beach
    dMP_beach_dt = PARS.k_SurfOce_MP_beach * MP_SurfOce + PARS.k_beach_P_to_MP * P_beach - PARS.k_beach_MP_to_sMP * MP_beach
    dsMP_beach_dt = + PARS.k_beach_MP_to_sMP * MP_beach
    
    dMP_sed_dt = PARS.k_SurfOce_MP_CoastSed * MP_SurfOce * PARS.f_shelf
    dsMP_sed_dt = PARS.k_SurfOce_sMP_CoastSed * sMP_SurfOce * PARS.f_shelf

    return(np.array([dP_use_dt, dP_disc_dt, dMP_disc_dt, dsMP_disc_dt, 
                     dP_SurfOce_dt, dMP_SurfOce_dt, dsMP_SurfOce_dt, 
                     dMP_DeepOce_dt, dsMP_DeepOce_dt, 
                     dsMP_atm_dt, dsMP_soil_dt, 
                     dP_beach_dt, dMP_beach_dt, dsMP_beach_dt, 
                     dMP_sed_dt, dsMP_sed_dt]))


################################

initial_cond = np.zeros(16)#initial conditions all in 0
t_span = np.array([1950,2100])
eval_times = np.linspace(t_span[0], t_span[1], (t_span[1]-t_span[0]+1)*1000)#time where we want this to be evaluated (note that the ODE solver determines the correct time step for calculation automatically, this is just for output)




print(f"Starting to compute box model from {t_span[0]} to {t_span[1]}...")
start = timer()
PARS = boxmodel_parameters() # here all the k values and functions are stored
FRCS = boxmodel_forcings("fullstop", 2015)# here the forcing functions (produced, waste, etc)

soln = solve_ivp(fun=lambda t, y: boxmodel_V1(t, y, PARS, FRCS), 
                 t_span = t_span, y0 = initial_cond, t_eval = eval_times,
                 method = "RK45")#4th order Runge-Kutta for integration. This is default. 
end = timer()
print(f"Finished. This took: {end-start} seconds. Results saved in the variable \"soln\"")


##python differential equations before correction (from Jeroens original python script)

    # dP_use_dt = P_prod + f_rec * P_waste - f_inc * P_waste - f_disc * P_waste
    # dP_disc_dt = f_disc * P_waste*(1 - PARS.f_MP) - PARS.k_P_Disc_to_river * P_disc - PARS.k_Disc_P_to_MP * P_disc
    # dMP_disc_dt = f_disc * P_waste*PARS.f_MP + PARS.k_Disc_P_to_MP * P_disc - PARS.k_MP_Disc_to_river * MP_disc - PARS.k_Disc_MP_to_sMP * MP_disc
    # dsMP_disc_dt = PARS.k_Disc_MP_to_sMP * MP_disc - PARS.k_sMP_Disc_to_river * sMP_disc - PARS.k_Disc_sMP_to_atm * sMP_disc
    # dP_SurfOce_dt = PARS.k_P_Disc_to_river * P_disc - PARS.k_SurfOce_P_beach * P_SurfOce
    # dMP_SurfOce_dt = PARS.k_MP_Disc_to_river * MP_disc - PARS.k_SurfOce_MP_beach * MP_SurfOce - PARS.k_SurfOce_MP_CoastSed * MP_SurfOce * PARS.f_shelf - PARS.k_MP_surf_to_deep_oce * MP_SurfOce
    # dsMP_SurfOce_dt = PARS.k_sMP_Disc_to_river * sMP_disc + PARS.k_sMP_atm_to_oce * sMP_atm + PARS.k_sMP_soil_to_oce * sMP_soil - PARS.k_sMP_oce_to_atm * sMP_SurfOce - PARS.k_SurfOce_sMP_CoastSed * sMP_SurfOce * PARS.f_shelf - PARS.k_sMP_surf_to_deep_oce * sMP_SurfOce
    # dMP_DeepOce_dt = +PARS.k_MP_surf_to_deep_oce * MP_SurfOce * PARS.f_pelagic - PARS.k_DeepOce_MP_to_sMP * MP_DeepOce
    # dsMP_DeepOce_dt = PARS.k_sMP_surf_to_deep_oce * sMP_SurfOce * PARS.f_pelagic + PARS.k_DeepOce_MP_to_sMP * MP_DeepOce
    # dsMP_atm_dt = PARS.k_Disc_sMP_to_atm * sMP_disc + PARS.k_sMP_atm_to_oce * sMP_SurfOce - PARS.k_sMP_atm_to_soil * sMP_atm - PARS.k_sMP_atm_to_oce * sMP_atm
    # dsMP_soil_dt = PARS.k_sMP_atm_to_soil * sMP_atm - PARS.k_sMP_soil_to_atm * sMP_soil - PARS.k_sMP_soil_to_oce * sMP_soil
    # dP_beach_dt = PARS.k_SurfOce_P_beach * P_SurfOce
    # dMP_beach_dt = PARS.k_SurfOce_MP_beach * MP_SurfOce
    # dMP_sed_dt = PARS.k_SurfOce_MP_CoastSed * MP_SurfOce * PARS.f_shelf
    # dsMP_sed_dt = PARS.k_SurfOce_sMP_CoastSed * sMP_SurfOce * PARS.f_shelf