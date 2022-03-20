import numpy as np
import matplotlib.pyplot as plt
from boxmodel_parameters import boxmodel_parameters, boxmodel_forcings

forcings = boxmodel_forcings("base",2015)
startstop = np.array([1950,2015])
P_prod = forcings.get_P_prod(np.linspace(startstop[0],
                                         startstop[1],
                                         (startstop[1]-startstop[0])+1))
print(np.sum(P_prod))

print(np.linspace(startstop[0],
                                         startstop[1],
                                         (startstop[1]-startstop[0])+1))