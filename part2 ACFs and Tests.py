# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 16:35:42 2020

@author: XHK
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.api import VAR
from pandas import read_csv
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from scipy.stats import pearsonr

#nor_vars = ['pre_detrend', 'rad_raw', 'temp_detrend', 'gdp_diff1',
       #'gdp_capita_diff1', 'ag_diff1', 'crop_diff1', 'pop_diff3']
#ned_vars = ['pre_raw', 'rad_raw', 'temp_detrend', 'gdp_diff1', 'gdp_capita_diff1',
       #'ag_diff1', 'crop_diff1', 'pop_diff3']
#  Loading all data and removing a useless column
nor_data = pd.read_excel("NorwayStationaryData.xlsx")
ned_data = pd.read_excel("NetherlandsStationaryData.xlsx")
nor_data = nor_data.drop(['Unnamed: 0'], axis = 1)
ned_data = ned_data.drop(['Unnamed: 0'], axis = 1)

nor_vars = list(nor_data.columns)
ned_vars = list(ned_data.columns)

from arch.unitroot import ADF
from arch.unitroot import PhillipsPerron
from statsmodels.stats.diagnostic import acorr_ljungbox, acorr_breusch_godfrey
from statsmodels.stats.stattools import durbin_watson

def serial_residuals(data, trend = '', prnt = False, plots = False, name = '', lags = 1):
    adf = ADF(data)
    
    print('lags  = ', lags)
    if trend in ['c', 'ct', 'ctt']:
        adf.trend = trend
    reg_res = adf.regression
    pp = PhillipsPerron(data)
    if lags > 0:
        adf.lags = lags
        pp.lags = lags
        
    if prnt == True:
        print("ADF summary of ", name, 'with trend: ', trend )
        print(adf.summary().as_text())
        
        #print("regression summary of ", name, 'with trend: ', trend)
        #print(reg_res.summary().as_text())
    
    resids = pd.DataFrame(reg_res.resid)
    column_name = 'residuals' + name
    resids.columns = [column_name]
    #fig = resids.plot()
    if plots:
        acf = plot_acf(reg_res.resid,title='Residual Autocorrelations '+name)
        acf.savefig('residuals_ACF_'+name+'.png')
    #pacf = plot_pacf(reg_res.resid,title='Partial Residual Autocorrelations '+name)
    #fig = acf[1:].plot(kind='bar', title='Residual Autocorrelations '+name)

    godfrey = acorr_breusch_godfrey(reg_res,nlags=n_lags)
    return adf, pp, resids, godfrey
    #'nc' : No deterministic terms
    #'c' : Constant only
    #'ct' : Constant and time trend
    #'ctt' : Constant, time trend and time-trend squared

    
    
nor_adf_results = []
ned_adf_results = []

nor_residual_dfs = []
ned_residual_dfs = []

nor_pp_results = []
ned_pp_results = []

nor_godfreys = []
ned_godfreys = []
n_lags =  10


# Checking for serial correlation:
for var in nor_vars:
    print(var)
    
    adf, pp, resids, godfrey = serial_residuals(nor_data[var].dropna(), name = var+ " Norway", lags = n_lags)
    nor_adf_results.append(adf)
    nor_pp_results.append(pp)
    nor_residual_dfs.append(resids)
    nor_godfreys.append(godfrey)
    
    
for var in ned_vars:
    print(var)
    
    adf, pp, resids, godfrey = serial_residuals(ned_data[var].dropna(), name = var+ " Netherlands", lags = n_lags)
    ned_adf_results.append(adf)
    ned_pp_results.append(pp)
    ned_residual_dfs.append(resids)
    ned_godfreys.append(godfrey)
    
    


if True:
    print("p-values Breusch-Godfrey test on Norway, n_lags = ", n_lags)    
    print([i[1] for i in nor_godfreys])
    print("p-values Breusch-Godfrey test on The Netherlands, n_lags = ", n_lags)
    print([i[1] for i in ned_godfreys])
    
    for residuals in nor_residual_dfs:
        print("Ljung-Box for Norway")
        print(acorr_ljungbox(residuals ,lags=[n_lags], return_df=True))
        
    for residuals in ned_residual_dfs:
        print("Ljung-Box for The Netherlands")
        print(acorr_ljungbox(residuals ,lags=[n_lags], return_df=True))    




