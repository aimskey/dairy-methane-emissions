import csv
import pandas as pd
import requests
import geopandas


#api = 'https://api.census.gov/data/2018/acs/acs5'
#for_clause = "county:*"
#in_clause = "state:36"
#key_value = "cbe5f0098dca16928b9dfef12d2504beb0f4d5ef"
#payload = {'get':["NAME,B20002_001E"], 'for':for_clause, 'in':in_clause, 'key':key_value}

#earnings = requests.get(api,payload)

#row_list = earnings.json()
    
#colnames = row_list[0]
#datarows = row_list[1:]
#earnings = pd.DataFrame(columns=colnames, data=datarows)
#earnings.set_index(["NAME"])

#earnings["GEOID"] = earnings["state"] + earnings["county"]

#earnings["median"] = earnings["B20002_001E"].astype(float)/1000
#earnings.to_csv("earnings.csv", index=False)

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

#Calculate how many cows per square meter of land in each county, converted to acres
nys_cows['cow_area'] = nys_cows['ALAND']/nys_cows['co_cow']/4046.86

#NOTE TO SELF -- SOME ARE INF -- THIS WILL BE A PROBLEM LATER



