import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from boxmodel_forcings import boxmodel_forcings #this is custom. Make sure to have the script boxmodel_forcings.py in the same folder
from timeit import default_timer as timer
from datetime import datetime
import json

##############################
#Microplastics box model. 27 Nov 2022. Authors: Jeroen Sonke & Alkuin Koenig (jeroen.sonke@get.omp.eu and Alkuin.Koenig@gmx.de)
#NOTE that in the manuscript large microplastics and small micropalstics are termed LMP and SMP; in the model below they are still called MP and sMP
##############################
#Instructions:
#This is the main script (boxmodel.py).To be able to run this, you need to have in the same folder
#the script "boxmodel_forcings.py", where forcings are defined.
#you also need a *.json input file with mass transfer coefficients, k (for example created with the script "boxmodel_parameters.py")
#The variable "input_relpath" below should point to the location of this input *.json
#Note that the output file will be named automatically. It will be saved at the path "output_relpath" which should be given below.

###############################
#User input.
###############################
#below indicate the input file with all the k-values for the model run. The name must be given without .json extension here. 
input_fname = "PARS_BASE_V2_20221127_1439" 
#below indicate the relative path to the input file. 
input_relpath = "./"
#below indicate the relative path to where you want the output file to be saved
output_relpath = "./"

#below indicate the time span for which the model should be run (t1 to t2, given in years)
t_span = np.array([1950,2015])
#below indicate how many output lines you want to have per year (for example 10 --> output every 0.1 years)
lines_per_year = 10


#set below to True if you want the used parameters (rate constants) repeated as metadata in the output file (recommended). Set to False otherwise. 
extended_meta = True 

#below indicate the future plastics release scenario (see examples further below). 
scenario_release = ("base",) 

#below indicate the cleanup scenario (cleanup referrs to removing P, MP or sMP from the discarded plastics pool)
scenario_cleanup = ("no_cleanup",) 

########
#EXAMPLES FOR RELEASE AND CLEANUP SCENARIOS BELOW
########
#scenario_release = ("base",) #business as usual
#scenario_release = ("SCS",) #system change scenario from Lau et al., 2020
#scenario_release = ("fullstop",2025) #stop all virgin plastics production and all plastics waste on 01.01.2025; this scenario illustrates ecosystem recovery over hundreds to thousands of years
#scenario_release = ("pulse", 0, 1000) #waste and immediately discard a 1-year pulse of a total of 1000 tons of plastics (P and MP with the defined fractionation in waste) at year "0"; this scenario also illustrates the timescales of plastics propogation

#scenario_cleanup = ("no_cleanup",) #no cleanup (remediation) of reservoirs in the enar future. Default.
#scenario_cleanup = ("cleanup_discarded_fixedfrac", 2025, np.array([0.03,0.03,0.03]))#start cleaning up 3% of the discarded pool of P, 3% of MP and 3% of sMP every year
#scenario_cleanup = ("cleanup_discarded_linear_increment", np.array([2025,2050]), np.array([0.1,0.05,0.025]))#linerally ramping up cleanup from 2025 to 2050 to 10% of P, 5% of MP and 2.5% of sMP by 2050. Then maintain this ratio.
#######
#######



