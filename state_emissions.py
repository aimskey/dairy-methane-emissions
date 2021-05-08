import pandas as pd
import matplotlib.pyplot as plt

us_state_abbrev = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
'Connecticut': 'CT', 'Delaware': 'DE', 'Distict of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'United States':'US'}

#Import csv file with all anaerobic digesters in the US
dtype_digester = {'State':str, 'Status':str, 'Animal/Farm Type(s)':str, 'Dairy':float, 'Total Emission Reductions(MTCO2e/yr)':float, 'Awarded USDA Funding?':str}
digester_db = pd.read_csv("agstar-livestock-ad-database.csv", dtype=dtype_digester)

#Editing header column to eliminate extra spaces
digester_db.columns = digester_db.columns.to_series().apply(lambda x: x.strip()) #found this line of code online after having problems with python not being able to read my data frame
digester_db = digester_db[["State", "Status", "Year Operational", "Animal/Farm Type(s)", "Dairy", "Total Emission Reductions (MTCO2e/yr)", "Awarded USDA Funding?"]]

#Changing column names. Note: it's important to remember the unit of measurement for total emissions (in thise case MTCO2e)
digester_db.rename(columns={'Year Operational':'year_operational','Animal/Farm Type(s)':'farm_type','Dairy':'num_cows','Total Emission Reductions (MTCO2e/yr)':'em_reduct','Awarded USDA Funding?':'usda_fund'}, inplace=True)

#Changing data types
digester_db["num_cows"] = digester_db["num_cows"].str.replace(",","").astype(float)
digester_db["em_reduct"] = digester_db["em_reduct"].str.replace(",","").astype(float)

#Isolating only the dairy farms that have operational anaerobic digesters
digester_db.query("Status == 'Operational' and farm_type == 'Dairy'", inplace=True)

#Replacing empty space with "N" to indicate which farms did no receive USDA funding
digester_db["usda_fund"].fillna("N", inplace=True)
digester_db.fillna(0, inplace=True)

#Pickle data frame for future use
digester_db.to_pickle('digester_db.pkl')

#Reading in file with number of cows per state (in thousands), including different ages
dtype_cownum = {'State':str,'Dairy Calves':float, 'Dairy Repl. Heif. 7-11 Months':float, 'Dairy Repl. Heif. 12-23 Months':float}
cow_num = pd.read_csv('cow_num_by_state_thou.csv', dtype = dtype_cownum)
cow_num["Dairy Cows"] = cow_num["Dairy Cows"].str.replace(",","").astype(float)

#Changing state names to abbreviations for future merge
cow_num["State"] = cow_num["State"].map(us_state_abbrev)

#Isolating only dairy animals. This spreadsheet includes beef as well for future analyses.
cow_num = cow_num[['State', 'Dairy Calves','Dairy Cows', 'Dairy Repl. Heif. 7-11 Months','Dairy Repl. Heif. 12-23 Months']]
cow_num.set_index('State', inplace=True)

#Creating one column for dairy heifer replacements in case I want them to be isolated in the future
cow_num['Replacements'] = cow_num['Dairy Repl. Heif. 7-11 Months'] + cow_num['Dairy Repl. Heif. 12-23 Months']
cow_num.drop(['Dairy Repl. Heif. 7-11 Months','Dairy Repl. Heif. 12-23 Months'], axis="columns", inplace=True)

#Creating a column with all of the animals summed
cow_num["total"] = cow_num.sum(axis="columns")

#Pickle the data frame to use in next script
cow_num.to_pickle("cow_num.pkl")


#Reading in file with state specific enteric fermentation methane emissions. Depending on feed, cows produce different levels of emissions which is captured on this csv file.
methane_ef = pd.read_csv('methane_em_ef_state_mt.csv')
methane_ef["Dairy Calves"] = methane_ef["Dairy Calves"].str.replace(",","").astype(float)
methane_ef["Dairy Cows"] = methane_ef["Dairy Cows"].str.replace(",","").astype(float)
methane_ef["Dairy Replacement Heifers 7-11 Months"] = methane_ef["Dairy Replacement Heifers 7-11 Months"].str.replace(",","").astype(float)
methane_ef["Dairy Replacement Heifers 12-23 Months"] = methane_ef["Dairy Replacement Heifers 12-23 Months"].str.replace(",","").astype(float)

#Isolating only the dairy cows. This spreadsheet includes 'dry' milk cattle and beef as well for future analyses
methane_ef = methane_ef[['State', 'Dairy Cows']]
methane_ef['State'] = methane_ef['State'].map(us_state_abbrev)
methane_ef.set_index('State', inplace=True)

#These emissions are in kgs/head (cow). For manure management comparison I need to put it into to kilotons.
methane_ef = methane_ef/1000

#This spreadsheet includes state specific manure management methane emissions. Because I'm interested in total emissions from the animals in a dairy operation, I want to  include both enteric fermentation and manure management emissions.
methane_mm = pd.read_csv('methane_em_mm_state_kt.csv')
methane_mm['State'] = methane_mm['State'].map(us_state_abbrev)
methane_mm = methane_mm[['State','Dairy Cattl']]
methane_mm.set_index('State', inplace=True)
methane_mm.rename(columns={'Dairy Cattl':'Manure Emissions'}, inplace=True)

#Merging the two datasets to see total emissions
total_methane = methane_ef.merge(methane_mm, on='State',
                                 how='outer', 
                                 validate ='1:1',
                                 indicator=True)
total_methane.drop(['_merge'], axis="columns", inplace=True)

#Pickle for future use
total_methane.to_pickle('total_methane.pkl')

#Total emissions
total_methane['total'] = total_methane.sum(axis="columns")

#Creating a totals variable to see total methane emissions from dairy animals.
us_total = round(total_methane['total'].sum(),2)
print('\nTotal Methane Emissions from US Dairy Cows in 2019:',us_total, 'kilotons')

#When looking at greenhouse gases, the unit of comparison is metric tons of carbon dioxide equivalent (MTCO2e)
#Convert kilotons to MTCO2e
#1kg of CH4(methane) is roughly equivalent to 84kgs of CO2. Here I muliply the kilotons by 1000 to get kgs, then multiply that by 84 to get KGCO2e, then divide by 1000 to get metric tons.
total_methane['converted_MTCO2e'] = total_methane['total']*1000*84/1000

#Pickling total_methane to use in future script
total_methane.to_pickle('total_methane.pkl')

#Create totals variable
converted_total = round(total_methane['converted_MTCO2e'].sum(),2)
print('\nTotal Methane Emissions from US Dairy Cows in 2019:',converted_total, 'MTCO2e')

























    
    








