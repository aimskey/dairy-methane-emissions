import pandas as pd
import matplotlib.pyplot as plt

#%%

us_state_abbrev = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
'Connecticut': 'CT', 'Delaware': 'DE', 'Distict of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'United States':'US'}

#Import database of incentive programs across the US
state_incentives = pd.read_csv("list_state_incentives.csv")

#Isolate the state nme and status
state_incentives = state_incentives[["Place", "Incentive/Active"]]
state_incentives.rename(columns={"Place":"program_state", "Incentive/Active":"program_status"}, inplace=True)

#Replace state name with abbreviations
state_incentives["program_state"] = state_incentives["program_state"].map(us_state_abbrev)

#Drop nan values
state_incentives.dropna(axis="rows", inplace=True)

#Isolate active programs
active_incentives = state_incentives[state_incentives["program_status"]]

#%%
#Import database of anaerobic digesters in US
digester_db = pd.read_pickle('digester_db.pkl')

#Calculate total number of Incentive Programs
print("\nNumber of Incentive Programs for Each Participating State")
print(active_incentives["program_state"].value_counts())

#Calculate total number of digesters
print("\nNumber Anaerobic Digesters for Each State")
print(digester_db["State"].value_counts())

#%%

#Add column to digester database with active incentive programs
digester_db["States with Incentive"] = active_incentives["program_state"]

#Create values to plot against each other
states_w_i = digester_db["States with Incentive"].value_counts()
states_w_d = digester_db["State"].value_counts()

#Create data frame with only value counts
compare = pd.DataFrame()
compare["States with Incentive"] = states_w_i
compare["State"] = states_w_d
compare.rename(columns={'States with Incentive':'Number of Incentives', 'State':'Number of Digesters'}, inplace=True)
compare.fillna(0, inplace=True)

#Look at total sorted number of incentives and sorted number of digesters
print('\nSorted by Digesters:',compare.sort_values(by='Number of Digesters'))
print('\nSorted by Incentives:',compare.sort_values(by='Number of Incentives'))


#Create scatter plot
plt.figure()
ax = compare.plot.scatter("Number of Digesters", "Number of Incentives")
ax.set_title("Potential Impact of Incentive Programs")
ax.set_xlabel("Number of Anaerobic Digesters")
ax.set_ylabel("Number of Incentive Programs")
ax.figure.savefig("policyimpact.png", dpi=300)

#%%

#Import cow numbers and emissions data from state_emissions script
cow_num = pd.read_pickle('cow_num.pkl')
total_methane = pd.read_pickle('total_methane.pkl')

#Drop unnecessary columns
total_methane.drop(['Dairy Cows','Manure Emissions','total'],axis="columns",inplace=True)
total_methane.rename(columns={'converted_MTCO2e':'MTCO2e Emissions'}, inplace=True)

#Merge emissions with cow numbers and clean up data frame
total_methane_num = total_methane.merge(cow_num, 
                                        on='State',
                                        how='outer',
                                        validate='1:1',
                                        indicator=True)
total_methane_num.drop(['Dairy Calves','Replacements','_merge'],axis='columns',inplace=True)
total_methane_num.rename(columns={'total':'Total Animals'},inplace=True)

#Convert cow numbers into thousands
total_methane_num['Dairy Cows'] = total_methane_num['Dairy Cows']*1000

#Create column of emissions/head
total_methane_num['Emissions per Head'] = total_methane_num['MTCO2e Emissions']/total_methane_num['Dairy Cows']

#Clean up digester data frame. Emissions data is from 2019 so must eliminate digesters operational after 2019.
print('\nTotal Digesters:',len(digester_db))
digest_operational = digester_db.query("year_operational <= 2019")
print('\nTotal Digesters Operational By 2019:',len(digest_operational))

digest_states = digest_operational.drop(['Status','farm_type','em_reduct','usda_fund','States with Incentive'],axis="columns")
digest_ornot = total_methane_num.reset_index().merge(digest_operational,
                                                     on='State',
                                                     how='left',
                                                     validate='1:m',
                                                     indicator=True)
digest_ornot = digest_ornot.set_index('State')


#Make data frame easier to read
digest_ornot.rename(columns={'_merge':'Digesters'}, inplace=True)
digest_ornot['Digesters'].replace(['both'],'Y', inplace=True)
digest_ornot['Digesters'].replace(['left_only'],'N', inplace=True)

#Pickle for future use
digest_ornot.to_pickle('digest_ornot.pkl')

#Dropping AK because it has emissions but no head of cattle in data frame
digest_ornot.drop('AK', axis="rows",inplace=True)

#Query for states with no digesters
no_digest = digest_ornot.query("Digesters == 'N'")

#Query for states with digesters
digest = digest_ornot.query("Digesters == 'Y'")

#Reset index to drop duplicates, then reassign
digest = digest.reset_index()
digest = digest.drop_duplicates(subset='State', keep='first')
digest = digest.set_index('State')

#Total emissions
total_digest = round(digest['Emissions per Head'].sum()/len(digest['Emissions per Head']),3)
total_nodigest = round(no_digest['Emissions per Head'].sum()/len(no_digest['Emissions per Head']),3)

#Convert to KGs - I think it's easier to conceive of kilograms when thinking of per cow basis
convert_digest = 1000*total_digest
convert_nodigest = 1000*total_nodigest                                                           

print('\nTotal Emissions per Head for States with Digesters:',total_digest, 'MTCO2e/year',
      '\nor',convert_digest,'KGCO2e/year')
print('\nTotal Emissions per Head for States without Digesters:',total_nodigest,'MTCO2e/year',
      '\nor',convert_nodigest,'KGCO2e/year')

#%%
#Plot emissions
fig, (ax1, ax2) = plt.subplots(1,2)
no_digest['Emissions per Head'].plot.hist(ax=ax1)
ax1.set_title("No Digesters")
ax1.set_xlabel('Emissions/Head')
digest['Emissions per Head'].plot.hist(ax=ax2)
ax2.set_title("Digesters")
ax2.set_xlabel('Emissions/Head')
fig.tight_layout()
fig.savefig('em_digest.png',dpi=300)

#%%
















