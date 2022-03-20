import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def fB(t, y):
    dydt = np.cos(np.pi*t**2) - y**2*np.sin(np.pi*t)
    return(dydt)

tstartstop = np.array([0,50])
times = np.linspace(tstartstop[0], tstartstop[1], 200)
Y0 = np.array([10])

soln1 = solve_ivp(fB, tstartstop, np.array([10]), t_eval = times)
soln2 = solve_ivp(fB, tstartstop, np.array([5]), t_eval = times)
soln3 = solve_ivp(fB, tstartstop, np.array([15]), t_eval = times)
t1 = soln1.t
y1 = soln1.y[0]
t2 = soln2.t
y2 = soln2.y[0]

t3 = soln3.t
y3 = soln3.y[0]

plt.rc("font",size=16)
plt.figure(figsize=(8,6))
plt.plot(t1,y1, "-", label="y0=10")
plt.plot(t2,y2, "-", label="y0=5")
plt.plot(t3,y3, "-", label="y0=15")
plt.xlabel("time")
plt.ylabel("y")
plt.legend()
plt.show()