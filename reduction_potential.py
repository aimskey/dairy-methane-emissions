import pandas as pd

us_state_abbrev = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
'Connecticut': 'CT', 'Delaware': 'DE', 'Distict of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'United States':'US'}

digester_db = pd.read_csv("agstar-livestock-ad-database.csv", dtype=str)
digester_db.columns = digester_db.columns.to_series().apply(lambda x: x.strip())
digester_db['Dairy'] = digester_db['Dairy'].str.replace(",","").astype(float)
digester_db['Total Emission Reductions (MTCO2e/yr)'] = digester_db['Total Emission Reductions (MTCO2e/yr)'].str.replace(",","").astype(float)
digester_db = digester_db[["State", "Status", "Animal/Farm Type(s)", "Dairy", "Total Emission Reductions (MTCO2e/yr)", "Awarded USDA Funding?"]]
digester_db.rename(columns={'Animal/Farm Type(s)':'farm_type','Dairy':'num_cows','Total Emission Reductions (MTCO2e/yr)':'em_reduct','Awarded USDA Funding?':'usda_fund'}, inplace=True)
digester_db.query("Status == 'Operational' and farm_type == 'Dairy'", inplace=True)


digester_db["usda_fund"].fillna("N", inplace=True)
digester_db.dropna(axis="rows", inplace=True)

methane_percow = pd.read_csv('em_percow.csv')
methane_percow['State'] = methane_percow['State'].map(us_state_abbrev)
methane_percow = methane_percow[['State','Dairy Cows']]
methane_percow.rename(columns={'Dairy Cows':'CH4/Cow'}, inplace=True)
methane_percow.set_index('State', inplace=True)
methane_percow['MTCO2e/Cow'] = methane_percow['CH4/Cow']*84/1000
methane_percow.drop(['CH4/Cow'],axis="columns", inplace=True)

merged = methane_percow.merge(digester_db, on='State', how='outer', validate='1:m', indicator=True)
merged.drop(['Status', 'farm_type', 'usda_fund','_merge'], axis="columns", inplace=True)
merged.dropna(axis="rows",inplace=True)
merged['total_em'] = merged['MTCO2e/Cow']*merged['num_cows']
merged['percent_reduct'] = round(merged['em_reduct']/merged['total_em']*100,1)
average_reduct = merged['percent_reduct'].sum()/len(merged['percent_reduct'])
print('\nAverage Reduction in Methane Emissions:',round(average_reduct,2), '%')

num_cows_digest = digester_db['num_cows'].sum()
print('\nTotal Number of Cows with Digester:',num_cows_digest,'thousand')

total_em_reduct = digester_db['em_reduct'].sum()
print('\nTotal Emissions Reductions from Digesters:',total_em_reduct,'MTCO2e/year')



