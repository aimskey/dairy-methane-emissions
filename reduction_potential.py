import pandas as pd

dtype_digester = {'State':str, 'Status':str, 'Animal/Farm Type(s)':str, 'Dairy':float, 'Total Emission Reductions(MTCO2e/yr)':float, 'Awarded USDA Funding?':str}
digester_db = pd.read_csv("agstar-livestock-ad-database.csv", dtype=dtype_digester)
digester_db.columns = digester_db.columns.to_series().apply(lambda x: x.strip())
digester_db = digester_db[["State", "Status", "Animal/Farm Type(s)", "Dairy", "Total Emission Reductions (MTCO2e/yr)", "Awarded USDA Funding?"]]
digester_db.rename(columns={'Animal/Farm Type(s)':'farm_type','Dairy':'num_cows','Total Emission Reductions (MTCO2e/yr)':'em_reduct','Awarded USDA Funding?':'usda_fund'}, inplace=True)
digester_db.query("Status == 'Operational' and farm_type == 'Dairy'", inplace=True)

digester_db["usda_fund"].fillna("N", inplace=True)
digester_db.dropna(axis="rows", inplace=True)

num_cows_digest = digester_db['num_cows'].sum()
print(num_cows_digest)

total_em_reduct = digester_db['em_reduct'].sum()
print(total_em_reduct)


