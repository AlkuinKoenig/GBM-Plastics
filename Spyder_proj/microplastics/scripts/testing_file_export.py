import pandas as pd
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 12:00:24 2022

@author: koenigal
"""



# # intialise data of lists.
# data = {'Name':['Tom', 'nick', 'krish', 'jack'],
#         'Age':[20, 21, 19, 18]}
 
# data = soln.y

# # Create DataFrame


data_out = {      
    "Year" : soln.t,
    "P_prod_tot" : soln.y[0],
    "P_waste_tot" : soln.y[1],
    "P_rec_tot" : soln.y[2],
    "P_inc_tot" : soln.y[3],
    "P_disc_tot" : soln.y[4],
    "MP_disc_tot" : soln.y[5],
    
    "P_use" : soln.y[6],
    "P_disc" : soln.y[7],
    "MP_disc" : soln.y[8],
    "sMP_disc" : soln.y[9],
    
    "P_SurfOce" : soln.y[10],
    "MP_SurfOce" : soln.y[11],
    "sMP_SurfOce" : soln.y[12],
    
    "MP_DeepOce" : soln.y[13],
    "sMP_DeepOce" : soln.y[14],
    
    "sMP_atm" : soln.y[15],
    "sMP_soil" : soln.y[16],
    
    "P_beach" : soln.y[17],
    "MP_beach" : soln.y[18],
    "sMP_beach" : soln.y[19],
    
    "MP_sed" : soln.y[20],
    "sMP_sed" : soln.y[21]
}
df = pd.DataFrame(data_out)

outdir = "D:/microplastics_story/plastics_story/output/"
fname = "test2.csv"

df.to_csv(path_or_buf = outdir + fname)