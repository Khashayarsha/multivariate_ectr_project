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

# plotting all raw data:   ignoring last entries because some non-numericals 
    

nor.iloc[:-3].plot(subplots=True, layout = (4,2), title = "Norway")
ned.iloc[:-3].plot(subplots=True, layout = (4,2), title = "The Netherlands")

nor = nor.iloc[:-3]
ned = ned.iloc[:-3]

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
    
    print(de_trended)
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
        print(var, " before detrending :")        
        adf_test(data_before[var])
        print()
        print(var, " after detrending:")
        adf_test(data_after[var])

print_adfs(variables, nor, de_trendeds_nor, "Norway")
print_adfs(variables, ned, de_trendeds_ned, "The Netherlands")





# meanpre:Mean precipitation
# meanrad:Mean radiation
# meantmp:Average yearly temperature
# NY.GDP.MKTP.KD:GDP (constant 2010 US$)
# NY.GDP.PCAP.KD:GDP per capita (constant 2010 US$)
# SP.POP.TOTL:Population
# totalAG.LND.AGRI.K2:Agricultural land (sq. km)
# AG.PRD.CROP.XD:Crop production index




#Evidence in favour or against presence of deterministic components such as a constant or linear trend:
#def regress_on_time(series):
    