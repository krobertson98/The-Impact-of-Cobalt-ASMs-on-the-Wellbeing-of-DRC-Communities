# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 21:03:32 2022

@author: Kaleb Robertson
"""
import pandas as pd


#load mining sites and limit it to cobalt sites only

mines = pd.read_csv('cod_mines_curated_all_opendata_p_ipis.csv', dtype=str)

n_now = len(mines)

print(n_now)
#renaming for simplicty
mines = mines.rename( columns={'visit_date':'date'} )
#checking date format
print(mines['date'])
#%%converts dates to years
ymd = pd.to_datetime(mines["date"],format="%m/%d/%Y")
#only including the year 2020. 2020 is the most recent year with a full set of data,
mines["date"] = ymd.dt.to_period("Y")
year_ok = ymd.dt.year == 2020
dates = mines[year_ok==True]

dates.to_csv('dates.csv')

minesprov = pd.read_csv('dates.csv')
minesprov = minesprov.drop_duplicates( subset='province' )
cobalt = mines.query("mineral1 == 'Cobalt'").drop_duplicates( subset='province' )
print("Cobalt mines provinces",list(cobalt['province']))
print(list(minesprov['province']))
#%%limiting sites to where that have mines
minesprov['province'].to_csv('minesprov.csv')



