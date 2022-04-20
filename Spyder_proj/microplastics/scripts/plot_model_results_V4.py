import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#################

fpath = "../../../output/"
#insert the output file name here
fname = "OUTP_20220420_1157_INP_PARS_BASE_V2_20220322_1739.csv"

#################

df_metadata = pd.read_csv(fpath + fname, header = None, error_bad_lines = False, warn_bad_lines=False)
mout = pd.read_csv(fpath + fname, skiprows = len(df_metadata.index))#skip all metadata lines

print(f"Available data columns: {mout.columns}")

mout["control"]  = mout[["P_use","P_disc","MP_disc",
               "sMP_disc","P_SurfOce","MP_SurfOce","sMP_SurfOce",
               "MP_DeepOce","sMP_DeepOce","sMP_atm","sMP_soil","P_beach",
               "MP_beach","sMP_beach","P_ShelfSed","MP_ShelfSed", "sMP_ShelfSed",
               "MP_DeepSed","sMP_DeepSed", "P_cleanUp","MP_cleanUp","sMP_cleanUp"]].sum(axis=1)


#calculating the flux at year t by subtracting total flux at year (t-1) from total flux at year (t).
#here the method "shift" comes in handy.
# steps_per_year = 10 #in how many timesteps has a year been cut in the output data? This must be known.
# mout["F_atm_to_soil_flux"] = mout["F_atm_to_soil"] - mout["F_atm_to_soil"].shift(steps_per_year)


# #calculating the flux by multiplying compartment with k value.
# k_sMP_atm_to_soil = 319.4444444 # I took that from the header file
# mout["F_atm_to_soil_2"] = mout["sMP_atm"] * k_sMP_atm_to_soil 


# #linear scale
# plt.plot(mout["Year"],mout["F_atm_to_soil_2"], "-",label = "F_atm_to_soil_2 [sMP_plastics multiplied by k]")
# plt.plot(mout["Year"],mout["F_atm_to_soil_flux"], "-",label = "F_atm_to_soil_flux [flux treated as compartment]")
# #plt.axvline(x=2015,color="red")
# #plt.yscale("log")
# plt.xlabel("year")
# plt.ylabel("mass flux [tonnes/yr]")
# plt.legend()
# plt.show()

# #log scale
# plt.plot(mout["Year"],mout["F_atm_to_soil_2"], "-",label = "F_atm_to_soil_2 [sMP_plastics multiplied by k]")
# plt.plot(mout["Year"],mout["F_atm_to_soil_flux"], "-",label = "F_atm_to_soil_flux [flux treated as compartment]")
# #plt.axvline(x=2015,color="red")
# plt.yscale("log")
# plt.xlabel("year")
# plt.ylabel("mass flux [tonnes/yr]")
# plt.legend()
# plt.show()



plt.plot(mout["Year"], mout["P_use"], "-", label = "P use")
plt.plot(mout["Year"], mout["P_disc"], "-", label = "P disc")
plt.plot(mout["Year"], mout["MP_disc"], "-", label = "MP disc")
plt.plot(mout["Year"], mout["sMP_disc"], "-", label = "sMP disc")
plt.plot(mout["Year"], mout["sMP_soil"], "-", label = "sMP soil")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.legend()
plt.show()



plt.plot(mout["Year"], mout["P_SurfOce"],"-", label = "P surface ocean")
plt.plot(mout["Year"], mout["MP_SurfOce"],"-", label = "MP surface ocean")
plt.plot(mout["Year"], mout["sMP_SurfOce"],"-", label = "sMP surface ocean")
plt.plot(mout["Year"], mout["MP_DeepOce"],"-", label = "MP deep ocean")
plt.plot(mout["Year"], mout["sMP_DeepOce"],"-", label = "sMP deep ocean")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.legend()
plt.show()


plt.plot(mout["Year"], mout["P_beach"],"-", label = "P beach")
plt.plot(mout["Year"], mout["MP_beach"],"-", label = "MP beach")
plt.plot(mout["Year"], mout["sMP_beach"],"-", label = "sMP beach")
plt.yscale("log")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.legend()
plt.show()


plt.plot(mout["Year"], mout["sMP_atm"], "-", label = "sMP_atm")
plt.plot(mout["Year"], mout["sMP_soil"],"-", label = "sMP_soil")
#plt.yscale("log")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.legend()
plt.show()


plt.plot(mout["Year"], mout["sMP_DeepOce"] , "-", label = "sMP_DeepOce ")
plt.plot(mout["Year"], mout["MP_DeepOce"] , "-", label = "MP_DeepOce ")
#plt.yscale("log")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.legend()
plt.show()

# plt.plot(mout["Year"], mout["F_atm_to_soil"] , "-", label = "total F_atm_to_soil")
# #plt.plot(mout["Year"], mout["MP_DeepOce"] , "-", label = "MP_DeepOce ")
# #plt.yscale("log")
# plt.xlabel("year")
# plt.ylabel("mass [tonnes]")
# plt.legend()
# plt.show()



plt.plot(mout["Year"],mout["control"], "-",label = "all compartments")
#plt.axvline(x=2015,color="red")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.legend()
plt.show()




print("\nup to this point:\n")
print(f"All plastics ever produced: {np.array(mout['P_prod_tot'])[-1]}")
print(f"\nAll plastics ever incinerated: {np.array(mout['P_inc_tot'])[-1]}")
print(f"\ncontrol at last year of computation: {np.array(mout['control'])[-1]}")
print(f"\nControl + all plastics ever incinerated (this should sum to \"ever produced\"): {np.array(mout['control'])[-1]+np.array(mout['P_inc_tot'])[-1]}")