###############################
#Below the definition of the model, alongside all ordinary differential equations
###############################
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
    
    P_cleanUp = y[25]
    MP_cleanUp = y[26]
    sMP_cleanUp = y[27]
    
    
    #First we get the forcings (P produced, P wasted, recycled fraction, incinerated fraction)
    P_prod = FRCS.get_P_prod(t)
    P_waste = FRCS.get_P_waste(t)
    f_rec = FRCS.get_f_rec(t)
    f_inc = FRCS.get_f_incin(t)
    #f_disc = FRCS.get_f_disc(t) #note that we use f_disc = 1 - f_incin - f_rec below for convenience (and to sum up the three fraction to 1.00)
    f_disc = 1 - f_rec - f_inc # As P_recycled + P_incinerated + P_discarded = 1
   
    #getting the cleanup dts
    cleanup = FRCS.get_f_cleanUp(t)
    dP_cleanUp = cleanup[0] * P_disc
    dMP_cleanUp = cleanup[1] * MP_disc
    dsMP_cleanUp = cleanup[2] * sMP_disc
    
    ####d dts
    dP_prod_tot_dt = P_prod
    dP_waste_tot_dt = P_waste
    dP_rec_tot_dt = f_rec * P_waste
    dP_inc_tot_dt = f_inc * P_waste
    dP_disc_tot_dt = f_disc * P_waste * (1 - PARS["f_MP"])
    dMP_disc_tot_dt = f_disc * P_waste * PARS["f_MP"]

    dP_use_dt = P_prod - P_waste + f_rec*P_waste 
    
    dP_disc_dt = f_disc * P_waste * (1 - PARS["f_MP"]) - PARS["k_P_Disc_to_river"] * P_disc - PARS["k_Disc_P_to_MP"] * P_disc - dP_cleanUp
    dMP_disc_dt = f_disc * P_waste * PARS["f_MP"] + PARS["k_Disc_P_to_MP"] * P_disc - PARS["k_MP_Disc_to_river"] * MP_disc - PARS["k_Disc_MP_to_sMP"] * MP_disc - dMP_cleanUp
    dsMP_disc_dt = PARS["k_Disc_MP_to_sMP"] * MP_disc - PARS["k_sMP_Disc_to_river"] * sMP_disc - PARS["k_Disc_sMP_to_atm"] * sMP_disc - dsMP_cleanUp
    
    dP_SurfOce_dt = PARS["k_P_Disc_to_river"] * P_disc - PARS["k_SurfOce_P_beach"] * P_SurfOce - PARS["k_SurfOce_P_to_MP"] * P_SurfOce - PARS["k_SurfOce_P_ShelfSed"] * P_SurfOce * PARS["f_shelf"] - PARS["k_P_surf_to_deep_oce"] * P_SurfOce* PARS["f_ocean"]#the last term is effectively 0 if all "large plastics" floats 
    dMP_SurfOce_dt = PARS["k_MP_Disc_to_river"] * MP_disc + PARS["k_SurfOce_P_to_MP"] * P_SurfOce - PARS["k_SurfOce_MP_to_sMP"] * MP_SurfOce - PARS["k_SurfOce_MP_beach"] * MP_SurfOce - PARS["k_SurfOce_MP_ShelfSed"] * MP_SurfOce * PARS["f_shelf"] - PARS["k_MP_surf_to_deep_oce"] * MP_SurfOce * PARS["f_ocean"]
    dsMP_SurfOce_dt = PARS["k_sMP_Disc_to_river"] * sMP_disc + PARS["k_SurfOce_MP_to_sMP"] * MP_SurfOce + PARS["k_sMP_atm_to_oce"] * sMP_atm + PARS["k_sMP_soil_to_oce"] * sMP_soil - PARS["k_sMP_oce_to_atm"] * sMP_SurfOce - PARS["k_SurfOce_sMP_ShelfSed"] * sMP_SurfOce * PARS["f_shelf"] - PARS["k_sMP_surf_to_deep_oce"] * sMP_SurfOce * PARS["f_ocean"]
    
    dMP_DeepOce_dt = PARS["k_MP_surf_to_deep_oce"] * MP_SurfOce * PARS["f_ocean"] - PARS["k_DeepOce_MP_to_sMP"] * MP_DeepOce - PARS["k_DeepOce_MP_DeepSed"] * MP_DeepOce
    dsMP_DeepOce_dt = PARS["k_sMP_surf_to_deep_oce"] * sMP_SurfOce * PARS["f_ocean"] + PARS["k_DeepOce_MP_to_sMP"] * MP_DeepOce - PARS["k_DeepOce_sMP_DeepSed"] * sMP_DeepOce
    
    dsMP_atm_dt = PARS["k_Disc_sMP_to_atm"] * sMP_disc + PARS["k_sMP_oce_to_atm"] * sMP_SurfOce - PARS["k_sMP_atm_to_soil"] * sMP_atm - PARS["k_sMP_atm_to_oce"] * sMP_atm + PARS["k_sMP_soil_to_atm"] * sMP_soil
    dsMP_soil_dt = PARS["k_sMP_atm_to_soil"] * sMP_atm - PARS["k_sMP_soil_to_atm"] * sMP_soil - PARS["k_sMP_soil_to_oce"] * sMP_soil
    
    dP_beach_dt = PARS["k_SurfOce_P_beach"] * P_SurfOce - PARS["k_beach_P_to_MP"] * P_beach
    dMP_beach_dt = PARS["k_SurfOce_MP_beach"] * MP_SurfOce + PARS["k_beach_P_to_MP"] * P_beach - PARS["k_beach_MP_to_sMP"] * MP_beach
    dsMP_beach_dt = + PARS["k_beach_MP_to_sMP"] * MP_beach #SMP on beach is only produced by degradation of LMP on beach. No direct ocean to beach deposition of SMP is included in the model
    
    dP_ShelfSed_dt = PARS["k_SurfOce_P_ShelfSed"] * P_SurfOce * PARS["f_shelf"]
    dMP_ShelfSed_dt = PARS["k_SurfOce_MP_ShelfSed"] * MP_SurfOce * PARS["f_shelf"]
    dsMP_ShelfSed_dt = PARS["k_SurfOce_sMP_ShelfSed"] * sMP_SurfOce * PARS["f_shelf"]
    dMP_DeepSed_dt = PARS["k_DeepOce_MP_DeepSed"] * MP_DeepOce
    dsMP_DeepSed_dt = PARS["k_DeepOce_sMP_DeepSed"] * sMP_DeepOce


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
                     dP_cleanUp, dMP_cleanUp, dsMP_cleanUp
                     ]))


