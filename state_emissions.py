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

dtype_digester = {'State':str, 'Status':str, 'Animal/Farm Type(s)':str, 'Dairy':float, 'Total Emission Reductions(MTCO2e/yr':float, 'Awarded USDA Funding?':str}
digester_db = pd.read_csv("agstar-livestock-ad-database.csv", dtype=dtype_digester)
digester_db.columns = digester_db.columns.to_series().apply(lambda x: x.strip()) #found this line of code online after having problems with python not being able to read my data frame
digester_db = digester_db[["State", "Status", "Animal/Farm Type(s)", "Dairy", "Total Emission Reductions (MTCO2e/yr)", "Awarded USDA Funding?"]]
digester_db.rename(columns={'Animal/Farm Type(s)':'farm_type','Dairy':'num_cows','Total Emissions Reductions (MTCO2e/yr)':'em_reduct','Awarded USDA Funding?':'usda_fund'}, inplace=True)
digester_db.query("Status == 'Operational' and farm_type == 'Dairy'", inplace=True)

digester_db["usda_fund"].fillna("N", inplace=True)
digester_db.fillna(0, inplace=True)

dtype_cownum = {'State':str,'Dairy Calves':float, 'Dairy Repl. Heif. 7-11 Months':float, 'Dairy Repl. Heif. 12-23 Months':float}
cow_num = pd.read_csv('cow_num_by_state_thou.csv', dtype = dtype_cownum)
cow_num["Dairy Cows"] = cow_num["Dairy Cows"].str.replace(",","").astype(float)
cow_num["State"] = cow_num["State"].map(us_state_abbrev)
cow_num = cow_num[['State', 'Dairy Calves','Dairy Cows', 'Dairy Repl. Heif. 7-11 Months','Dairy Repl. Heif. 12-23 Months']]
cow_num.set_index('State', inplace=True)
cow_num['Replacements'] = cow_num['Dairy Repl. Heif. 7-11 Months'] + cow_num['Dairy Repl. Heif. 12-23 Months']
cow_num.drop(['Dairy Repl. Heif. 7-11 Months','Dairy Repl. Heif. 12-23 Months'], axis="columns", inplace=True)
cow_num["total"] = cow_num.sum(axis="columns")










    
    








