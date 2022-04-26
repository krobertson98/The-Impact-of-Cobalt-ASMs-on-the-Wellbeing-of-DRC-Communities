# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 19:32:48 2022

@author: Kaleb Robertson
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Making sure the number and names of province match other datasets
pop =  pd.read_csv('cod_admpop_adm1.csv')
pop = pop.rename( columns={'admin1Name_fr':'province'} )
pop = pop.set_index("province")
print('Number of Provinces:', len(pop))
print("\nList Of Provinces:\n", pop.index)

#getting the population total pop for each province
print("Population in each Province",pop['Pop_2020'])
print("Total Population of DRC (2020)",pop['Pop_2020'].sum())
#%%
#getting the amount of internally displaced people in countries as an indicator for 
con = pd.read_excel('rdc_mouvement_de_population_deplace_juin_2021.xlsx')
con = con.rename( columns={'creation_date':'date','admin1Name_fr':'province','person':'Pop_2020'} )
ymd = pd.to_datetime(con["date"],format="%m%d%y")
#only including the year 2020. 2020 is the most recent year with a full set of data,matches year of previous files
con["date"] = ymd.dt.to_period("Y")
year_ok = ymd.dt.year >= 2020
con["dateuse"] = con[year_ok==True]
fight = con.groupby('province')
con_prov = fight['Pop_2020']
print("Internally displaced people by province:",con_prov)
print("Total displaced people in DRC (2020):",con_prov.sum())
#checking if there is the same number and same number of province
print("Number of provinces:",len(fight),"\nList of provinces:\n",fight.index)
con_prov.to_csv("conflict.csv")

use = pd.read_csv("conflict.csv")
join_keys = ["province","Pop_2020",] 
#merging the datasets using a one to one outer join
merged = use.merge(pop, on=join_keys , how="outer", validate="1:1", indicator=True)
#getting the number of records in both data sets and the ones not in both.
print(merged["_merge"].value_counts())

merged.to_csv("join.csv",index=False)
#%%
join = pd.read_csv('join.csv')
keep_prov = join["province"].isin(top_cand.index)
keep_pov = join["Pop_2020"].isin(top_state.index)
keep = keep_cand & keep_state
sub = reset[keep]
grouped = sub.groupby(["STATE","CAND_NAME"])
summed = grouped['amt'].sum()
grid = summed.unstack("STATE")
fig, ax1 = plt.subplots(dpi=300)
fig.suptitle("Contributions in Millions")
sns.heatmap(grid, annot=True,fmt=".0f", ax=ax1)
ax1.set_xlabel("State")
ax1.set_ylabel("Row")
fig.tight_layout()
fig.savefig("heatmap.png")