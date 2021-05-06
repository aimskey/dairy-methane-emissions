import pandas as pd
import matplotlib.pyplot as plt

abbrevs = pd.read_csv("state_abs.csv")
us_state_abbrev = {'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO',
'Connecticut': 'CT', 'Delaware': 'DE', 'Distict of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID',
'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA',
'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS',
'Missouri': 'MO', 'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ',
'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR', 'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA', 'Washington': 'WA',
'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY', 'United States':'US'}

state_incentives = pd.read_csv("list_state_incentives.csv")
state_incentives = state_incentives[["Place", "Incentive/Active"]]
state_incentives.rename(columns={"Place":"program_state", "Incentive/Active":"program_status"}, inplace=True)
state_incentives["program_state"] = state_incentives["program_state"].map(us_state_abbrev)

active_incentives = state_incentives[state_incentives["program_status"]]

dtype_digester = {'State':str, 'Status':str, 'Animal/Farm Type(s)':str, 'Dairy':float, 'Total Emission Reductions(MTCO2e/yr':float, 'Awarded USDA Funding?':str}
digester_db = pd.read_csv("agstar-livestock-ad-database.csv", dtype=dtype_digester)
digester_db.columns = digester_db.columns.to_series().apply(lambda x: x.strip()) #found this line of code online after having problems with python not being able to read my data frame
digester_db = digester_db[["State", "Status", "Animal/Farm Type(s)", "Dairy", "Total Emission Reductions (MTCO2e/yr)", "Awarded USDA Funding?"]]
digester_db.rename(columns={'Animal/Farm Type(s)':'farm_type','Dairy':'num_cows','Total Emissions Reductions (MTCO2e/yr)':'em_reduct','Awarded USDA Funding?':'usda_fund'}, inplace=True)
digester_db.query("Status == 'Operational' and farm_type == 'Dairy'", inplace=True)

digester_db["usda_fund"].fillna("N", inplace=True)
digester_db.fillna(0, inplace=True)

print("\nNumber of Incentive Programs for Each Participating State")
print(active_incentives["program_state"].value_counts())

print("\nNumber Anaerobic Digesters for Each State")
print(digester_db["State"].value_counts())

digester_db["States with Incentive"] = active_incentives["program_state"]


#CHANGE THIS SO IT'S PLOTTING VALUE COUNTS
plt.figure()
ax = digester_db.plot.scatter("State", "States with Incentive")
ax.set_title("Potential Impact of Incentive Programs")
ax.set_xlabel("Number of Anaerobic Digesters")
ax.set_ylabel("Number of Incentive Programs")
ax.figure.savefig("policyimpact.png", dpi=300)





    
    








