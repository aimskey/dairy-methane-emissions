import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

nys_cows_ppl = pd.read_pickle('nys_cows_ppl.pkl')
nys_county_digest = pd.read_pickle('nys_county_digest.pkl')

county_detail = nys_cows_ppl[['NAME_x','pop_area','cow_area','median']]
county_detail = county_detail.copy()

#Drop counties with no cows
county_detail['cow_area'].replace(0,np.nan, inplace=True)
county_detail.dropna(inplace=True)

#Find most dense cow population AND most dense human population
print(county_detail.sort_values(by='pop_area', ascending=False))
print(county_detail.sort_values(by='cow_area', ascending=False))

#Plot cow and population density against each other 
sns.scatterplot(x='pop_area', y="cow_area", data=county_detail)

#Plot cows per acre and median income against each other
sns.scatterplot(x='cow_area', y='median', data=county_detail)
#%%

county_detail["pop_dec"] = pd.qcut(county_detail['pop_area'],10,labels=[1,2,3,4,5,6,7,8,9,10])
county_detail['cow_sept'] = pd.qcut(county_detail['cow_area'],7,labels=[1,2,3,4,5,6,7])
county_detail['median_quint'] = pd.qcut(county_detail['median'],5,labels=[1,2,3,4,5])

#%%
#Pull out cows per acre below 100 and median income below 35. Can pick any cut off.

#Counties with 28% highest cow density and 20% lowest median income
income_cows1 = county_detail.query("median_quint == 1 and cow_sept < 2")
print(income_cows1)

#Counties with 42% highest cow density and 20% lowest median income
income_cows2 = county_detail.query("median_quint == 1 and cow_sept < 3")
print(income_cows2)


#Counties with 42% highest cow density and 50% highest population density
pop_cows1 = county_detail.query("cow_sept < 3 and pop_dec < 5")
print(pop_cows1)

#Counties with 42% highest cow density and 60% highest population density
pop_cows2 = county_detail.query("cow_sept < 3 and pop_dec < 4")
print(pop_cows2)

#%%
#build heatmap

county_detail_low = county_detail.query("median_quint == 1 and cow_sept <")


fig, ax1 = plt.subplots(dpi=300)
fig.suptitle("Where to Build Digesters")
sns.heatmap(county_detail_select, annot=True, fmt=".2f", ax=ax1)
ax1.set_xlabel("State")
ax1.set_ylabel("Candidate")
fig.tight_layout()
#fig.savefig("heatmap.png")
