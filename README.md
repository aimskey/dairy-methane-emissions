# dairy-methane-emissions
An analysis of US Dairy Farms and their methane emissions and the potential impact of anaerobic digesters (AD)

This analysis looks at total US dairy cow methane emissions, current anaerobic digesters in the US, and existing
state policies that offer incentives to encourage farms to build anaerobic digesters. It focuses on New York
State and pulls census data about the county size, population, and income.

I wanted to know whether or not the existence of anaerobic digesters made an impact on dairy emissions in the US.
After analyzing their potential impact, I was interested in their current existence, whether policy incentives impacted
their being built, and where to target future building of digesters.

Data:

State Agricultural Emissions Data:
Inventory of US Greenhouse Gas Emissions and Sinks: 1990-2019
https://www.epa.gov/sites/production/files/2021-04/documents/us-ghg-inventory-2021-annex-3-additional-source-or-sink-categories-part-b.pdf

Livestock Anaerobic Digester Database:
https://www.epa.gov/agstar/livestock-anaerobic-digester-database

Cow Inventory by State:
https://www.nass.usda.gov/Publications/AgCensus/2017/Full_Report/Volume_1,_Chapter_1_State_Level/New_York/

New York County Cows Inventory:
https://www.nass.usda.gov/Publications/AgCensus/2017/Full_Report/Volume_1,_Chapter_2_County_Level/New_York/st36_2_0011_0011.pdf

State AD Incentive Programs:
https://openei.org/wiki/List_of_Anaerobic_Digestion_Incentives

Process:
Scripts should be run in this order:
1. state_emissions.py
2. reduction_potential.py
3. policy_impact.py
4. analyze_digester.py
5. emissions_map.py

