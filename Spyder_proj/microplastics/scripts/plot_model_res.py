import matplotlib.pyplot as plt
from boxmodel_parameters import boxmodel_parameters, boxmodel_forcings

forcings = boxmodel_forcings("fullstop",2015)
startstop = np.array([1950,2025])
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

P_use = soln.y[0]
P_disc = soln.y[1]
MP_disc = soln.y[2]
sMP_disc = soln.y[3]

P_SurfOce = soln.y[4]
MP_SurfOce = soln.y[5]
sMP_SurfOce = soln.y[6]

MP_DeepOce = soln.y[7]
sMP_DeepOce = soln.y[8]

sMP_atm = soln.y[9]
sMP_soil = soln.y[10]

P_beach = soln.y[11]
MP_beach = soln.y[12]
sMP_beach = soln.y[13]

MP_sed = soln.y[14]
sMP_sed = soln.y[15]

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

control = sum(soln.y)
print(f"\ncontrol at last year of computation: {control[-1]}")

plt.plot(t,control, "-",label = "all compartments")
plt.axvline(x=2015,color="red")
plt.legend()
plt.show()