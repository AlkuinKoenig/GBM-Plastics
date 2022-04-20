import numpy as np

#This is the forcing class for the microplastics boxmodel. Here forcing functions on produced, wasted, discarded, recycled plastics are saved ...
#... as well as a function describing cleanup scenarios
class boxmodel_forcings():
    
    def __init__(self, scenario_release = ("base"), scenario_cleanup = ("no_cleanup")):
        self.scenario_release = scenario_release
        if not self.scenario_release[0] in ["base","fullstop","pulse"]:
            raise Exception("Error. Undefined release scenario. Be sure to initiate your 'forcings' class with a valid release scenario! Typo?")
        
        self.scenario_cleanup = scenario_cleanup
        if not self.scenario_cleanup[0] in ["no_cleanup","cleanup_discarded_fixedfrac"]:
            raise Exception("Error. Undefined cleanup scenario. Be sure to initiate your 'forcings' class with a valid cleanup scenario! Typo?")
        
        
    
    def get_P_prod(self,time):        
        P_prod = np.where(time < 1950, 0, (0.1045809 * time ** 2 - 409.084300 * time + 400055.2))
        P_prod = P_prod * 8300/8007 # tweaking the function so that total produced form 1950 to 2015 (including) is 8300.
        if (self.scenario_release[0] == "fullstop"):
            P_prod = np.where(time >= self.scenario_release[1], 0, P_prod)
        
        if (self.scenario_release[0] == "pulse"):
            P_prod = np.where(np.floor(time) == self.scenario_release[1], self.scenario_release[2],0)
            
        return (P_prod)
    

    def get_P_waste(self,time):
        P_waste = np.where(time < 1950, 0,
                           0.000438727092 * time ** 3 - 2.52227209 * time ** 2 + 4831.80835 * time - 3084191.67)
        if (self.scenario_release[0] == "fullstop"):
            P_waste = np.where(time >= self.scenario_release[1], 0, P_waste)
            
        if (self.scenario_release[0] == "pulse"):
            P_waste = np.where(np.floor(time) == self.scenario_release[1], self.scenario_release[2],0)
        
        return (P_waste)
    

    
    def get_f_disc(self,time):  # Would it not be better to say that "everything not incinerated or recycled is discarded"
        # this way f_disc + f_incin + f_rec sum 1
        f_disc = np.where(time < 1980, 1, -0.000000017315 * time ** 3 + 0.0000624932 * time ** 2 - 0.0553287 * time)
        
        if (self.scenario_release[0] == "pulse"): 
            f_disc = 1 #in the pulse scenario_release, all waste P is discarded
            
        return (f_disc)
    
    

    def get_f_incin(self,time):
        f_incin = np.where(time < 1980, 0,
                           0.000000010866 * time ** 3 - 0.000040095 * time ** 2 + 0.0367815 * time)  # before 1980=0; since 1980 use equation
        
        if (self.scenario_release[0] == "pulse"):
            f_incin = 0 #in the pulse scenario_release, all waste P is discarded
        
        return (f_incin)

    def get_f_rec(self,time):
        f_rec = np.where(time < 1989, 0, 0.00712723 * time - 14.1653)  # before 1989=0; since 1989 use equation
        
        if (self.scenario_release[0] == "pulse"):
            r_rec = 0 #in the pulse scenario_release, all waste P is discarded
        
        return (f_rec)
    
    def get_f_cleanUp(self,time):
        f_P_cleanUp = 0
        f_MP_cleanUp = 0
        f_sMP_cleanUp = 0
        
        if (self.scenario_cleanup[0] == "cleanup_discarded_fixedfrac"):
            
            f_P_cleanUp = np.where(time >= self.scenario_cleanup[1], self.scenario_cleanup[2][0], 0)
            f_MP_cleanUp = np.where(time >= self.scenario_cleanup[1], self.scenario_cleanup[2][1], 0)
            f_sMP_cleanUp = np.where(time >= self.scenario_cleanup[1], self.scenario_cleanup[2][2], 0)
        
        return (np.array([f_P_cleanUp, f_MP_cleanUp, f_sMP_cleanUp]))
    
    
    

#FRCS = boxmodel_forcings(("base",),("no_cleanup",))

# print(FRCS.get_P_prod(2000))
# # print(FRCS.get_f_incin(1981))
# print(1 - FRCS.get_f_incin(1980) - FRCS.get_f_rec(1980) )
