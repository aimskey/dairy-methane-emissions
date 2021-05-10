import pandas as pd
import seaborn as sns
import numpy as np

nys_cows_ppl = pd.read_pickle('nys_cows_ppl.pkl')

county_detail = nys_cows_ppl[['NAME_x','pop_area','cow_area','median']]
county_detail = county_detail.copy()
county_detail.rename(columns={'NAME_x':'County'},inplace=True)
county_detail.set_index('County', inplace=True)

#Find most dense cow population AND most dense human population
print(county_detail.sort_values(by='pop_area', ascending=False))
print(county_detail.sort_values(by='cow_area', ascending=False))

#Plot cow and population density against each other 
sns.scatterplot(x='pop_area', y="cow_area", data=county_detail)

#Plot cows per acre and median income against each other
sns.scatterplot(x='cow_area', y='median', data=county_detail)

#Drop counties with no cows
county_detail['cow_area'].replace(0,np.nan, inplace=True)
county_detail.dropna(inplace=True)

#%%
#Breaking data down into smaller chunks for analysis. Population in deciles, cows in sevens (~14%), and median income in quintiles.
county_detail["pop_dec"] = pd.qcut(county_detail['pop_area'],10,labels=[1,2,3,4,5,6,7,8,9,10])
county_detail['cow_sept'] = pd.qcut(county_detail['cow_area'],7,labels=[1,2,3,4,5,6,7])
county_detail['median_quint'] = pd.qcut(county_detail['median'],5,labels=[1,2,3,4,5])

income_cows1 = county_detail.query("median_quint == 1 and cow_sept < 2")
print('\nCounties with 28% highest cow density and bottom 20% median income:',income_cows1)

income_cows2 = county_detail.query("median_quint == 1 and cow_sept < 3")
print('\nCounties with 42% highest cow density and bottom 20% median income:', income_cows2)

pop_cows1 = county_detail.query("cow_sept < 3 and pop_dec < 5")
print('\nCounties with 42% highest cow density and 50% highest population density:',pop_cows1)

pop_cows2 = county_detail.query("cow_sept < 3 and pop_dec < 4")
print('\nCounties with 42% highest cow density and 60% highest population density:',pop_cows2)

