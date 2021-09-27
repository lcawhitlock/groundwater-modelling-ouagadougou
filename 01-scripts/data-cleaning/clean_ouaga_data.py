# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 16:10:34 2020

@author: lcawh
"""
def clean(filename,var,varshort):
    '''Cleans the weirdly formatted climate data from Ouagadougou, return pandas
    df with just the date and variable.
    Arguments:
    ==========
    filename (str): CSV file in original-data folder
    var(str): variable in English we're looking at
    varshort (str): short version of the var in Fr which is in cell F2 (or
                    whatever) to target cleaning'''
    
    import pandas as pd
    import numpy as np
    
    #load data and ditch na and extra rows
    names = ('day','01','02','03','04','05','06','07','08','09','10','11','12')
    df = pd.read_csv(f'../../02-data/original-data/climate/{filename}',names=names)
    df = df.dropna(how='all')
    df = df[(df.day!='DEC')&(df.day!='MOIS')&(df.day!='TOTAL')& \
            (df.day!='DATE')&(df.day!='JRS')&(df['05']!=varshort)& \
            (df['04']!='OUAG')]
    
    #add year column (all months have 31 days in this wretched sheet)
    years = []
    for i in range(1961,2005):
        yr = [i]*31
        years = years + yr
    df['year'] = years
    
    #rearrange columns
    cols = df.columns.tolist()
    cols2 = cols[-1:] + cols[:-1]
    df=df[cols2]
    
    #melt into long form and get rid of nans
    value_vars = ['01','02','03','04','05','06','07','08','09','10','11','12']
    df = pd.melt(df,id_vars=['year','day'],
              value_vars=value_vars,
              var_name='month',value_name=var)
    df=df.dropna(how='any')
    
    #add a datetime column for full date
    df['date'] = pd.to_datetime(df[['year','month','day']],dayfirst=True)
    
    #replace random nans bits and pieces
    df = df.replace(to_replace='**',value=np.nan)
    df = df.replace(to_replace='.',value=0)
    df = df.replace(to_replace='TR',value=0)
    df[var] = df[var].astype('float64')
    
    #final ouput just date and var
    final = df[['date',var]]
    
    return final

#################
# TEST FUNCTION #
#################

all_rain = clean('rainfall-19612003.csv','rainfall','PLUVI')
all_rain