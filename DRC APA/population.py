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
print("\nPopulation in each Province\n",pop['Pop_2020'])
print("Total Population of DRC (2020):",pop['Pop_2020'].sum())

#%%getting the amount of people displaced in provinces
con = pd.read_excel('rdc_mouvement_de_population_deplace_octobre_2021.xlsx')
con = con.rename( columns={'creation_date':'date','admin1_label':'province'} )

ymd = pd.to_datetime(con["date"],format="%m%d%y")
#only including the year 2020. 2020 is the most recent year with a full set of data,matches year of previous files
con["date"] = ymd.dt.to_period("Y")
year_ok = ymd.dt.year <= 2021
dates = con[year_ok==True]
fight = dates

#dropping columns with other dates not needed due to using the date based off creation of the report since it is already evaulated to be in dataset
fight = fight.drop(columns='evaluation_date')
fight = fight.drop(columns='movement_date')
con_prov = fight['person'].groupby(fight['province'])
print("\nInternally displaced people by province:\n",con_prov.sum())
tight = con_prov.sum()
#this figure does not include displaced people before 2019 that was about 2.9 million people
print("Total displaced people in DRC from 2019 to 2020:",fight['person'].sum())


#%%Creating the figures to display the displaced people
#seperating out provinces with lowest numbers to get a better scale for the y axis
in_group = fight['province'].isin(['Maniema','Haut-uele','Nord-kivu'])
subset = fight[ in_group ].sort_values('person')

fig, ax1 = plt.subplots()
sns.barplot(data=subset,x='province',y='person',ax=ax1)
plt.xticks(rotation = 45)
ax1.set_title("Interanlly Displaced People in DRC by Province 2019-2020")
ax1.set_xlabel("Provinces")
ax1.set_ylabel("Internally Displaced People")
fig.tight_layout()
fig.savefig('conflict.png')

out_group = fight['province'].isin(['Maniema','Haut-uele','Nord-kivu'])==False
subset2 = fight[ out_group ].sort_values('person')

#using the remainder of the highest values
fig, ax1 = plt.subplots()
sns.barplot(data=subset2,x='province',y='person',ax=ax1)
plt.xticks(rotation = 45)
ax1.set_title("Interanlly Displaced People in DRC by Province 2019-2020")
ax1.set_xlabel("Provinces")
ax1.set_ylabel("Internally Displaced People")
fig.tight_layout()
fig.savefig('conflict.png')