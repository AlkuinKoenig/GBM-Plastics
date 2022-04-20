import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from boxmodel_forcings import boxmodel_forcings
from timeit import default_timer as timer
from datetime import datetime
import json



###############################
#User input.
################################
extended_meta = True #Set this to True if you want the used parameters repeated as metadata in the output file (recommended). Set to False otherwise.
#The output file will be named automatically. 

input_fname = "PARS_BASE_V2_20220322_1739" #this is the input file with all the k-values for the model run. The name must be given without .json extension here. The .json file must be found in /input folder.
#scenario = ("fullstop",2025) #this is the scenario to run. Currently implemented: ("base") and ("fullstop", stopyear), with "stopyear" the year where all production and waste production is set to 0
scenario = ("pulse",0,1000) #a pulse at year "0" of 1000 tons of P


#examples:
#scenario = ("base") #business as usual
#scenario = ("fullstop",2025) #stop all virgin plastics production and all plastics waste on the 01.01.2025.
#scenario = ("pulse", 0, 1000) #waste and immediately discard a 1-year pulse of a total of 1000 tons of plastics (P and MP with the defined fractionation in waste) at year "0".

t_span = np.array([0,1000])#The model will be run from from t1 to t2 (given in years)
#eval_times = np.arange(t_span[0], t_span[1], 0.01)#defining timesteps (for output only)
eval_times = np.linspace(t_span[0],t_span[1],(t_span[1]-t_span[0])*10+1)#time where we want this to be evaluated (note that the ODE solver determines the correct time step for calculation automatically, this is just for output)


#ignore this for the moment
# name_to_index = {
#     "P_prod_tot": x,
#     "P_waste_tot": y,
#     "P_rec_tot": y,
#     "P_inc_tot": u,
#     "P_disc_tot": o,
#     "MP_disc_tot": y,
#     "P_use": z,
#     "P_disc": y,
#     "MP_disc": i,
#     "sMP_disc": u,
#     "P_SurfOce":    
#     }



