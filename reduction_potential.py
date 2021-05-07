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

#Importing spreadsheet that details where all anaerobic digesters are in the US
digester_db = pd.read_pickle('digester_db.pkl')

#Importing spreadsheet that details state specific enteric fermentation emissions per cow 
methane_percow = pd.read_csv('em_percow.csv')
methane_percow['State'] = methane_percow['State'].map(us_state_abbrev)
methane_percow = methane_percow[['State','Dairy Cows']]
methane_percow.rename(columns={'Dairy Cows':'CH4/Cow'}, inplace=True)
methane_percow.set_index('State', inplace=True)

#Converting kg/head into greenhouse gas unit of measurement - MTCO2e (metric tons carbon dioxide equivalent)
methane_percow['MTCO2e/Cow'] = methane_percow['CH4/Cow']*84/1000
methane_percow.drop(['CH4/Cow'],axis="columns", inplace=True)

#Merging two data frames to look total emissions and emissions reductions
merged = methane_percow.merge(digester_db, on='State', how='outer', validate='1:m', indicator=True)
merged.drop(['Status', 'farm_type', 'usda_fund','_merge'], axis="columns", inplace=True)
merged.dropna(axis="rows",inplace=True)

#Caluclating total emissions from farms with digesters
merged['total_em'] = merged['MTCO2e/Cow']*merged['num_cows']

#Calculating the estimated reduction percentage
merged['percent_reduct'] = round(merged['em_reduct']/merged['total_em']*100,1)

#Calculating an average reduction in methane emissions
average_reduct = merged['percent_reduct'].sum()/len(merged['percent_reduct'])
print('\nAverage Reduction in Methane Emissions:',round(average_reduct,2), '%')

num_cows_digest = digester_db['num_cows'].sum()
print('\nTotal Number of Cows with Digester:',num_cows_digest,'thousand')

total_em_reduct = digester_db['em_reduct'].sum()
print('\nTotal Emissions Reductions from Digesters:',total_em_reduct,'MTCO2e/year')



