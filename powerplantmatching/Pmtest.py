# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 11:31:48 2020

@author: geipel
"""

import pandas as pd
import powerplantmatching as pm
wepp        = pm.data.WEPP()
geo         = pm.data.GEO()
entsoe      = pm.data.ENTSOE()
carma       = pm.data.CARMA()
gpd         = pm.data.GPD()
opsd        = pm.data.OPSD()
df1         = pm.powerplants(reduced = True, from_url=False, update=True)

capacity_per_fuel_matched=round(df1.groupby('Fueltype').Capacity.sum()/1000,0)
#df1=pm.heuristics.fill_missing_commyears(df1)
#df1=pm.heuristics.fill_missing_decommyears(df1)
#df1=pm.heuristics.remove_oversea_areas(df1)
#df1=pm.heuristics.rescale_capacities_to_country_totals(df1)
#df=pm.powerplants(reduced = True, from_url=False, update=True)
#pm.collection.matched_data(update=True, use_saved_aggregation=False, use_saved_matches=False)
print(round(pm.data.CARMA().groupby('Fueltype').Capacity.sum()/1000,0))





# %%% COMPARISON AUTOPRODUCERS WEPP/FULL
''' requires manual change of the WEPP database: drop autoproducers [ELECTYPE != A] and run matching. Save matched dataframe with autoproducers
'''
#sdef autoproducer_analysis(df_without_autoproducer, df_with_autoprod): 
# df_with_autoprod.drop(columns=['Scaled Capacity'])        ## if scaled capacity
# df_without_autoprod.drop(columns=['Scaled Capacity'])

# df_with_autoprod=df_with_autoprod.drop(columns=['Duration', 'Volume_Mm3', 'DamHeight_m', 'Retrofit', 'lat', 'lon', 'projectID'])
# df_without_autoprod=df_without_autoprod.drop(columns=['Duration', 'Volume_Mm3', 'DamHeight_m', 'Retrofit', 'lat', 'lon', 'projectID'])

## %%Find Rows in DF1 Which Are Not Available in DF2 
#merged_w = df_with_autoprod.merge(df_without_autoprod, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='left_only']

## %%Find Rows in DF1 Which Are Not Available in DF2 
#merged_wo = df_without_autoprod.merge(df_with_autoprod, how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='right_only']
## %%Check If Columns of Two Dataframes Are Exactly Same 
#pd.concat([df_with_autoprod,df_without_autoprod]).drop_duplicates(keep=False)



## %% Find Rows in DF2 Which Are Not Available in DF1 
#pm.gather_fueltype_info(wepp)
#pm.gather_fueltype_info(opsd)
#chp=wepp.query('Set == "CHP"')

#return df_with_autoprod



#dfw=pm.data.WEPP()
# %%% Other plottypües
#fig, ax = pm.plot.powerplant_map(df)
#pm.plot.fueltype_stats(df)
#fig,  ax = pm.plot.fueltype_and_country_totals_bar(df)
#pm.plot.fueltype_totals_bar(df)
#pm.plot.country_totals_hbar(df)
#pm.plot.factor_comparison(df)