###############################
#Defining the model
################################
def boxmodel_V1(t, y, PARS, FRCS):
    #this is for control
    P_prod_tot = y[0]
    P_waste_tot = y[1]
    P_rec_tot = y[2]
    P_inc_tot = y[3]
    P_disc_tot = y[4]
    MP_disc_tot = y[5]
    #these are the compartments we're actually looking at
    P_use = y[6]
    P_disc = y[7]
    MP_disc = y[8]
    sMP_disc = y[9]
    P_SurfOce = y[10]
    MP_SurfOce = y[11]
    sMP_SurfOce = y[12]
    MP_DeepOce = y[13]
    sMP_DeepOce = y[14]
    sMP_atm = y[15]
    sMP_soil = y[16]
    P_beach =y[17]
    MP_beach = y[18]
    sMP_beach = y[19]
    P_ShelfSed = y[20]
    MP_ShelfSed = y[21]
    sMP_ShelfSed = y[22]
    MP_DeepSed = y[23]
    sMP_DeepSed = y[24]
    
    #ADDING FLUXES
    #you have to add the fluxes as compartments here. 
    
    
    # F_SurfOce_P_to_beach = 
    # F_SurfOce_P_to_shelf = 
    # F_SurfOce_P_to_DeepOce = 
    # F_SurfOce_P_to_MP = 
    
    # F_SurfOce_MP_to_beach
    # F_SurfOce_MP_to_shelf
    # F_SurfOce_MP_to_deep
    # F_SurfOce_MP_to_sMP
    
    # F_SurfOce_sMP_to_beach = 
    # F_SurfOce_sMP_to_shelf
    # F_SurfOce_sMP_to_deep
    # F_SurfOce_sMP_to_atm
    
    # F_DeepOce_MP_to_DeepSed
    # F_DeepOce_MP_to_sMP
    
    # F_DeepOce_sMP_to_DeepSed
    
    # F_sMP_atm_to_soil =
    # F_sMP_atm_to_oce = 
    
    # F_sMP_soil_to_atm
    # F_sMP_soil_to_SurfOce
    
    # F_beach_P_to_MP
    # F_beach_MP_to_sMP
    
    
    
    
    
    #F_atm_to_soil = y[25]
    
    
    
    
    #now starting to calculate. First we get the forcings (P produced, P wasted, recycled fraction, incinerated fraction)
    P_prod = FRCS.get_P_prod(t)
    P_waste = FRCS.get_P_waste(t)
    f_rec = FRCS.get_f_rec(t)
    f_inc = FRCS.get_f_incin(t)
    #f_disc = FRCS.get_f_disc(t) 
    f_disc = 1 - f_rec - f_inc # As P_recycled + P_incinerated + P_discarded = 1
    
    ####d dts
    dP_prod_tot_dt = P_prod
    dP_waste_tot_dt = P_waste
    dP_rec_tot_dt = f_rec * P_waste
    dP_inc_tot_dt = f_inc * P_waste
    dP_disc_tot_dt = f_disc * P_waste * (1 - PARS["f_MP"])
    dMP_disc_tot_dt = f_disc * P_waste * PARS["f_MP"]

    #dP_use_dt = P_prod - f_inc * P_waste - f_disc * P_waste + f_rec * P_waste #I commented f_rec * P_waste, because I think recycled waste gets first removed from the used pool (because it becomes "waste"), then added again...so + recycled - recycled = 0 
    dP_use_dt = P_prod - P_waste + f_rec*P_waste #AK 16.03.2022 maybe this is more logical?
    dP_disc_dt = f_disc * P_waste * (1 - PARS["f_MP"]) - PARS["k_P_Disc_to_river"] * P_disc - PARS["k_Disc_P_to_MP"] * P_disc
    dMP_disc_dt = f_disc * P_waste * PARS["f_MP"] + PARS["k_Disc_P_to_MP"] * P_disc - PARS["k_MP_Disc_to_river"] * MP_disc - PARS["k_Disc_MP_to_sMP"] * MP_disc
    dsMP_disc_dt = PARS["k_Disc_MP_to_sMP"] * MP_disc - PARS["k_sMP_Disc_to_river"] * sMP_disc - PARS["k_Disc_sMP_to_atm"] * sMP_disc
    
    dP_SurfOce_dt = PARS["k_P_Disc_to_river"] * P_disc - PARS["k_SurfOce_P_beach"] * P_SurfOce - PARS["k_SurfOce_P_to_MP"] * P_SurfOce - PARS["k_SurfOce_P_ShelfSed"] * P_SurfOce * PARS["f_shelf"] - PARS["k_P_surf_to_deep_oce"] * P_SurfOce#the last term is effectively 0 if all "large plastics" floats 
    dMP_SurfOce_dt = PARS["k_MP_Disc_to_river"] * MP_disc + PARS["k_SurfOce_P_to_MP"] * P_SurfOce - PARS["k_SurfOce_MP_to_sMP"] * MP_SurfOce - PARS["k_SurfOce_MP_beach"] * MP_SurfOce - PARS["k_SurfOce_MP_ShelfSed"] * MP_SurfOce * PARS["f_shelf"] - PARS["k_MP_surf_to_deep_oce"] * MP_SurfOce * PARS["f_ocean"]
    dsMP_SurfOce_dt = PARS["k_sMP_Disc_to_river"] * sMP_disc + PARS["k_SurfOce_MP_to_sMP"] * MP_SurfOce + PARS["k_sMP_atm_to_oce"] * sMP_atm + PARS["k_sMP_soil_to_oce"] * sMP_soil - PARS["k_sMP_oce_to_atm"] * sMP_SurfOce - PARS["k_SurfOce_sMP_ShelfSed"] * sMP_SurfOce * PARS["f_shelf"] - PARS["k_sMP_surf_to_deep_oce"] * sMP_SurfOce * PARS["f_ocean"]
    
    dMP_DeepOce_dt = PARS["k_MP_surf_to_deep_oce"] * MP_SurfOce * PARS["f_ocean"] - PARS["k_DeepOce_MP_to_sMP"] * MP_DeepOce - PARS["k_DeepOce_MP_DeepSed"] * MP_DeepOce
    dsMP_DeepOce_dt = PARS["k_sMP_surf_to_deep_oce"] * sMP_SurfOce * PARS["f_ocean"] + PARS["k_DeepOce_MP_to_sMP"] * MP_DeepOce - PARS["k_DeepOce_sMP_DeepSed"] * sMP_DeepOce
    
    dsMP_atm_dt = PARS["k_Disc_sMP_to_atm"] * sMP_disc + PARS["k_sMP_oce_to_atm"] * sMP_SurfOce - PARS["k_sMP_atm_to_soil"] * sMP_atm - PARS["k_sMP_atm_to_oce"] * sMP_atm + PARS["k_sMP_soil_to_atm"] * sMP_soil
    dsMP_soil_dt = PARS["k_sMP_atm_to_soil"] * sMP_atm - PARS["k_sMP_soil_to_atm"] * sMP_soil - PARS["k_sMP_soil_to_oce"] * sMP_soil
    
    dP_beach_dt = PARS["k_SurfOce_P_beach"] * P_SurfOce - PARS["k_beach_P_to_MP"] * P_beach
    dMP_beach_dt = PARS["k_SurfOce_MP_beach"] * MP_SurfOce + PARS["k_beach_P_to_MP"] * P_beach - PARS["k_beach_MP_to_sMP"] * MP_beach
    dsMP_beach_dt = + PARS["k_beach_MP_to_sMP"] * MP_beach
    
    dP_ShelfSed_dt = PARS["k_SurfOce_P_ShelfSed"] * P_SurfOce * PARS["f_shelf"]
    dMP_ShelfSed_dt = PARS["k_SurfOce_MP_ShelfSed"] * MP_SurfOce * PARS["f_shelf"]
    dsMP_ShelfSed_dt = PARS["k_SurfOce_sMP_ShelfSed"] * sMP_SurfOce * PARS["f_shelf"]
    dMP_DeepSed_dt = PARS["k_DeepOce_MP_DeepSed"] * MP_DeepOce
    dsMP_DeepSed_dt = PARS["k_DeepOce_sMP_DeepSed"] * sMP_DeepOce


    ##ADDING FLUXES
    ###You also have to define the Flux for each timestep
    #dF_atm_to_soil_dt = PARS["k_sMP_atm_to_soil"] * sMP_atm  #im doing gross flux from atmo to soil here, not net
    
    

    return(np.array([dP_prod_tot_dt, dP_waste_tot_dt, 
                     dP_rec_tot_dt, dP_inc_tot_dt,
                     dP_disc_tot_dt, dMP_disc_tot_dt,
                     dP_use_dt, dP_disc_dt, dMP_disc_dt, dsMP_disc_dt, 
                     dP_SurfOce_dt, dMP_SurfOce_dt, dsMP_SurfOce_dt, 
                     dMP_DeepOce_dt, dsMP_DeepOce_dt, 
                     dsMP_atm_dt, dsMP_soil_dt, 
                     dP_beach_dt, dMP_beach_dt, dsMP_beach_dt, 
                     dP_ShelfSed_dt, dMP_ShelfSed_dt, dsMP_ShelfSed_dt,
                     dMP_DeepSed_dt, dsMP_DeepSed_dt,
                     #####ADDING FLUXES
                     #####You also have to make the function return the d/dt, otherwise it wont work.
                    # dF_atm_to_soil_dt
                     ]))


