# -*- coding: utf-8 -*-
"""
Created on Fri Sep 10 18:40:42 2021

@author: lcawh
"""
def clean(filename,var,varshort,startdate,enddate):
    '''Cleans the weirdly formatted climate data from Ouaga, return pandas
    df with just the date and variable.
    Arguments:
    ==========
    filename (str): CSV file in data folder
    var(str): variable in English we're looking at
    varshort (str): short version of the var in Fr which is in cell F2 (or whatever) to target cleaning'''
    
    import pandas as pd
    import numpy as np
    
    #load data and ditch na
    names = ('day','01','02','03','04','05','06','07','08','09','10','11','12')
    df = pd.read_csv(f'../02-data/original-data/climate/{filename}',names=names,encoding="ISO-8859-1")
    df = df.dropna(how='all')
    df = df[(df.day!='DEC')&(df.day!='MOIS')&(df.day!='TOTAL')& \
            (df.day!='DATE')&(df.day!='JRS')&(df['05']!=varshort)& \
            (df['04']!='OUAG')]
    
    #add year column as every month has 31 days in this spreadsheet
    years = []
    for i in range(startdate,enddate):
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

def clean2(filename,var,startyear,endyear):
    
    #load data with column names
    cols = [0,1,2,3,4,5,6,7,8,9,10,11,12]
    names = ('day','01','02','03','04','05','06','07','08','09','10','11','12')
    df = pd.read_csv(f'../02-data/original-data/climate/{filename}.csv',names=names,usecols=cols,
                    encoding="ISO-8859-1")

    #get rid of extra rows and random text
    df = df[(df.day!='DEC')&(df.day!='MOIS')&(df.day!='TOTAL')& \
            (df.day!='DATE')&(df.day!='JRS')&(df.day.notna())]

    #generate years column
    years = []
    for i in range(startyear,endyear+1):
        yr = [i]*31
        years = years + yr
    df['year'] = years

    #melt to normal-looking table
    value_vars = ['01','02','03','04','05','06','07','08','09','10','11','12']
    df = pd.melt(df,id_vars=['year','day'],
              value_vars=value_vars,
              var_name='month',value_name=var)

    #convert days and months to int
    df.day = df.day.astype('int64')
    df.month = df.month.astype('int64')

    #get rid of rows with rainfall NanN (wrong dates)
    df = df[df.rainfall.notna()]

    #catch stray months with extra days
    m = ['04','06','09','11']
    df = df[~((df.month.isin(m))&(df.day>30))]
    df = df[~((df['month']==2)&(df.day>29))]

    #reindex
    df = df.reset_index(drop=True)

    #convert YMD to datetime
    df['date'] = pd.to_datetime(df[['year','month','day']],dayfirst=True)

    #replace all the weird symbols with NaN and convert variable to float
    df = df.replace(to_replace='**',value=np.nan)
    df = df.replace(to_replace='.',value=0)
    df = df.replace(to_replace='TR',value=0)
    df['rainfall'] = df['rainfall'].astype('float64')

    final = df[['date','rainfall']]
    
    return final

test = clean2('rainfall-19612003','rainfall',1961,2004)
test.head()
