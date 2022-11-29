import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

####Description
#This is an example script on plotting boxmodel output.
#################

#below insert the relative path to the output file
#fpath = "../../../output/"
fpath = "./"
#below give the ouput file name (including the ".csv")
fname = "OUTP_20221127_1447_INP_PARS_BASE_V2_20221127_1439.csv"

#################
#reading file in, skipping metadata
df_metadata = pd.read_csv(fpath + fname, header = None, error_bad_lines = False, warn_bad_lines=False)
mout = pd.read_csv(fpath + fname, skiprows = len(df_metadata.index))#skip all metadata lines

print(f"Available data columns: {mout.columns}")

mout["control"]  = mout[["P_use","P_disc","MP_disc",
               "sMP_disc","P_SurfOce","MP_SurfOce","sMP_SurfOce",
               "MP_DeepOce","sMP_DeepOce","sMP_atm","sMP_soil","P_beach",
               "MP_beach","sMP_beach","P_ShelfSed","MP_ShelfSed", "sMP_ShelfSed",
               "MP_DeepSed","sMP_DeepSed", "P_cleanUp","MP_cleanUp","sMP_cleanUp"]].sum(axis=1)


plt.plot(mout["Year"], mout["P_disc"], "-", label = "P disc")
plt.plot(mout["Year"], mout["MP_disc"], "-", label = "LMP disc")
plt.plot(mout["Year"], mout["sMP_disc"], "-", label = "SMP disc")
plt.plot(mout["Year"], mout["sMP_soil"], "-", label = "SMP remote land")
plt.xlabel("year")
plt.ylabel("mass [Tg]")
plt.legend()
plt.show()



plt.plot(mout["Year"], mout["P_SurfOce"],"-", label = "P surface ocean")
plt.plot(mout["Year"], mout["MP_SurfOce"],"-", label = "LMP surface ocean")
plt.plot(mout["Year"], mout["sMP_SurfOce"],"-", label = "SMP surface ocean")
plt.plot(mout["Year"], mout["MP_DeepOce"],"-", label = "LMP deep ocean")
plt.plot(mout["Year"], mout["sMP_DeepOce"],"-", label = "SMP deep ocean")
plt.xlabel("year")
plt.ylabel("mass [Tg]")
plt.legend()
plt.show()


plt.plot(mout["Year"], mout["P_beach"],"-", label = "P beach")
plt.plot(mout["Year"], mout["MP_beach"],"-", label = "LMP beach")
plt.plot(mout["Year"], mout["sMP_beach"],"-", label = "SMP beach")
#plt.yscale("log")
plt.xlabel("year")
plt.ylabel("mass [Tg]")
plt.legend()
plt.show()


plt.plot(mout["Year"], mout["sMP_atm"], "-", label = "SMP_atm")
plt.plot(mout["Year"], mout["sMP_soil"],"-", label = "SMP_remote land")
#plt.yscale("log")
plt.xlabel("year")
plt.ylabel("mass [Tg]")
plt.legend()
plt.show()


plt.plot(mout["Year"], mout["sMP_DeepOce"] , "-", label = "SMP_DeepOce ")
plt.plot(mout["Year"], mout["MP_DeepOce"] , "-", label = "LMP_DeepOce ")
#plt.yscale("log")
plt.xlabel("year")
plt.ylabel("mass [Tg]")
plt.legend()
plt.show()


plt.plot(mout["Year"],mout["control"], "-",label = "all compartments")
#plt.axvline(x=2015,color="red")
plt.xlabel("year")
plt.ylabel("mass [Tg]")
plt.legend()
plt.show()



print("\nup to this point:\n")
print(f"All plastics ever produced: {np.array(mout['P_prod_tot'])[-1]}")
print(f"\nAll plastics ever incinerated: {np.array(mout['P_inc_tot'])[-1]}")
print(f"\ncontrol at last year of computation: {np.array(mout['control'])[-1]}")
print(f"\nControl + all plastics ever incinerated (this should sum to \"ever produced\"): {np.array(mout['control'])[-1]+np.array(mout['P_inc_tot'])[-1]}")

