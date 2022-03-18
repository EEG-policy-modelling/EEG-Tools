"""
Created October 2021
@author: Franziska Schöniger

based on 
@author: Michael Pertl, 
michael@thesmartinsights.com

Query data from ENTSO-E transparency portal
------------------------------------------------------------------------------
DISCLAIMER: 
You may use the Code for any private or commercial purpose. However, you may not sell, 
sub-license, rent, lease, lend, assign or otherwise transfer, duplicate or otherwise 
reproduce, directly or indirectly, the Code in whole or in part. 

You acknowledge that the Code is provided “AS IS” and thesmartinsights.com expressly 
disclaims all warranties and conditions including, but not limited to, any implied 
warranties for suitability of the Code for a particular purpose, or any form of warranty 
that operation of the Code will be error-free.

You acknowledge that in no event shall thesmartinsights.com or any of its affiliates be 
liable for any damages arising out of the use of the Code or otherwise in connection with 
this agreement, including, without limitation, any direct, indirect special, incidental 
or consequential damages, whether any claim for such recovery is based on theories of 
contract, negligence, and even if thesmartinsights.com has knowledge of the possibility 
of potential loss or damage.
------------------------------------------------------------------------------- 

Detailed information: https://github.com/EnergieID/entsoe-py

The Pandas Client works similar to the Raw Client, with extras:

    Time periods that span more than 1 year are automatically dealt with
    Requests of large numbers of files are split over multiple API calls

Please note that this client requires you to specifically set a start= and end= parameter which should be a pandas timestamp with timezone. If not it will throw an exception

from entsoe import EntsoePandasClient
import pandas as pd

client = EntsoePandasClient(api_key=<YOUR API KEY>)

start = pd.Timestamp('20171201', tz='Europe/Brussels')
end = pd.Timestamp('20180101', tz='Europe/Brussels')
country_code = 'BE'  # Belgium
country_code_from = 'FR'  # France
country_code_to = 'DE_LU' # Germany-Luxembourg
type_marketagreement_type = 'A01'
contract_marketagreement_type = "A01"

# methods that return Pandas Series
client.query_day_ahead_prices(country_code, start=start,end=end)
client.query_net_position(country_code, start=start, end=end, dayahead=True)
client.query_crossborder_flows(country_code_from, country_code_to, start, end)
client.query_scheduled_exchanges(country_code_from, country_code_to, start, end, dayahead=False)
client.query_net_transfer_capacity_dayahead(country_code_from, country_code_to, start, end)
client.query_net_transfer_capacity_weekahead(country_code_from, country_code_to, start, end)
client.query_net_transfer_capacity_monthahead(country_code_from, country_code_to, start, end)
client.query_net_transfer_capacity_yearahead(country_code_from, country_code_to, start, end)
client.query_intraday_offered_capacity(country_code_from, country_code_to, start, end,implicit=True)
client.query_offered_capacity(country_code_from, country_code_to, start, end, contract_marketagreement_type, implicit=True)

# methods that return Pandas DataFrames
client.query_load(country_code, start=start,end=end)
client.query_load_forecast(country_code, start=start,end=end)
client.query_load_and_forecast(country_code, start=start, end=end)
client.query_generation_forecast(country_code, start=start,end=end)
client.query_wind_and_solar_forecast(country_code, start=start,end=end, psr_type=None)
client.query_generation(country_code, start=start,end=end, psr_type=None)
client.query_generation_per_plant(country_code, start=start,end=end, psr_type=None)
client.query_installed_generation_capacity(country_code, start=start,end=end, psr_type=None)
client.query_installed_generation_capacity_per_unit(country_code, start=start,end=end, psr_type=None)
client.query_imbalance_prices(country_code, start=start,end=end, psr_type=None)
client.query_contracted_reserve_prices(country_code, start, end, type_marketagreement_type, psr_type=None)
client.query_contracted_reserve_amount(country_code, start, end, type_marketagreement_type, psr_type=None)
client.query_unavailability_of_generation_units(country_code, start=start,end=end, docstatus=None, periodstartupdate=None, periodendupdate=None)
client.query_unavailability_of_production_units(country_code, start, end, docstatus=None, periodstartupdate=None, periodendupdate=None)
client.query_unavailability_transmission(country_code_from, country_code_to, start, end, docstatus=None, periodstartupdate=None, periodendupdate=None)
client.query_withdrawn_unavailability_of_generation_units(country_code, start, end)
client.query_import(country_code, start, end)
client.query_generation_import(country_code, start, end)
client.query_procured_balancing_capacity(country_code, start, end, process_type, type_marketagreement_type=None)

Mappings

These lists are always evolving, so let us know if something's inaccurate!
Domains

DOMAIN_MAPPINGS = {
    'AL': '10YAL-KESH-----5',
    'AT': '10YAT-APG------L',
    'BA': '10YBA-JPCC-----D',
    'BE': '10YBE----------2',
    'BG': '10YCA-BULGARIA-R',
    'BY': '10Y1001A1001A51S',
    'CH': '10YCH-SWISSGRIDZ',
    'CZ': '10YCZ-CEPS-----N',
    'DE': '10Y1001A1001A83F',
    'DK': '10Y1001A1001A65H',
    'EE': '10Y1001A1001A39I',
    'ES': '10YES-REE------0',
    'FI': '10YFI-1--------U',
    'FR': '10YFR-RTE------C',
    'GB': '10YGB----------A',
    'GB_NIR': '10Y1001A1001A016',
    'GR': '10YGR-HTSO-----Y',
    'HR': '10YHR-HEP------M',
    'HU': '10YHU-MAVIR----U',
    'IE': '10YIE-1001A00010',
    'IT': '10YIT-GRTN-----B',
    'LT': '10YLT-1001A0008Q',
    'LU': '10YLU-CEGEDEL-NQ',
    'LV': '10YLV-1001A00074',
    # 'MD': 'MD',
    'ME': '10YCS-CG-TSO---S',
    'MK': '10YMK-MEPSO----8',
    'MT': '10Y1001A1001A93C',
    'NL': '10YNL----------L',
    'NO': '10YNO-0--------C',
    'PL': '10YPL-AREA-----S',
    'PT': '10YPT-REN------W',
    'RO': '10YRO-TEL------P',
    'RS': '10YCS-SERBIATSOV',
    'RU': '10Y1001A1001A49F',
    'RU_KGD': '10Y1001A1001A50U',
    'SE': '10YSE-1--------K',
    'SI': '10YSI-ELES-----O',
    'SK': '10YSK-SEPS-----K',
    'TR': '10YTR-TEIAS----W',
    'UA': '10YUA-WEPS-----0',
    'DE_AT_LU': '10Y1001A1001A63L',
    'DE_LU':'10Y1001A1001A82H',
}

Bidding Zones

BIDDING_ZONES = DOMAIN_MAPPINGS.copy()
BIDDING_ZONES.update({
    'DE': '10Y1001A1001A63L',  # DE-AT-LU
    'LU': '10Y1001A1001A63L',  # DE-AT-LU
    'IT_NORD': '10Y1001A1001A73I',
    'IT_CNOR': '10Y1001A1001A70O',
    'IT_CSUD': '10Y1001A1001A71M',
    'IT_SUD': '10Y1001A1001A788',
    'IT_FOGN': '10Y1001A1001A72K',
    'IT_ROSN': '10Y1001A1001A77A',
    'IT_BRNN': '10Y1001A1001A699',
    'IT_PRGP': '10Y1001A1001A76C',
    'IT_SARD': '10Y1001A1001A74G',
    'IT_SICI': '10Y1001A1001A75E',
    'IT_CALA': '10Y1001C--00096J',
    'NO_1': '10YNO-1--------2',
    'NO_2': '10YNO-2--------T',
    'NO_3': '10YNO-3--------J',
    'NO_4': '10YNO-4--------9',
    'NO_5': '10Y1001A1001A48H',
    'SE_1': '10Y1001A1001A44P',
    'SE_2': '10Y1001A1001A45N',
    'SE_3': '10Y1001A1001A46L',
    'SE_4': '10Y1001A1001A47J',
    'DK_1': '10YDK-1--------W',
    'DK_2': '10YDK-2--------M'
})

PSR-type

PSRTYPE_MAPPINGS = {
    'A03': 'Mixed',
    'A04': 'Generation',
    'A05': 'Load',
    'B01': 'Biomass',
    'B02': 'Fossil Brown coal/Lignite',
    'B03': 'Fossil Coal-derived gas',
    'B04': 'Fossil Gas',
    'B05': 'Fossil Hard coal',
    'B06': 'Fossil Oil',
    'B07': 'Fossil Oil shale',
    'B08': 'Fossil Peat',
    'B09': 'Geothermal',
    'B10': 'Hydro Pumped Storage',
    'B11': 'Hydro Run-of-river and poundage',
    'B12': 'Hydro Water Reservoir',
    'B13': 'Marine',
    'B14': 'Nuclear',
    'B15': 'Other renewable',
    'B16': 'Solar',
    'B17': 'Waste',
    'B18': 'Wind Offshore',
    'B19': 'Wind Onshore',
    'B20': 'Other',
    'B21': 'AC Link',
    'B22': 'DC Link',
    'B23': 'Substation',
    'B24': 'Transformer'}
"""

