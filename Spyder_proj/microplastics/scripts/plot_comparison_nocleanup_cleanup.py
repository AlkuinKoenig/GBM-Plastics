import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#import plotnine

#Example script on plotting a cleanup scenario vs. a non-cleanup scenario

#################

#below give the relative path to the output files
fpath = "../../../output/"
#insert the output file name here. Vaiable names should be self-explanatory
fname_nocleanup = "OUTP_20220420_1703_INP_PARS_BASE_V2_20220322_1739_no_CU.csv"
fname_cleanup = "OUTP_20220420_1658_INP_PARS_BASE_V2_20220322_1739_CU_static.csv"


#################
#importing data, skipping the metadata lines
df_metadata = pd.read_csv(fpath + fname_nocleanup, header = None, error_bad_lines = False, warn_bad_lines=False)
mout_noCU = pd.read_csv(fpath + fname_nocleanup, skiprows = len(df_metadata.index))#skip all metadata lines

df_metadata = pd.read_csv(fpath + fname_nocleanup, header = None, error_bad_lines = False, warn_bad_lines=False)
mout_CU = pd.read_csv(fpath + fname_cleanup, skiprows = len(df_metadata.index))#skip all metadata lines
###

print(f"Available data columns: {mout_noCU.columns}")


plt.plot(mout_noCU["Year"], mout_noCU["P_use"], "-", label = "P use")
plt.plot(mout_noCU["Year"], mout_noCU["P_disc"], "-", label = "P disc")
plt.plot(mout_noCU["Year"], mout_noCU["MP_disc"], "-", label = "MP disc")
plt.plot(mout_noCU["Year"], mout_noCU["sMP_disc"], "-", label = "sMP disc")
plt.plot(mout_noCU["Year"], mout_noCU["sMP_soil"], "-", label = "sMP soil")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.title("no cleanup")
plt.legend(loc=(1.04,0))
plt.show()

plt.plot(mout_CU["Year"], mout_CU["P_use"], "-", label = "P use")
plt.plot(mout_CU["Year"], mout_CU["P_disc"], "-", label = "P disc")
plt.plot(mout_CU["Year"], mout_CU["MP_disc"], "-", label = "MP disc")
plt.plot(mout_CU["Year"], mout_CU["sMP_disc"], "-", label = "sMP disc")
plt.plot(mout_CU["Year"], mout_CU["sMP_soil"], "-", label = "sMP soil")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.title("cleanup")
plt.legend(loc=(1.04,0))
plt.show()



plt.plot(mout_noCU["Year"], mout_noCU["MP_DeepOce"], "-", label = "MP_DeepOce (no cleanup)")
plt.plot(mout_CU["Year"], mout_CU["MP_DeepOce"], "-", label = "MP_DeepOce (cleanup)")
plt.axvline(x=2015,color="red", linestyle = "dashed")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.legend()
plt.show()


plt.plot(mout_noCU["Year"], mout_noCU["sMP_soil"], "-", label = "sMP_soil (no cleanup)")
plt.plot(mout_CU["Year"], mout_CU["sMP_soil"], "-", label = "sMP_soil (cleanup)")
plt.axvline(x=2015,color="red", linestyle = "dashed")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.legend()
plt.show()

plt.plot(mout_noCU["Year"], mout_noCU["sMP_beach"], "-", label = "sMP_beach (no cleanup)")
plt.plot(mout_CU["Year"], mout_CU["sMP_beach"], "-", label = "sMP_beach (cleanup)")
plt.axvline(x=2015,color="red", linestyle = "dashed")
plt.xlabel("year")
plt.ylabel("mass [tonnes]")
plt.legend()
plt.show()


