import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


def fB(t, C):
    tau = 1
    return(-C/tau)

t_span = np.array([0,5])
times = np.linspace(t_span[0], t_span[1], 50)

C0 = np.array([1.0])

soln = solve_ivp(fB, t_span, C0, t_eval = times)
t=soln.t
C = soln.y[0]

t_exact = np.linspace(t_span[0], t_span[1],101)
C_exact = C0*np.exp(-t_exact/1.0)

plt.rc("font", size=16)
plt.figure(figsize=(8,6))
plt.plot(t_exact, C_exact, "-", label="exact")
plt.plot(t,C,"o", label="solve_ivp")
plt.xlabel("time")
plt.ylabel("C");
plt.legend()
plt.show()
