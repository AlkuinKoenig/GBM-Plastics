import numpy as np

#This is the forcing class for the microplastics boxmodel. Here forcing functions on produced, wasted, discarded, recycled plastics are saved ...
#... as well as a function describing cleanup scenarios
class boxmodel_forcings():
    
    def __init__(self, scenario_release = ("base"), scenario_cleanup = ("no_cleanup")):
        self.scenario_release = scenario_release
        if not self.scenario_release[0] in ["base","fullstop","pulse","SCS"]:
            raise Exception("Error. Undefined release scenario. Be sure to initiate your 'forcings' class with a valid release scenario! Typo?")
        
        self.scenario_cleanup = scenario_cleanup
        if not self.scenario_cleanup[0] in ["no_cleanup","cleanup_discarded_fixedfrac",
                                            "cleanup_discarded_linear_increment"]:
            raise Exception("Error. Undefined cleanup scenario. Be sure to initiate your 'forcings' class with a valid cleanup scenario! Typo?")
        
        
    
    def get_P_prod(self,time):        
        #base case
        P_prod = np.where(time < 1950, 0, (0.1045809 * time ** 2 - 409.084300 * time + 400055.2))
       # P_prod = P_prod * 8300/8007 # tweaking the function so that total produced form 1950 to 2015 (including) is 8300.
        
        if (self.scenario_release[0] == "fullstop"):
            P_prod = np.where(time >= self.scenario_release[1], 0, P_prod)
        
        if (self.scenario_release[0] == "pulse"):
            P_prod = np.where(np.floor(time) == self.scenario_release[1], self.scenario_release[2],0)
            
        if (self.scenario_release[0] == "SCS"):
            P_prod = np.where(time < 2016, P_prod, # base case until 2016
                np.where(time <= 2050, -6.44 * time + 13358, #SCS linear equation between 2016 and 2050
                         -6.44 * 2050 + 13358)# fix ratios after 2050 in the value at 2050
                )
            
        return (P_prod)
    
    

    def get_P_waste(self,time):
        #base scenario
        P_waste = np.where(time < 1950, 0,
                           0.000438727092 * time ** 3 - 2.52227209 * time ** 2 + 4831.80835 * time - 3084191.67)
        
        if (self.scenario_release[0] == "fullstop"):
            P_waste = np.where(time >= self.scenario_release[1], 0, P_waste)
            
        if (self.scenario_release[0] == "pulse"):
            P_waste = np.where(np.floor(time) == self.scenario_release[1], self.scenario_release[2],0)
        
        if (self.scenario_release[0] == "SCS"):
            P_waste = np.where(time < 2016, P_waste,
                               np.where(time <= 2050, -0.43237 * time**2 + 1754.06*time - 1778620,
                                        -0.43237*2050**2 + 1754.06*2050 - 1778620) #fix in 2050
                               )
        
        return (P_waste)
    

    
    def get_f_disc(self,time):  
        #please note that in the box model, not the following fractions are used,
        #but instead: f_disc = 1 - f_incin - f_rec
        f_disc = np.where(time < 1980, 1, 
                          np.where(time <= 2050, -0.000000017315 * time ** 3 + 0.0000624932 * time ** 2 - 0.0553287 * time,
                                   -0.000000017315 * 2050 ** 3 + 0.0000624932 * 2050 ** 2 - 0.0553287 * 2050)#fix at 2050
                          )
        
        if (self.scenario_release[0] == "pulse"): 
            f_disc = 1 #in the pulse scenario_release, all waste P is discarded
           
        if (self.scenario_release[0] == "SCS"):
            f_disc = np.where(time < 2016, f_disc, # base case until 2016
                np.where(time <= 2050, -0.013*time + 26.75, #SCS linear equation between 2016 and 2050
                         -0.013*2050 + 26.75)# fix ratios after 2050 in the value at 2025
                )
            
        return (f_disc)
    
    
    

    def get_f_incin(self,time):
        #base case
        f_incin = np.where(time < 1980, 0,
                           np.where(time <=2050, 0.000000010866 * time ** 3 - 0.000040095 * time ** 2 + 0.0367815 * time, #use this between 1980 and 2050
                                    0.000000010866 * 2050 ** 3 - 0.000040095 * 2050 ** 2 + 0.0367815 * 2050) #after 2050 use value of 2050
                           ) 
                           
        
        if (self.scenario_release[0] == "pulse"):
            f_incin = 0 #in the pulse scenario_release, all waste P is discarded
    
        if (self.scenario_release[0] == "SCS"):
            f_incin = np.where(time < 2016, f_incin, # base case until 2016
                np.where(time <= 2050, -0.000475692 * time**2 + 1.93297 * time - 1963.25, #SCS linear equation between 2016 and 2050
                         -0.000475692 * 2050**2 + 1.93297 * 2050 - 1963.25)# fix ratios after 2050 in the value at 2025
                )        
    
        return (f_incin)
    


    def get_f_rec(self,time):
        #base case
        f_rec = np.where(time < 1989, 0,
                         np.where(time <= 2050, 0.00712723 * time - 14.1653,
                                  0.00712723 * 2050 - 14.1653)#fix after 2050
                         )
        
        if (self.scenario_release[0] == "pulse"):
            r_rec = 0 #in the pulse scenario_release, all waste P is discarded
        
        if (self.scenario_release[0] == "SCS"):
            f_rec = np.where(time < 2016, f_rec, # base case until 2016
                np.where(time <= 2050, 0.000475692 * time** 2 - 1.91997*time + 1937.5, #SCS linear equation between 2025 and 2050
                         0.000475692 * 2050**2 - 1.91997 * 2050 + 1937.5)# fix ratios after 2050 in the value at 2025
                )    
        
        return (f_rec)
    
    
    
    def get_f_cleanUp(self,time):
        f_P_cleanUp = 0
        f_MP_cleanUp = 0
        f_sMP_cleanUp = 0
        
        if (self.scenario_cleanup[0] == "cleanup_discarded_fixedfrac"):
            
            f_P_cleanUp = np.where(time >= self.scenario_cleanup[1], self.scenario_cleanup[2][0], 0)
            f_MP_cleanUp = np.where(time >= self.scenario_cleanup[1], self.scenario_cleanup[2][1], 0)
            f_sMP_cleanUp = np.where(time >= self.scenario_cleanup[1], self.scenario_cleanup[2][2], 0)
            
        if (self.scenario_cleanup[0] == "cleanup_discarded_linear_increment"):
            t_ini = self.scenario_cleanup[1][0]#when the increment starts
            slope = self.scenario_cleanup[2]/(self.scenario_cleanup[1][1] - self.scenario_cleanup[1][0])
            
            f_P_cleanUp = np.where(time <  self.scenario_cleanup[1][0],  0 ,
                                   np.where(time < self.scenario_cleanup[1][1], (time - t_ini)*slope[0],
                                            self.scenario_cleanup[2][0]))
            
            f_MP_cleanUp = np.where(time <  self.scenario_cleanup[1][0],  0 ,
                                   np.where(time < self.scenario_cleanup[1][1], (time - t_ini)*slope[1],
                                            self.scenario_cleanup[2][1]))
            
            f_sMP_cleanUp = np.where(time <  self.scenario_cleanup[1][0],  0 ,
                                   np.where(time < self.scenario_cleanup[1][1], (time - t_ini)*slope[2],
                                            self.scenario_cleanup[2][2]))
                                 
            
        
        return (np.array([f_P_cleanUp, f_MP_cleanUp, f_sMP_cleanUp]))
    
    



#FRCS = boxmodel_forcings(("base",),("no_cleanup",))

# print(FRCS.get_P_prod(2000))
# # print(FRCS.get_f_incin(1981))
# print(1 - FRCS.get_f_incin(1980) - FRCS.get_f_rec(1980) )
