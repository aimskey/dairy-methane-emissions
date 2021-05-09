import pandas as pd
import requests
import geopandas
import numpy as np

#%%

#Collect census data with population and income to assess population density and median income levels in each county.
api = 'https://api.census.gov/data/2018/acs/acs5'
for_clause = "county:*"
in_clause = "state:36"
key_value = "cbe5f0098dca16928b9dfef12d2504beb0f4d5ef"
payload = {'get':["NAME,B20002_001E,B01001_001E"], 'for':for_clause, 'in':in_clause, 'key':key_value}

pop_earnings = requests.get(api,payload)

row_list = pop_earnings.json()
    
colnames = row_list[0]
datarows = row_list[1:]
pop_earnings = pd.DataFrame(columns=colnames, data=datarows)
pop_earnings.set_index(["NAME"])

#Create GEOID column for future merging
pop_earnings['GEOID'] = pop_earnings['state'] + pop_earnings['county']
pop_earnings.rename(columns={"B01001_001E":"pop","B20002_001E":"income"}, inplace=True)

#Calculate median income
pop_earnings["median"] = pop_earnings["income"].astype(float)/1000

#%%
#Import county dairy cow numbers
county_cows = pd.read_csv('county_cows.csv')
county_cows["co_cow"] = county_cows["co_cow"].str.replace(",","").astype(float)

#Import USA shapefile
counties =  geopandas.read_file('zip://tl_2020_us_county.zip')

#Isolate New York state
nys_counties = counties.query("STATEFP == '36'")
print(len(nys_counties))

#Merge County with cow numbers
nys_cows = nys_counties.merge(county_cows,
                              left_on = "NAME",
                              right_on = "county_name",
                              how="left",
                              validate="1:1",
                              indicator=True)

print(nys_cows['_merge'].value_counts())

#%%
#Clean up data frame
nys_cows.drop(['county_name','_merge'], axis='columns', inplace=True)


#Calculate how many cows per square meter of land in each county, converted to acres
nys_cows['cow_area'] = nys_cows['ALAND']/nys_cows['co_cow']/4046.86

#Fix counties with 0 cows
nys_cows['cow_area'].replace([np.inf,-np.inf],0, inplace=True)

#Save to geopackage file
nys_cows.to_file('nys_data.gpkg', layer='cows', driver='GPKG')
#%%

#Merge census population data

nys_cows_ppl = nys_cows.merge(pop_earnings,
                              on='GEOID',
                              how='left',
                              validate='1:1',
                              indicator=True)

print(nys_cows_ppl['_merge'].value_counts())

nys_cows_ppl.drop(['_merge'], axis='columns', inplace=True)

#%%
#Calculate population per acre to keep it in the same units
nys_cows_ppl['pop_area'] = nys_cows_ppl['ALAND']/nys_cows_ppl['pop'].astype(float)/4046.86

nys_cows_ppl.to_file('nys_data.gpkg', layer='population', driver='GPKG')
nys_cows_ppl.to_file('nys_data.gpkg', layer='earnings', driver='GPKG')

#%%
#Import digester data and isolate NYS
#Note to self - could pickle this from previous script
digester_db = pd.read_csv("agstar-livestock-ad-database.csv")

#Editing header column to eliminate extra spaces
digester_db.columns = digester_db.columns.to_series().apply(lambda x: x.strip()) #found this line of code online after having problems with python not being able to read my data frame
digester_db = digester_db[["County","State", "Status", "Animal/Farm Type(s)"]]

#Changing column names. Note: it's important to remember the unit of measurement for total emissions (in thise case MTCO2e)
digester_db.rename(columns={'Animal/Farm Type(s)':'farm_type'}, inplace=True)

#Isolating only the dairy farms that have operational anaerobic digesters
nys_digesters = digester_db.query("farm_type == 'Dairy' and State == 'NY'")

#Merge digesters with census data
nys_county_digest = nys_counties.merge(nys_digesters,
                                       left_on = 'NAME',
                                       right_on = 'County',
                                       how = 'left',
                                       validate = '1:m',
                                       indicator = True)

#Drop duplicate records - I want to know if a county has digesters, not how many
nys_county_digest.drop_duplicates(['County'], inplace=True)
nys_county_digest.dropna(subset=['County'], inplace=True)
nys_county_digest.drop(['_merge'], axis='columns', inplace=True)

nys_county_digest.to_file('nys_data.gpkg', layer='digesters', driver='GPKG')