import pandas as pd
from entsoe import EntsoePandasClient, Area

pd.options.display.max_columns = None

#%% parameter definitions
client = EntsoePandasClient(api_key='')

start = pd.Timestamp('20151001', tz ='CET')
end = pd.Timestamp('20200101', tz ='CET')

BZ_list = ['AT']
# Done: 'ES','DK_1','DK_2', 'RO'
# Left out: 'DE_LU','AT'
#['IT_CNOR','IT_CSUD','IT_FOGN','IT_NORD','IT_PRGP','IT_ROSN','IT_SARD','IT_SICI','IT_SUD']
# PT',,'GB','IE_SEM','IT_BRNN'
#'IT_CALA'


for BZ in BZ_list:
# Get day-ahead prices from ENTSO-E Transparency
        print('Start installed capacities')
        print('Installed capacities in zone '+BZ)
        capacities =    client.query_installed_generation_capacity(BZ, start=start,end=end, psr_type=None)
        df_capacities = pd.DataFrame(capacities).reset_index()
        print('End capacities')
             
        df_capacities.to_csv('output/outfile_'+BZ+'.csv')
'''      

# Get day-ahead prices from ENTSO-E Transparency
        print('Start prices')
        print('Prices in zone '+BZ)
        DA_prices = client.query_day_ahead_prices(BZ, start=start,end=end)
        df_prices = pd.DataFrame(DA_prices).reset_index()
        df_prices.columns = ['Date/time', 'price_'+BZ]
        
        # correct daylight saving shifts: in fall, replace new hour by mean of two hours; in spring, use value of hour before
        
        DL_saving_28_Oct_18_1 = df_prices.iloc[650]['price_'+BZ]
        DL_saving_28_Oct_18_2 = df_prices.iloc[651]['price_'+BZ]
        DL_saving_28_Oct_18_new = (DL_saving_28_Oct_18_1+DL_saving_28_Oct_18_2)/2
        # replace price at index 650 and column 1 by mean of the two hours
        df_prices.iat[650, 1] = DL_saving_28_Oct_18_new
        
        DL_saving_27_Oct_19_1 = df_prices.iloc[9386]['price_'+BZ]
        DL_saving_27_Oct_19_2 = df_prices.iloc[9387]['price_'+BZ]
        DL_saving_27_Oct_19_new = (DL_saving_27_Oct_19_1+DL_saving_27_Oct_19_2)/2
        # replace price at index 9386 and column 1 by mean of the two hours
        df_prices.iat[9386, 1] = DL_saving_27_Oct_19_new
        
        # insert value of hour 01:00-02:00 for virtual 02:00-03:00 in spring
        DL_saving_31_Mar_19_1 = df_prices.iloc[4346]['price_'+BZ]
        # Create new dataframe without time shift
        df_prices_new = df_prices.iloc[0:4347]
        df_prices_rest = df_prices.iloc[4347:10969]
        new_row = {'Date/time':'2019-03-31 02:00:00+01:00', 'price_'+BZ:DL_saving_31_Mar_19_1}
        df_prices_new = df_prices_new.append(new_row, ignore_index=True)
        df_prices_new = df_prices_new.append(df_prices_rest, ignore_index=True)
        print('End prices')
        
        
# Get day-ahead load from ENTSO-E Transparency
        print('Start load')
        print('Load in zone '+BZ)
        DA_load = client.query_load_forecast(BZ, start=start,end=end)
        df_load = pd.DataFrame(DA_load).reset_index()
        df_load.columns = ['Date/time', 'load_'+BZ]
        
        # correct daylight saving shifts: in fall, replace new hour by mean of two hours; in spring, use value of hour before
        
        DL_saving_28_Oct_18_1 = df_load.iloc[650]['load_'+BZ]
        DL_saving_28_Oct_18_2 = df_load.iloc[651]['load_'+BZ]
        DL_saving_28_Oct_18_new = (DL_saving_28_Oct_18_1+DL_saving_28_Oct_18_2)/2
        # replace price at index 650 and column 1 by mean of the two hours
        df_load.iat[650, 1] = DL_saving_28_Oct_18_new
        
        DL_saving_27_Oct_19_1 = df_load.iloc[9386]['load_'+BZ]
        DL_saving_27_Oct_19_2 = df_load.iloc[9387]['load_'+BZ]
        DL_saving_27_Oct_19_new = (DL_saving_27_Oct_19_1+DL_saving_27_Oct_19_2)/2
        # replace price at index 9386 and column 1 by mean of the two hours
        df_load.iat[9386, 1] = DL_saving_27_Oct_19_new
        
        # insert value of hour 01:00-02:00 for virtual 02:00-03:00 in spring
        DL_saving_31_Mar_19_1 = df_load.iloc[4346]['load_'+BZ]
        # Create new dataframe without time shift
        df_load_new = df_load.iloc[0:4347]
        df_load_rest = df_load.iloc[4347:10969]
        new_row = {'Date/time':'2019-03-31 02:00:00+01:00', 'load_'+BZ:DL_saving_31_Mar_19_1}
        df_load_new = df_load_new.append(new_row, ignore_index=True)
        df_load_new = df_load_new.append(df_load_rest, ignore_index=True)
        print('End load')
        
        
# Get day-ahead wind onshore forecast from ENTSO-E Transparency
        print('Start wind onshore forecast')
        print('Wind onshore in zone '+BZ)
        DA_wind_onshore = client.query_wind_and_solar_forecast(BZ, start=start,end=end, psr_type='B19', process_type = 'A01')
        df_wind_ons = pd.DataFrame(DA_wind_onshore).reset_index()
        df_wind_ons.columns = ['Date/time', 'wind_ons_'+BZ]
        
        # correct daylight saving shifts: in fall, replace new hour by mean of two hours; in spring, use value of hour before
        
        DL_saving_28_Oct_18_1 = df_wind_ons.iloc[650]['wind_ons_'+BZ]
        DL_saving_28_Oct_18_2 = df_wind_ons.iloc[651]['wind_ons_'+BZ]
        DL_saving_28_Oct_18_new = (DL_saving_28_Oct_18_1+DL_saving_28_Oct_18_2)/2
        # replace price at index 650 and column 1 by mean of the two hours
        df_wind_ons.iat[650, 1] = DL_saving_28_Oct_18_new
        
        DL_saving_27_Oct_19_1 = df_wind_ons.iloc[9386]['wind_ons_'+BZ]
        DL_saving_27_Oct_19_2 = df_wind_ons.iloc[9387]['wind_ons_'+BZ]
        DL_saving_27_Oct_19_new = (DL_saving_27_Oct_19_1+DL_saving_27_Oct_19_2)/2
        # replace price at index 9386 and column 1 by mean of the two hours
        df_wind_ons.iat[9386, 1] = DL_saving_27_Oct_19_new
        
        # insert value of hour 01:00-02:00 for virtual 02:00-03:00 in spring
        DL_saving_31_Mar_19_1 = df_wind_ons.iloc[4346]['wind_ons_'+BZ]
        # Create new dataframe without time shift
        df_wind_ons_new = df_wind_ons.iloc[0:4347]
        df_wind_ons_rest = df_wind_ons.iloc[4347:10969]
        new_row = {'Date/time':'2019-03-31 02:00:00+01:00', 'wind_ons_'+BZ:DL_saving_31_Mar_19_1}
        df_wind_ons_new = df_wind_ons_new.append(new_row, ignore_index=True)
        df_wind_ons_new = df_wind_ons_new.append(df_wind_ons_rest, ignore_index=True)
        print('End wind onshore forecast') 

      
# Get day-ahead solar forecast from ENTSO-E Transparency
        print('Start solar forecast')
        print('Solar in zone '+BZ)
        DA_solar = client.query_wind_and_solar_forecast(BZ, start=start,end=end, psr_type='B16', process_type = 'A01')
        df_solar = pd.DataFrame(DA_solar).reset_index()
        df_solar.columns = ['Date/time', 'solar_'+BZ]
        
        # correct daylight saving shifts: in fall, replace new hour by mean of two hours; in spring, use value of hour before
        
        DL_saving_28_Oct_18_1 = df_solar.iloc[650]['solar_'+BZ]
        DL_saving_28_Oct_18_2 = df_solar.iloc[651]['solar_'+BZ]
        DL_saving_28_Oct_18_new = (DL_saving_28_Oct_18_1+DL_saving_28_Oct_18_2)/2
        # replace price at index 650 and column 1 by mean of the two hours
        df_solar.iat[650, 1] = DL_saving_28_Oct_18_new
        
        DL_saving_27_Oct_19_1 = df_solar.iloc[9386]['solar_'+BZ]
        DL_saving_27_Oct_19_2 = df_solar.iloc[9387]['solar_'+BZ]
        DL_saving_27_Oct_19_new = (DL_saving_27_Oct_19_1+DL_saving_27_Oct_19_2)/2
        # replace price at index 9386 and column 1 by mean of the two hours
        df_solar.iat[9386, 1] = DL_saving_27_Oct_19_new
        
        # insert value of hour 01:00-02:00 for virtual 02:00-03:00 in spring
        DL_saving_31_Mar_19_1 = df_solar.iloc[4346]['solar_'+BZ]
        # Create new dataframe without time shift
        df_solar_new = df_solar.iloc[0:4347]
        df_solar_rest = df_solar.iloc[4347:10969]
        new_row = {'Date/time':'2019-03-31 02:00:00+01:00', 'solar_'+BZ:DL_saving_31_Mar_19_1}
        df_solar_new = df_solar_new.append(new_row, ignore_index=True)
        df_solar_new = df_solar_new.append(df_solar_rest, ignore_index=True)
        print('End solar forecast')
# Get day-ahead wind offshore forecast from ENTSO-E Transparency
        print('Start wind offshore forecast')
        print('Wind offshore in zone '+BZ)
        DA_wind_offshore = client.query_wind_and_solar_forecast(BZ, start=start,end=end, psr_type='B18', process_type = 'A01')
        df_wind_offs = pd.DataFrame(DA_wind_offshore).reset_index()
        df_wind_offs.columns = ['Date/time', 'wind_offs_'+BZ]
        
        # correct daylight saving shifts: in fall, replace new hour by mean of two hours; in spring, use value of hour before
        
        DL_saving_28_Oct_18_1 = df_wind_offs.iloc[650]['wind_offs_'+BZ]
        DL_saving_28_Oct_18_2 = df_wind_offs.iloc[651]['wind_offs_'+BZ]
        DL_saving_28_Oct_18_new = (DL_saving_28_Oct_18_1+DL_saving_28_Oct_18_2)/2
        # replace price at index 650 and column 1 by mean of the two hours
        df_wind_offs.iat[650, 1] = DL_saving_28_Oct_18_new
        
        DL_saving_27_Oct_19_1 = df_wind_offs.iloc[9386]['wind_offs_'+BZ]
        DL_saving_27_Oct_19_2 = df_wind_offs.iloc[9387]['wind_offs_'+BZ]
        DL_saving_27_Oct_19_new = (DL_saving_27_Oct_19_1+DL_saving_27_Oct_19_2)/2
        # replace price at index 9386 and column 1 by mean of the two hours
        df_wind_offs.iat[9386, 1] = DL_saving_27_Oct_19_new
        
        # insert value of hour 01:00-02:00 for virtual 02:00-03:00 in spring
        DL_saving_31_Mar_19_1 = df_wind_offs.iloc[4346]['wind_offs_'+BZ]
        # Create new dataframe without time shift
        df_wind_offs_new = df_wind_offs.iloc[0:4347]
        df_wind_offs_rest = df_wind_offs.iloc[4347:10969]
        new_row = {'Date/time':'2019-03-31 02:00:00+01:00', 'wind_offs_'+BZ:DL_saving_31_Mar_19_1}
        df_wind_offs_new = df_wind_offs_new.append(new_row, ignore_index=True)
        df_wind_offs_new = df_wind_offs_new.append(df_wind_offs_rest, ignore_index=True)
        print('End wind offshore forecast')
        
# Create dataframe containing all data        
        print('Start summary')
        df_all = pd.DataFrame({'Date/time':df_prices_new['Date/time'],
                               'price'+BZ: df_prices_new['price_'+BZ],
                               #'load_'+BZ: df_load_new['load_'+BZ],
                               #'solar_'+BZ: df_solar_new['solar_'+BZ],
                               #'wind_offs_'+BZ: df_wind_offs_new['wind_offs_'+BZ],
                               #wind_ons_'+BZ: df_wind_ons_new['wind_ons_'+BZ]
                               })
        # remove double hours
        df_all = df_all.drop([651])
        df_all = df_all.drop([9388])
        print('End summary')
     
        file_name = 'output/data_2019_'+BZ+'.xlsx'
        print(df_all['Date/time'].dtypes)
        df_all['Date/time'] = df_all['Date/time'].astype(str)
        df_all.to_excel(file_name)
        print(df_all.head())
'''
           

       
    
   


