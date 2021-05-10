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

Findings:
The highest dairy emitters are both states with high cow numbers, and also states with high per/head emitters.
Cows emit different levels of methane based on their feed, suggesting that while these anaerobic digesters can 
have a significant impact on emissions, feed may be another important angle to address emissions. 

Based on the average reduction of emissions from existing ADs, the average reduction is 52.95%. 
This is significantly less than the reported reduction of up to 85%.
Per head emissions between states that have operational digeesters and those that don't are nearly identical.
Per head emissions varies greatly by state, and those with ADs have higher per head emissions from the start.
Farm size does seem to make a difference, digesters are much more common on large farms (>1000)

The existence of incentive programs rarely means the existence of digesters. Many states have some form of incentive
but that doesn't necessarily encourage a lot of digesters. Future research should be done on the quality of forms of
these incentives. The actual number of incentives doens't seem to make a large difference either. 

States with the highest emissions tend to have digesters in place, but that is not always true. Looking at the map
us_cont_emissions.png, Texas and New Mexico are relatively high emitters with no ADs. It's also important to note
that the existence of operational digesters does not specify how many. Future analysis could be done to see how many
are in each state and how many would be necessary to make a significant impact.

Isolating New York State, we can see highest density of cows/acre by looking at nys_cow_density.png. This map
indicates where ADs could have the biggest impact in NYS. nys_county_digesters shows where ADs are currently in place.










