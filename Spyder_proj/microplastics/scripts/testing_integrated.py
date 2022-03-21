import numpy as np

def prod_int(time):
    return(0.1045809*1/3*time**3 - 409.084300*1/2*time**2 + 400055.2*time)

print(prod_int(2016)-prod_int(1950))