################################
#running the model
################################
with open(input_relpath + input_fname + ".json","r") as myfile:
    PARS = json.load(myfile) #loading the input file

FRCS = boxmodel_forcings(scenario_release, scenario_cleanup)# here the forcing functions (produced, waste, etc). Note that this class was imported from "boxmodel_forcings.py", which must be in the same folder.

eval_times = np.linspace(t_span[0],t_span[1],(t_span[1]-t_span[0])*lines_per_year+1)#time where we want this to be evaluated (note that the ODE solver determines the correct time step for calculation automatically, this is just for output)

initial_cond = np.zeros(28)#set all initial conditions to 0


print(f"Starting to compute box model from {t_span[0]} to {t_span[1]}...")
start = timer()

soln = solve_ivp(fun=lambda t, y: boxmodel_V1(t, y, PARS, FRCS), 
                 t_span = t_span, y0 = initial_cond, t_eval = eval_times,
                 method = "RK45")#4th order Runge-Kutta for integration. This is default, but we specify it explicitely for clarity 
end = timer()
print(f"Finished. This took: {end-start} seconds. Results saved in the variable \"soln\"")


###############################
#Writing model output
###############################
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
    
    "P_cleanUp" : soln.y[25],
    "MP_cleanUp" : soln.y[26],
    "sMP_cleanUp" : soln.y[27]
}
df = pd.DataFrame(data_out)

#now creating all the additional flux columns...
#...We do this outside the ODE solver, but the introduced error should be minimal
df["FLUXES_AFTER"] = df["P_disc"] * np.nan #empty separating column for convenience
df["F_P_produced"] = FRCS.get_P_prod(df["Year"])
df["F_P_waste"] = FRCS.get_P_waste(df["Year"])
df["F_P_disc"] = FRCS.get_P_waste(df["Year"]) * (1 - FRCS.get_f_incin(df["Year"]) - FRCS.get_f_rec(df["Year"]))
df["F_P_incin"] = FRCS.get_P_waste(df["Year"]) * FRCS.get_f_incin(df["Year"])
df["F_P_rec"] = FRCS.get_P_waste(df["Year"]) * FRCS.get_f_rec(df["Year"])

df["F_P_disc_to_SurfOce"] = df["P_disc"] * PARS["k_P_Disc_to_river"]
df["F_MP_disc_to_SurfOce"] = df["MP_disc"] * PARS["k_MP_Disc_to_river"]
df["F_sMP_disc_to_SurfOce"] = df["sMP_disc"] * PARS["k_sMP_Disc_to_river"]

df["F_P_SurfOce_to_beach"] = df["P_SurfOce"] * PARS["k_SurfOce_P_beach"]
df["F_P_SurfOce_to_ShelfSed"] = df["P_SurfOce"] * PARS["k_SurfOce_P_ShelfSed"] * PARS["f_shelf"]
df["F_P_SurfOce_to_DeepOce"] = df["P_SurfOce"] * PARS["k_P_surf_to_deep_oce"] * PARS["f_ocean"]
df["F_P_to_MP_SurfOce"] = df["P_SurfOce"] * PARS["k_SurfOce_P_to_MP"]

