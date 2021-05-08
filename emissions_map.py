import pandas as pd
import geopandas


#Import and clean up emissions and digester data frame
digest_ornot = pd.read_pickle('digest_ornot.pkl')
emissions = digest_ornot.drop(['Total Animals', 'Emissions per Head', 'Status', 'farm_type','num_cows',
                   'em_reduct','usda_fund','States with Incentive','Digesters',
                   'Dairy Cows','year_operational'], axis="columns")
emissions.drop_duplicates(subset='Dairy Cows', inplace=True)

print(len(emissions))

##ISN'T WORKING - MUST EDIT DROP DUPLICATES

#Import shapefile
usa = geopandas.read_file('zip://tl_2020_us_state.zip')

#Merge shapefile with emissions
us_emissions = usa.merge(emissions, left_on="STUSPS",
                                  right_on="State",
                                  how="left",
                                  validate="1:1",
                                  indicator=True)

#Make sure all states accounted for
print(len(us_emissions.value_counts()))
us_emissions.drop(['_merge'], axis='columns', inplace=True)

#Save to geopackage
us_emissions.to_file('us_emissions.gpkg', layer='emissions', driver='GPKG')

#Create digesters data frame
digesters_state = digest_ornot.drop(['MTCO2e Emissions','Total Animals', 'Emissions per Head', 'Status', 'farm_type','num_cows',
                   'em_reduct','usda_fund','States with Incentive',
                   'Dairy Cows','year_operational'], axis="columns")

#Merge
digesters_us = usa.merge(digesters_state, left_on="STUSPS",
                         right_on="State",
                         how="left",
                         validate="1:1",
                         indicator=True)

print(len(digesters_us.value_counts()))
digesters_us.drop(['_merge'],axis='columns', inplace=True)

digesters_us.to_file('us_emissions.gpkg', layer='digesters', driver='GPKG')




