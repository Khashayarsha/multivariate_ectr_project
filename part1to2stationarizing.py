# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 02:51:57 2020

@author: XHK
"""

#Evidence in favour or against presence of deterministic components such as a constant or linear trend:

import numpy as np 
import openpyxl
from pathlib import Path
import pandas as pd

	
from pandas import read_csv
from matplotlib import pyplot  

import statsmodels.api as sm


from statsmodels.tsa.stattools import adfuller
file_name = 'MVE_assignment_2020_dataset.xlsx'
variables = ['ISO_N3', 'ISO_C3', 'Country', 'Year', 'Precipitation'
                     , 'Radiation', 'Temperature', 'GDP', 'GDP per capita'
                     , 'Population', 'AG Land', 'Crop']
data = pd.read_excel(file_name,names = variables)


nor = data[data['Country']=='Norway']
ned = data[data['Country']=='Netherlands']

variables = [ 'Precipitation'
                     , 'Radiation', 'Temperature', 'GDP', 'GDP per capita'
                     , 'Population', 'AG Land', 'Crop']

nor = nor[variables]
ned = ned[variables]



def regress_on_t(time_series, differenced_periods = 0):
    y = [i for i in time_series if type(i) == float or type(i) ==int] #ignoring non-numericals
    x = np.array([i for i in range(len(y))])
    x = sm.add_constant(x)
    
    
    mod = sm.OLS(y,x)
    res = mod.fit(cov_type='HC1')
    print(res.summary())
    print("B_0, B_1 = ", [i for i in res.params])
    
    return res, x, y

for var in variables:
    print("$$$$$$$$$$$$$$$$ $$$$$$$$$$$$$ $$$$$$$$$$$$$$$ $$$$$$$$$$$$$ ")
    print(var)
    print("Norway:   ")
    regress_on_t(nor[var])
    print(var)
    print("The Netherlands: ")
    regress_on_t(ned[var])

## plotting all raw data:   ignoring last entries because some non-numericals 
nor = nor.iloc[:-3]
ned = ned.iloc[:-3]    

nor.plot(subplots=True, layout = (4,2), title = "Norway")
ned.plot(subplots=True, layout = (4,2), title = "The Netherlands")



###  now gonna take out the linear trends that were revealed by linear regression:
### for: 
### Norway:  Precipitation, Temperature, Crop
### Netherlands: 
### Take logs of:
###    Norway: GDP, Population
###    Netherlands: GDP, Population
###

def de_trend(data):
    """Removes linear trend from a n*1 dataseries"""
    res, _, y = regress_on_t(data)
    x = np.array([i for i in range(len(y))])
    constant, b_1 = res.params[0], res.params[1]
    
    de_trended = (y-constant)-(b_1*x)
    
    #print(de_trended)
    return de_trended

def adf_test(data):
    
    result = adfuller(data)
    print('ADF Statistic: %f' % result[0])
    print('p-value: %f' % result[1])
    print('Critical Values:')
    for key, value in result[4].items():
     	print('\t%s: %.3f' % (key, value))
         
         
adf_tests = []

de_trendeds_nor = pd.DataFrame()
de_trendeds_ned = pd.DataFrame()

for var in variables:
    de_trendeds_nor[var] = de_trend(nor[var])
    de_trendeds_ned[var] = de_trend(ned[var])


de_trendeds_nor.plot(subplots=True, layout = (4,2), title = "Norway de-trended")
de_trendeds_ned.plot(subplots=True, layout = (4,2), title = "Netherlands de-trended")


def print_adfs(variables, data_before, data_after, name):
    for var in variables:
        print("----------------------------------------------")
        print(name)
        print(var, " before :")        
        adf_test(data_before[var])
        print()
        print(var, " after ")
        adf_test(data_after[var])


             #DETRENDING 

#print_adfs(variables, nor, de_trendeds_nor, "Norway")
#print_adfs(variables, ned, de_trendeds_ned, "The Netherlands")

             # DIFFERENCING 
diffed_nor = nor.diff(periods=1)
diffed_ned = ned.diff(periods=1)

 
# print_adfs(variables, nor, diffed_nor.dropna(), "Norway")
#print_adfs(variables, ned, diffed_ned.dropna(), "The Netherlands")
# =============================================================================

diffed_nor.dropna().plot(subplots=True, layout = (4,2), title = "Norway first difference")
diffed_ned.dropna().plot(subplots=True, layout = (4,2), title = "The Netherlands first difference")

diff2_nor = diffed_nor.dropna().diff().dropna()
diff2_ned = diffed_ned.dropna().diff().dropna()

diff2_nor.plot(subplots = True, layout = (4,2), title = "Norway Second Difference")
diff2_ned.plot(subplots = True, layout = (4,2), title = "The Netherlands Second Difference")


#Evidence in favour or against presence of deterministic components such as a constant or linear trend:
#def regress_on_time(series):

# Putting all stationary variables together 

# For Norway we want:
    #Raw data: Radiation 
    # De-trended: Precipitation Temperature, Crop 
    # First-diff: GDP, GDP-per-Capita, AG-land
    # THIRD-diff: Population
    

# For Netherlands we want:
    #Raw data: Precipitation, Radiation, 
    # De-trended: Temperature
    # First-diff: GDP, GDP-per-Capita, AG-land, Crop
    # SECOND-diff: Population


nor_data = pd.DataFrame()
nor_data["pre_detrend"] = de_trendeds_nor['Precipitation']
nor_data["rad_raw"] = nor['Radiation']
nor_data["temp_detrend"] = de_trendeds_nor['Temperature']
nor_data["gdp_diff1"] = diffed_nor["GDP"]
nor_data["gdp_capita_diff1"] = diffed_nor["GDP per capita"]
nor_data["ag_diff1"] = diffed_nor["AG Land"]
nor_data["crop_detrend"] = de_trendeds_nor["Crop"]
nor_data["pop_diff3"] =  diffed_nor["Population"].diff().diff()
    
ned_data = pd.DataFrame()
ned_data["pre_raw"] = ned['Precipitation']
ned_data["rad_raw"] = ned['Radiation']
ned_data["temp_detrend"] = de_trend(ned["Temperature"])
ned_data["gdp_diff1"] = diffed_ned["GDP"]
ned_data["gdp_capita_diff1"] = diffed_ned["GDP per capita"]
ned_data["ag_diff1"] = diffed_ned["AG Land"]
ned_data["crop_diff1"] = diffed_ned["Crop"]
ned_data["pop_diff2"] =  diffed_ned["Population"].diff()


nor_data.to_excel("NorwayStationaryData.xlsx")
ned_data.to_excel("NetherlandsStationaryData.xlsx")