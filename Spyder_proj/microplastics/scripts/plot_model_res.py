import numpy as np
import matplotlib.pyplot as plt
from boxmodel_parameters import boxmodel_parameters, boxmodel_forcings

forcings = boxmodel_forcings("base",2015)
startstop = np.array([1950,2015])
P_prod = forcings.get_P_prod(np.linspace(startstop[0],
                                         startstop[1],
                                         (startstop[1]-startstop[0])+1))
print(f"All plastic produced between {startstop[0]} and {startstop[1]} (included): {np.sum(P_prod)}")


print("\nAll variables in the parameters:")
mypars = vars(boxmodel_parameters)
mykeys = mypars.keys()
for key in mykeys:
    print(f"{key}:  {mypars.get(key)}")


#print(vars(boxmodel_parameters).keys())

t = soln.t #this is computed with the other script, boxmodel_V1.py. 
#Run this first. Alternatively, copy this below "boxmodel_V1.py" and run it all.

P_prod_tot = soln.y[0]
P_waste_tot = soln.y[1]
P_rec_tot = soln.y[2]
P_inc_tot = soln.y[3]
P_disc_tot = soln.y[4]
MP_disc_tot = soln.y[5]

P_use = soln.y[6]
P_disc = soln.y[7]
MP_disc = soln.y[8]
sMP_disc = soln.y[9]

P_SurfOce = soln.y[10]
MP_SurfOce = soln.y[11]
sMP_SurfOce = soln.y[12]

MP_DeepOce = soln.y[13]
sMP_DeepOce = soln.y[14]

sMP_atm = soln.y[15]
sMP_soil = soln.y[16]

P_beach = soln.y[17]
MP_beach = soln.y[18]
sMP_beach = soln.y[19]

MP_sed = soln.y[20]
sMP_sed = soln.y[21]

print(f"Solver message: {soln.message}")
print(P_use[-1])
print(P_disc[-1])
print(MP_disc[-1])
print(sMP_disc[-1])
print("surfocean")
print(P_SurfOce[-1])
print(MP_SurfOce[-1])
print(sMP_SurfOce[-1])
print("deepocean")
print(MP_DeepOce[-1])
print(sMP_DeepOce[-1])
print("atm_and_soil")
print(sMP_atm[-1])
print(sMP_soil[-1])
print("beach")
print(P_beach[-1])
print(MP_beach[-1])
print("sediments")
print(MP_sed[-1])
print(sMP_sed[-1])

plt.plot(t, P_use, "-", label = "P use")
plt.plot(t, P_disc, "-", label = "P disc")
plt.plot(t, MP_disc, "-", label = "MP disc")
plt.plot(t, sMP_disc, "-", label = "sMP disc")
plt.plot(t, sMP_soil, "-", label = "sMP soil")
plt.legend()
plt.show()

plt.plot(t, P_SurfOce,"-", label = "P surface ocean")
plt.plot(t, MP_SurfOce,"-", label = "MP surface ocean")
plt.plot(t, sMP_SurfOce,"-", label = "sMP surface ocean")
plt.plot(t, MP_DeepOce,"-", label = "MP deep ocean")
plt.plot(t, sMP_DeepOce,"-", label = "sMP deep ocean")
plt.legend()
plt.show()

plt.plot(t, P_beach,"-", label = "P beach")
plt.plot(t, MP_beach,"-", label = "MP beach")
plt.plot(t, sMP_beach,"-", label = "sMP beach")
plt.yscale("log")
plt.legend()
plt.show()

plt.plot(t, sMP_atm, "-", label = "sMP_atm")
plt.plot(t, sMP_soil,"-", label = "sMP_soil")
#plt.yscale("log")
plt.legend()
plt.show()

plt.plot(t, sMP_DeepOce , "-", label = "sMP_DeepOce ")
plt.plot(t, MP_DeepOce , "-", label = "MP_DeepOce ")
#plt.yscale("log")
plt.legend()
plt.show()

control = sum(soln.y[6:21])
print(len(control))
print(f"\nAll plastics ever produced: {P_prod_tot[-1]}")
print(f"\nAll plastics ever incinerated: {P_inc_tot[-1]}")
print(f"\ncontrol at last year of computation: {control[-1]}")
print(f"\nControl + all plastics ever incinerated (this should sum to \"ever produced\"): {control[-1]+P_inc_tot[-1]}")

plt.plot(t,control, "-",label = "all compartments")
plt.axvline(x=2015,color="red")
plt.legend()
plt.show()