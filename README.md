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

Cow Inventory by County (New York):
https://www.nass.usda.gov/Publications/AgCensus/2017/Full_Report/Volume_1,_Chapter_2_County_Level/New_York/st36_2_0011_0011.pdf

State Anaerobic Digester Incentive Programs:
https://openei.org/wiki/List_of_Anaerobic_Digestion_Incentives

Process:
Scripts should be run in this order:
1. state_emissions.py
2. reduction_potential.py
3. policy_impact.py
4. analyze_digester.py
5. emissions_map.py
6. county_cows.py

Findings:
Digesters effect on emissions:

Figure em_digest.png shows the emissions/head for states with and without digesters.
Emissions/Head/yr with Digesters: 23kg
Emissions/Head/yes without Digesters: 22kg

The highest dairy emitters are both states with high cow numbers and also states with high per head emitters.
Cows emit different levels of methane based on their feed, potentially suggesting that while these anaerobic digesters can 
have a significant impact on emissions, feed may be another important angle to address emissions. 

Based on the average reduction of emissions from existing ADs, the average reduction is 52.95%. 
This is significantly less than the reported reduction of up to 85%.

Figure farm_size.png shows the rate of digesters based on farm size.
Farm size does seem to make a difference, digesters are much more common on large farms (head > 2000)

Figure policyimpact.png shows that the existence of incentive programs does not necessariy lead to the existence
of digesters. Many states have some form of incentive but that doesn't necessarily encourage a lot of digesters. 
Future research should be done on the quality ofthese incentives. 
The actual number of incentive programs doesn't seem to make a large difference either. 

Figure us_cont_emissions.png shows that states with the highest emissions tend to have digesters in place. 
Exceptions are Texas and New Mexico, which are relatively high emitters with no ADs. It's also important to note
that the existence of operational digesters does not specify how many (but could with this data). Future analysis 
could be done to see how many are in each state and how many would be necessary to make a significant impact.

Isolating New York State

Figure nys_cow_density.png shows the density of cows across NYS counties. The highest density of cows are found in
midwest part of the state in Genesee, Livingston, Onondaga, Ontario, Wyoming, and Yates counties.

Figure pop_cow_density.png overlays population data, showing where the most people live and where the most cows
are located in NYS. If the greatest impact on climate change should be focused on where the most people live, the greatest
impact that ADs can have based on these data points are: Onondaga, Ontario, and Montgomery counties.

I also looked at median income with the assumption that climate change more adversely affects people in lower income
brackets. When I isolated the bottom 20% of median income and compared it to high cow density, the most advantageous
county for ADs is Yates county. 

Figure nys_county_digesters.png overlays the existence of digesters on the cow density data.

Based on the above analysis, NYS should focus its incentive programs for AD development in Cortland, Onondaga,
Tompkins, and Yates counties. It would also benefit from encouraging more ADs in Montgomery and Ontario counties.










