import aerosol_functions as af
import pytest
import pandas as pd
import numpy as np

# load the number size distribution
data = pd.read_csv("data.sum",index_col=0,parse_dates=True)
temp = 298.15
pres = 101325.0

#### Divide the data.sum file to different years and save them
###years = np.unique([x.year for x in data.index])
###
###for y in years:
###    data_subset=data.iloc[data.index.year==y]
###    data_subset.to_csv("data_%d.sum" % y)

# condensation sink
cs = af.calc_cs(data,temp,pres)

# Calculate the formation rate for particles
dp1 = np.array([30e-9,70e-9])
dp2 = np.array([60e-9,120e-9])
coags = af.calc_coags(data,dp1,temp,pres)
conc = af.calc_conc(data,dp1,dp2)
conc_pos = conc.copy()/5.2
conc_neg = conc.copy()/4.7
conc_pos_small = af.calc_conc(data,[1e-9,1e-9],[30e-9,60e-9]) 
conc_neg_small = conc_pos_small.copy()/1.1
gr = 2.0

J = af.calc_formation_rate(dp1,dp2,conc,coags,gr)

J_neg,J_pos = af.calc_ion_formation_rate(
        dp1,dp2,conc_pos,conc_neg,conc_pos_small,conc_neg_small,conc,coags,gr)



# Calculate the formation rate for ions

filenames = ["data_2015.sum",
        "data_2016.sum",
        "data_2017.sum",
        "data_2018.sum",
        "data_2019.sum",
        "data_2020.sum",
        "data_2021.sum",
        "data_2022.sum"]
# Calculate
