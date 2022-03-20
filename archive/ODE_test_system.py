import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def fB(t, y):
    A = y[0]
    B = y[1]
    C = y[2]
    E = y[3]

    k=0.1

    dA_dt = -k*A*B
    dB_dt = -k*A*B
    dC_dt = k*A*B
    dE_dt = -dA_dt-dB_dt

    return(np.array([dA_dt, dB_dt, dC_dt, dE_dt]))

t_span = np.array([0,50])
times = np.linspace(t_span[0], t_span[1], 101)

y0 = np.array([2,1,0,0])

soln = solve_ivp(fB, t_span, y0, t_eval=times)
t=soln.t
A =soln.y[0]
B = soln.y[1]
C = soln.y[2]
E =soln.y[3]

plt.rc("font",size=14)
plt.figure(figsize=(10,5))
plt.plot(t,A,"-", label = "A")
plt.plot(t,B,"-", label="B")
plt.plot(t,C,"-", label="C")
plt.plot(t,E,"-.", label="E")
plt.xlabel("Time")
plt.ylabel("value")
plt.legend()
plt.show()

