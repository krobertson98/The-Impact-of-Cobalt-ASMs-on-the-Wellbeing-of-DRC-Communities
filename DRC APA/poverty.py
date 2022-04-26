# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 20:22:51 2022

@author: Kaleb Robertson
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


pov = pd.read_excel('cod-region-results-mpi-2021.xlsx')
#selecting out the provinces 
pov = pov.rename( columns={'Subnational region':'province'} )
pov = pov.set_index("province")
print('Number of Provinces:', len(pov))
print("\nList Of Provinces:\n", pov.index)

#getting poverty data for region
pov = pov.rename( columns={'In severe poverty':'poverty'} )

#%%
#total number of those in poverty in each province
pov['pro_pov'] = (pov['poverty']/100) * 84068 #total pop of DRC in 2018
pro_pov =pov['pro_pov'].sort_values().round(2)
print("\nNumber of People by Province in Poverty by Thousands:\n", pro_pov)

#getting the total of populations in poverty in the Country
tot_pov = pro_pov.sum().round(2) * 1000
print("Total number of people of DRC in Severe Poverty:", tot_pov)

#collecting province property data to be used for gis to compare areas with and without cobalt mines
pov.to_csv("pro_pov.csv")
pover = pd.read_csv("pro_pov.csv")
groupedvalues=pover.groupby('province').sum().reset_index()
#uploading previously made file to identify  provinces that have mines in them
minespr = pd.read_csv("minesprov.csv")
in_group = groupedvalues['province'].isin(['Haut-Uélé', 'Sud-Kivu', 'Tanganyika', 'Ituri', 'Lualaba', 'Haut-Katanga', 'Nord Kivu'])
subset = groupedvalues[ in_group ].sort_values('poverty')
out_group =groupedvalues['province'].isin(['Haut-Uélé', 'Sud-Kivu', 'Tanganyika', 'Ituri', 'Lualaba', 'Haut-Katanga', 'Nord Kivu'])== False
seperate = groupedvalues[ out_group ].sort_values('poverty')
print(list(seperate['province']))
small_group = seperate['province'].isin(['Kinshasa', 'Kongo Central', 'Tshopo', 'Équateur', 'Mai-Ndombe', 'Bas-Uélé', 'Lomami', 'Kasaï-Oriental', 'Haut-Lomami','Mongala', 'Sankuru'])
subset2 =seperate[small_group]
large_group = seperate['province'].isin(['Kinshasa', 'Kongo Central', 'Tshopo', 'Équateur', 'Mai-Ndombe', 'Bas-Uélé', 'Lomami', 'Kasaï-Oriental', 'Haut-Lomami','Mongala', 'Sankuru'])==False
subset3 = seperate[large_group]
#looking at the two provinces with Cobalt mines
cobalt = groupedvalues['province'].isin(['Lualaba', 'Haut-Katanga'])
subset4 = groupedvalues[ cobalt ].sort_values('poverty')
#%%making a figure to display severe poverty by province for mining provinces
fig, ax1 = plt.subplots()
sns.barplot(data=subset,x='province',y='pro_pov',ax=ax1)
plt.xticks(rotation = 45)
ax1.set_title("Severe Poverty in DRC in Mining Provinces (2018)")
ax1.set_xlabel("Provinces")
ax1.set_ylabel("Amount of people in Poverty")
fig.tight_layout()
fig.savefig('pov_mining.png')

fig, ax1 = plt.subplots()
sns.barplot(data=subset2,x='province',y='pro_pov',ax=ax1)
plt.xticks(rotation = 45)
ax1.set_title("Severe Poverty in DRC in Nonmining Provinces (2018)")
ax1.set_xlabel("Provinces")
ax1.set_ylabel("Amount of people in Poverty")
fig.tight_layout()
fig.savefig('pov_nonmining1.png')

fig, ax1 = plt.subplots()
sns.barplot(data=subset3,x='province',y='pro_pov',ax=ax1)
plt.xticks(rotation = 45)
ax1.set_title("Severe Poverty in DRC in Nonmining Provinces (2018) pt2")
ax1.set_xlabel("Provinces")
ax1.set_ylabel("Amount of people in Poverty")
fig.tight_layout()
fig.savefig('pov_nonmining2.png')

fig, ax1 = plt.subplots()
sns.barplot(data=subset4,x='province',y='pro_pov',ax=ax1)
plt.xticks(rotation = 45)
ax1.set_title("Severe Poverty in DRC in Cobalt mining Provinces (2018)")
ax1.set_xlabel("Provinces")
ax1.set_ylabel("Amount of people in Poverty")
fig.tight_layout()
fig.savefig('pov_cobalt.png')

mines_mean = round(subset['pro_pov'].mean(axis=0),2)
print("Mean of People in Severe poverty where there are mines:",mines_mean)

non_mean = round(seperate['pro_pov'].mean(axis=0),2)
print("Mean of People in Severe Poverty with no mines:",non_mean)

cobalt_mean = round(subset4['pro_pov'].mean(axis=0),2)
print("Mean of people in severe poverty with Cobalt mines:", cobalt_mean)
