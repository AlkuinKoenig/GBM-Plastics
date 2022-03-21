import numpy as np

#saving forcings (P use, P waste, etc) in a class as well
class boxmodel_forcings():
    
    def __init__(self, scenario = "base", stoptime = 999999):
        self.scenario = scenario
        self.stoptime = stoptime
        
    
    def get_P_prod(self,time):
        P_prod = np.where(time < 1950, 0, (0.1045809 * time ** 2 - 409.084300 * time + 400055.2))
        P_prod = P_prod * 8300/8007 # tweaking the function so that total produced form 1950 to 2015 (including) is 8300.
        if (self.scenario == "fullstop"):
            P_prod = np.where(time >= self.stoptime, 0, P_prod)
        
        return (P_prod)

    def get_P_waste(self,time):
        P_waste = np.where(time < 1950, 0,
                           0.000438727092 * time ** 3 - 2.52227209 * time ** 2 + 4831.80835 * time - 3084191.67)
        if (self.scenario == "fullstop"):
            P_waste = np.where(time >= self.stoptime, 0, P_waste)
        
        return (P_waste)

    def get_f_disc(self,time):  # Would it not be better to say that "everything not incinerated or recycled is discarded"
        # this way f_disc + f_incin + f_rec sum 1
        f_disc = np.where(time < 1980, 1, -0.000000017315 * time ** 3 + 0.0000624932 * time ** 2 - 0.0553287 * time)
        return (f_disc)

    def get_f_incin(self,time):
        f_incin = np.where(time < 1980, 0,
                           0.000000010866 * time ** 3 - 0.000040095 * time ** 2 + 0.0367815 * time)  # before 1980=0; since 1980 use equation
        return (f_incin)

    def get_f_rec(self,time):
        f_rec = np.where(time < 1989, 0, 0.00712723 * time - 14.1653)  # before 1989=0; since 1989 use equation
        return (f_rec)