###############################
#running the model
################################
with open("../../../input/" + input_fname + ".json","r") as myfile:
    PARS = json.load(myfile) #loading the input file

FRCS = boxmodel_forcings(scenario)# here the forcing functions (produced, waste, etc). Note that this class was imported from "boxmodel_forcings.py", which must be in the same folder.


#initial_cond = np.zeros(25)#initial conditions all in 0
####ADDING FLUXES
###don't forget to add these "new compartments" in the initial conditions. They should start in 0.
initial_cond = np.zeros(25)#initial conditions all in 0


print(f"Starting to compute box model from {t_span[0]} to {t_span[1]}...")
start = timer()

soln = solve_ivp(fun=lambda t, y: boxmodel_V1(t, y, PARS, FRCS), 
                 t_span = t_span, y0 = initial_cond, t_eval = eval_times,
                 method = "RK45")#4th order Runge-Kutta for integration. This is default, but we specify it explicitely for clarity 
end = timer()
print(f"Finished. This took: {end-start} seconds. Results saved in the variable \"soln\"")


###############################
#Writing model output
################################
data_out = {      
    "Year" : soln.t,
    "P_prod_tot" : soln.y[0],
    "P_waste_tot" : soln.y[1],
    "P_rec_tot" : soln.y[2],
    "P_inc_tot" : soln.y[3],
    "P_disc_tot" : soln.y[4],
    "MP_disc_tot" : soln.y[5],
    
    "P_use" : soln.y[6],
    "P_disc" : soln.y[7],
    "MP_disc" : soln.y[8],
    "sMP_disc" : soln.y[9],
    
    "P_SurfOce" : soln.y[10],
    "MP_SurfOce" : soln.y[11],
    "sMP_SurfOce" : soln.y[12],
    
    "MP_DeepOce" : soln.y[13],
    "sMP_DeepOce" : soln.y[14],
    
    "sMP_atm" : soln.y[15],
    "sMP_soil" : soln.y[16],
    
    "P_beach" : soln.y[17],
    "MP_beach" : soln.y[18],
    "sMP_beach" : soln.y[19],
    
    "P_ShelfSed" : soln.y[20],
    "MP_ShelfSed" : soln.y[21],
    "sMP_ShelfSed" : soln.y[22],
    "MP_DeepSed" : soln.y[23],
    "sMP_DeepSed" : soln.y[24],
    
    ###ADDING FLUXES
    ###finally, you have to add them to the output with an adequate name and with the right index.
    #"F_atm_to_soil" : soln.y[25]
    
}
df = pd.DataFrame(data_out)

#creating a timestamp so that we can keep track of the outputs
now = datetime.now()
current_time = now.strftime("%Y%m%d_%H%M")
print("Current Time =", current_time)

outdir = "../../../output/"
fname = f"OUTP_{current_time}_INP_{input_fname}.csv"

print(f"\nWriting output to file...{outdir + fname}")

#writing the output as .csv
with open(outdir + fname, 'w', newline = "") as fout:
    if (extended_meta):
        fout.write(f"Timespan, {t_span[0]}-{t_span[1]}\n")
        fout.write(f"Scenario, {';'.join(map(str, scenario))}\n")
        fout.write("Used parameters below\n")
        for key, value in PARS.items():
            fout.write(f"{key}, {value}\n")
        fout.write("###############\n")
        fout.write("Data below\n")
    df.to_csv(fout)

print("\nDone.")