df["F_MP_SurfOce_to_beach"] = df["MP_SurfOce"] * PARS["k_SurfOce_MP_beach"]
df["F_MP_SurfOce_to_ShelfSed"] = df["MP_SurfOce"] * PARS["k_SurfOce_MP_ShelfSed"] * PARS["f_shelf"]
df["F_MP_SurfOce_to_DeepOce"] = df["MP_SurfOce"] * PARS["k_MP_surf_to_deep_oce"] * PARS["f_ocean"]
df["F_MP_to_sMP_SurfOce"] = df["MP_SurfOce"] * PARS["k_SurfOce_MP_to_sMP"]

df["F_sMP_SurfOce_to_beach"] = 0
df["F_sMP_SurfOce_to_ShelfSed"] = df["sMP_SurfOce"] * PARS["k_SurfOce_sMP_ShelfSed"] * PARS["f_shelf"]
df["F_sMP_SurfOce_to_DeepOce"] = df["sMP_SurfOce"] * PARS["k_sMP_surf_to_deep_oce"] * PARS["f_ocean"]
df["F_sMP_SurfOce_to_atm"] = df["sMP_SurfOce"] * PARS["k_sMP_oce_to_atm"]

df["F_MP_DeepOce_to_DeepSed"] = df["MP_DeepOce"] * PARS["k_DeepOce_MP_DeepSed"]
df["F_MP_to_sMP_DeepOce"] = df["MP_DeepOce"] * PARS["k_DeepOce_MP_to_sMP"]

df["F_sMP_DeepOce_to_DeepSed"] = df["sMP_DeepOce"] * PARS["k_DeepOce_sMP_DeepSed"]
df["F_sMP_atm_to_soil"] = df["sMP_atm"] * PARS["k_sMP_atm_to_soil"]
df["F_sMP_atm_to_oce"] = df["sMP_atm"] * PARS["k_sMP_atm_to_oce"]
df["F_sMP_soil_to_atm"] = df["sMP_soil"] * PARS["k_sMP_soil_to_atm"]
df["F_sMP_soil_to_oce"] = df["sMP_soil"] * PARS["k_sMP_soil_to_oce"]
df["F_P_to_MP_beach"] = df["P_beach"] * PARS["k_beach_P_to_MP"]
df["F_MP_to_sMP_beach"] = df["MP_beach"] * PARS["k_beach_MP_to_sMP"]

df["F_P_disc_to_cleanUp"] = df["P_disc"] * FRCS.get_f_cleanUp(df["Year"])[0]
df["F_MP_disc_to_cleanUp"] = df["MP_disc"] * FRCS.get_f_cleanUp(df["Year"])[1]
df["F_sMP_disc_to_cleanUp"] = df["sMP_disc"] * FRCS.get_f_cleanUp(df["Year"])[2]

df["DIVERSE_AFTER"] = df["P_disc"] * np.nan #empty separating column for convenience
df["f_rec"] = FRCS.get_f_rec(df["Year"])
df["f_incin"] =  FRCS.get_f_incin(df["Year"])
df["f_disc"] = 1 - FRCS.get_f_rec(df["Year"]) - FRCS.get_f_incin(df["Year"])
df["frac_P_cleanup"] = FRCS.get_f_cleanUp(df["Year"])[0]
df["frac_MP_cleanup"] = FRCS.get_f_cleanUp(df["Year"])[1]
df["frac_sMP_cleanup"] = FRCS.get_f_cleanUp(df["Year"])[2]

#creating a timestamp so that we can keep track of the outputs
now = datetime.now()
current_time = now.strftime("%Y%m%d_%H%M")
print("Current Time =", current_time)

#automatically created output file name
fname = f"OUTP_{current_time}_INP_{input_fname}.csv"

print(f"\nWriting output to file...{output_relpath + fname}")

#writing the output as .csv
with open(output_relpath + fname, 'w', newline = "") as fout:
    if (extended_meta):
        fout.write(f"Timespan, {t_span[0]}-{t_span[1]}\n")
        fout.write(f"scenario_release, {';'.join(map(str, scenario_release))}\n")
        fout.write(f"scenario_cleanup, {';'.join(map(str, scenario_cleanup))}\n")
        fout.write("Used parameters below\n")
        for key, value in PARS.items():
            fout.write(f"{key}, {value}\n")
        fout.write("###############\n")
        fout.write("Data below\n")
    df.to_csv(fout)

print("\nDone.")

