# -*- coding: utf-8 -*-
# Copyright 2016-2018 Fabian Hofmann (FIAS), Jonas Hoersch (KIT, IAI) and
# Fabian Gotzens (FZJ, IEK-STE)

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This export script is intented for the users of PyPSA:
#   https://www.pypsa.org/
# or the VEDA-TIMES modelling framework:
#   http://iea-etsap.org/index.php/etsap-tools/data-handling-shells/veda

from .core import _data_out, get_obj_if_Acc
from .heuristics import set_denmark_region_id, set_known_retire_years
import powerplantmatching as pm
import pandas as pd
import numpy as np
import pycountry
import logging
logger = logging.getLogger(__name__)
cget = pycountry.countries.get


def to_pypsa_names(df):
    """Rename the columns of the powerplant data according to the
    convention in PyPSA.
    Arguments:
        df {pandas.DataFrame} -- powerplant data
    Returns:
        pandas.DataFrame -- Column renamed dataframe
    """
    df = get_obj_if_Acc(df)
    return (df.assign(Fueltype=df['Fueltype'].str.lower())
              .rename(columns={'Fueltype': 'carrier',
                               'Capacity': 'p_nom',
                               'Duration': 'max_hours',
                               'Set': 'component'}))


def to_pypsa_network(df, network, buslist=None):
    """
    Export a powerplant dataframe to a pypsa.Network(), specify specific buses
    to allocate the plants (buslist).
    """
    df = get_obj_if_Acc(df)
    from scipy.spatial import cKDTree as KDTree
    substation_lv_i = network.buses.index[network.buses['substation_lv']]
    substation_lv_i = substation_lv_i.intersection(
            network.buses.reindex(buslist).index)
    kdtree = KDTree(network.buses.loc[substation_lv_i, ['x', 'y']].values)
    df = df.assign(bus=substation_lv_i[kdtree.query(df[['lon',
                                                        'lat']].values)[1]])
    df.Set.replace('CHP', 'PP', inplace=True)
    if 'Duration' in df:
        df['weighted_duration'] = df['Duration'] * df['Capacity']
        df = (df.groupby(['bus', 'Fueltype', 'Set'])
                .aggregate({'Capacity': sum,
                            'weighted_duration': sum}))
        df = df.assign(Duration=df['weighted_duration'] / df['Capacity'])
        df = df.drop(columns='weighted_duration')
    else:
        df = (df.groupby(['bus', 'Fueltype', 'Set'])
                .aggregate({'Capacity': sum}))
    df = df.reset_index()
    df = to_pypsa_names(df)
    df.index = df.bus + ' ' + df.carrier
    network.import_components_from_dataframe(df[df['component'] != 'Store'],
                                             'Generator')
    network.import_components_from_dataframe(df[df['component'] == 'Store'],
                                             'StorageUnit')
    
def to_Balmorel(df=None, use_scaled_capacity=True, baseyear=2017):
       
    if df is None:
        from .collection import matched_data
        df = matched_data()
        if df is None:
            raise RuntimeError("The data to be exported does not yet exist.")
    df=df1
    df = df.loc[(df.YearCommissioned.isnull()) |
                (df.YearCommissioned <= baseyear)]
    plausible = True
    df=pm.heuristics.fill_missing_commyears(df)
    df=pm.heuristics.remove_oversea_areas(df)
    if use_scaled_capacity: df=pm.heuristics.rescale_capacities_to_country_totals(df)



    # add column with technical lifetime
    if 'Life' not in df:
        pos = [i for i, x in enumerate(df.columns) if x == 'Retrofit'][0]
        df.insert(pos+1, 'Life', np.nan)
    df.loc[:, 'Life'] = df.Fueltype.map(pm.export.Balmorel_fueltype_to_life())
    if df.Life.isnull().any():
        raise ValueError("There are rows without a given lifetime in the "
                         "dataframe. Please check!")

    # add column with decommissioning year
    if 'YearRetire' not in df:
        pos = [i for i, x in enumerate(df.columns) if x == 'Life'][0]
        df.insert(pos+1, 'YearRetire', np.nan)
    df.loc[:, 'YearRetire'] = df.loc[:, 'Retrofit'] + df.loc[:, 'Life']
    df = pm.heuristics.set_known_retire_years(df)

    
    #solve natgas issues
    df=df.replace('CCGT, Thermal', 'CCGT')
    df.replace('', np.nan, inplace=True)
    
    # statistics for all countries
    NGas_tec                        = df[(df['Fueltype']=='Natural Gas') & (df['Technology'].notnull())].copy()
    NGas_tec                        = NGas_tec.groupby(['Set', 'Technology'])['Capacity'].sum().reset_index()
    NGas_tec_sum                    = df[(df['Fueltype']=='Natural Gas') & (df['Technology'].notnull())].copy()
    NGas_tec_sum                    = NGas_tec_sum.groupby(['Set'])['Capacity'].sum().reset_index()
    NGas_tec_sum.rename(columns={'Capacity': 'Capacity_sum'}, inplace=True)
    NGas_tec_stats = pd.merge(NGas_tec, NGas_tec_sum)
    NGas_tec_stats['percentage'] = NGas_tec_stats['Capacity']/NGas_tec_stats['Capacity_sum']
    
    # statistics for per country
    NGas_country_tec         = df[(df['Fueltype']=='Natural Gas') & (df['Technology'].notnull())].copy()
    NGas_country_tec         = NGas_country_tec.groupby(['Country', 'Set', 'Technology'])['Capacity'].sum().reset_index()
    NGas_country_tec_sum     = df[(df['Fueltype']=='Natural Gas') & (df['Technology'].notnull())].copy()
    NGas_country_tec_sum     = NGas_country_tec_sum.groupby(['Country', 'Set'])['Capacity'].sum().reset_index()
    NGas_country_tec_sum.rename(columns={'Capacity': 'Capacity_sum'}, inplace=True)
    NGas_country_tec_stats = pd.merge(NGas_country_tec, NGas_country_tec_sum)
    NGas_country_tec_stats['percentage']=NGas_country_tec_stats['Capacity']/NGas_country_tec_stats['Capacity_sum']
    
    # Add global stats for those countries with missing entries
    #for countries in df['Countries'].unique():
     #   for Sets in df['Sets'].unique():
      #      if NGas_country_tec_stats.loc['Country']

    
    
    NGas_country_tec_stats = NGas_country_tec_stats.drop(columns=['Capacity', 'Capacity_sum'])
    NGas_no_tec          = df[(df['Fueltype']=='Natural Gas') & (df['Technology'].isnull())].copy()  
    NGas_no_tec_OCGT     = NGas_no_tec.copy()
    NGas_no_tec_OCGT['Technology']='OCGT'
    NGas_no_tec_CCGT     = NGas_no_tec.copy()
    NGas_no_tec_CCGT['Technology']='CCGT'
    NGas_no_tec_ST     = NGas_no_tec.copy()
    NGas_no_tec_ST['Technology']='Steam Turbine'
    frames = [NGas_no_tec_OCGT, NGas_no_tec_CCGT, NGas_no_tec_ST]
    NGas_no_tec_all = pd.concat(frames)
    Capacity_summary_origin=NGas_no_tec.groupby(['Country'])['Capacity'].sum().reset_index()
    NGas_no_tec_all = pd.merge(
                  NGas_no_tec_all, 
                  NGas_country_tec_stats, 
                  on = ['Country','Technology', 'Set' ], 
                  how = 'left')
    NGas_no_tec_all = NGas_no_tec_all.dropna(subset=['percentage'])
    Capacity_summary_origin=df[(df['Fueltype']=='Natural Gas') & (df['Technology'].notnull())].groupby(['Country'])['Capacity'].sum().reset_index()
    NGas_no_tec_all['Capacity']= NGas_no_tec_all['Capacity']*NGas_no_tec_all['percentage']
    Capacity_summary_mod=NGas_no_tec_all.groupby(['Set', 'Country'])['Capacity'].sum().reset_index()
    NGas_no_tec_all=NGas_no_tec_all.drop(columns=['percentage'])
    df=df.loc[df['Technology'].notnull()]

    df=pd.concat([df, NGas_no_tec_all])
    df=df.reset_index()
    # Insert periodwise capacities
    #df.loc[:, baseyear] = df.loc[:, 'Capacity']
    for yr in range(baseyear, 2051, 1):
        #df.iloc[yr <= (df.loc[:, 'YearCommissioned'] + 60)] = df.loc[:, 'Capacity']
        df.loc[(yr <= (df['YearRetire'])),yr] = df['Capacity']
        df[yr].fillna(0)
        

    #drop columns not necessary for balmorel
    df2=df.drop(columns=['Duration', 'Volume_Mm3', 'DamHeight_m', 'lat', 'lon', 'projectID'])
    df2=df2.loc[~df['Fueltype'].isin(['Bioenergy','Waste', 'Oil'])]
    df2.replace('', np.nan, inplace=True)
    #groupby for number of combinations check
    df_combinations=df2.groupby(['Fueltype','Technology', 'Set']).size().reset_index().rename(columns={0:'count'})     
    
    
    
    # Initial grouping (basically a sorted version of df)
    PreGroupby_df = df.groupby(["Group 1","Group 2","Final Group"]).agg({'Numbers I want as percents': 'sum'}).reset_index()
# Get the sum of values for the "final group", append "_Sum" to it's column name, and change it into a dataframe (.reset_index)
    SumGroup_df = df.groupby(["Group 1","Group 2"]).agg({'Numbers I want as percents': 'sum'}).add_suffix('_Sum').reset_index()
# Merge the two dataframes
    Percents_df = pd.merge(PreGroupby_df, SumGroup_df)
# Divide the two columns
    Percents_df["Percent of Final Group"] = Percents_df["Numbers I want as percents"] / Percents_df["Numbers I want as percents_Sum"] * 100
# Drop the extra _Sum column
    Percents_df.drop(["Numbers I want as percents_Sum"], inplace=True, axis=1)
    
    
    
    df2=df2.replace('CCGT, Thermal', 'CCGT')
    
    
    NGas_country_tec         = df2[(df2['Fueltype']=='Natural Gas') & (df2['Technology'].notnull())].copy()
    NGas_country_tec         = NGas_country_tec.groupby(['Country', 'Set', 'Technology'])['Capacity'].sum().reset_index()
    NGas_country_tec_sum     = df2[(df2['Fueltype']=='Natural Gas') & (df2['Technology'].notnull())].copy()
    NGas_country_tec_sum      =NGas_country_tec_sum.groupby(['Country', 'Set'])['Capacity'].sum().reset_index()
    NGas_country_tec_sum.rename(columns={'Capacity': 'Capacity_sum'}, inplace=True)
    NGas_country_tec_stats = pd.merge(NGas_country_tec, NGas_country_tec_sum)
    NGas_country_tec_stats['percentage']=NGas_country_tec_stats['Capacity']/NGas_country_tec_stats['Capacity_sum']
    
    NGas_country_tec_sum     = df2[(df2['Fueltype']=='Natural Gas') & (df2['Technology'].notnull())].copy()
    NGas_country_tec_sum      =NGas_country_tec_sum.groupby(['Country', 'Set'])['Capacity'].sum().reset_index()
    NGas_country_tec_sum.rename(columns={'Capacity': 'Capacity_sum'}, inplace=True)
    NGas_country_tec_stats = pd.merge(NGas_country_tec, NGas_country_tec_sum)
    NGas_country_tec_stats['percentage']=NGas_country_tec_stats['Capacity']/NGas_country_tec_stats['Capacity_sum']
    
    
    
    
    NGas_country_tec_stats = NGas_country_tec_stats.drop(columns=['Capacity', 'Capacity_sum'])
    
    NGas_no_tec          = df2[(df2['Fueltype']=='Natural Gas') & (df2['Technology'].isnull())].copy()  
    NGas_no_tec_OCGT     = NGas_no_tec.copy()
    NGas_no_tec_OCGT['Technology']='OCGT'
    NGas_no_tec_CCGT     = NGas_no_tec.copy()
    NGas_no_tec_CCGT['Technology']='CCGT'
    NGas_no_tec_ST     = NGas_no_tec.copy()
    NGas_no_tec_ST['Technology']='Steam Turbine'
    
    frames = [NGas_no_tec_OCGT, NGas_no_tec_CCGT, NGas_no_tec_ST]
    NGas_no_tec_all = pd.concat(frames)
    Capacity_summary_origin=NGas_no_tec.groupby(['Country'])['Capacity'].sum().reset_index()
    NGas_no_tec_all = pd.merge(
                  NGas_no_tec_all, 
                  NGas_country_tec_stats, 
                  on = ['Country','Technology', 'Set' ], 
                  how = 'left')
    NGas_no_tec_all = NGas_no_tec_all.dropna(subset=['percentage'])
    Capacity_summary_origin=df2[(df2['Fueltype']=='Natural Gas') & (df2['Technology'].notnull())].groupby(['Country'])['Capacity'].sum().reset_index()

    NGas_no_tec_all['Capacity']= NGas_no_tec_all['Capacity']*NGas_no_tec_all['percentage']
    Capacity_summary_mod=NGas_no_tec_all.groupby(['Set', 'Country'])['Capacity'].sum().reset_index()
    

    
    ### Exkurs eigentlich hier besser mit dictionaries arbeiten
    #for name in companies:
    #    d[name] = pd.DataFrame()
    #    
    #    (f'NGas_country_no_tec_ratio_{natset}').DataFrame()=NGas_country_no_tec_stats[(NGas_country_no_tec_stats['Set']==natset)].copy()
        
    
    rangestep = 5
    class_number = 5
    countrylist = df2.Country.unique()
    for yr in range(1890, 2020, rangestep):
        for c in countrylist:
            #Hard Coal
            df2.loc[(df2['Technology'].isnull()) & (df2['Set'] == 'CHP') & (df2['Fueltype'] == 'Hard Coal') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_COAL_EXT_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'].isnull()) & (df2['Set'] == 'PP') & (df2['Fueltype'] == 'Hard Coal') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_COAL_CND_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'CCGT') & (df2['Set'] == 'CHP') & (df2['Fueltype'] == 'Hard Coal') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_COAL_EXT_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'CCGT') & (df2['Set'] == 'PP') & (df2['Fueltype'] == 'Hard Coal') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_COAL_CND_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'CCGT, Thermal') & (df2['Set'] == 'PP') & (df2['Fueltype'] == 'Hard Coal') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_COAL_CND_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'OCGT') & (df2['Set'] == 'CHP') & (df2['Fueltype'] == 'Hard Coal') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_COAL_EXT_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'Steam Turbine') & (df2['Set'] == 'PP') & (df2['Fueltype'] == 'Hard Coal') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_COAL_CND_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'Steam Turbine') & (df2['Set'] == 'CHP') & (df2['Fueltype'] == 'Hard Coal') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_COAL_EXT_Y-{yr}-{yr +rangestep-1}'
            
            #Lignite            
            df2.loc[(df2['Technology'] == 'Steam Turbine') & (df2['Set'] == 'PP') & (df2['Fueltype'] == 'Lignite') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_LIGN_CND_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'Steam Turbine') & (df2['Set'] == 'CHP') & (df2['Fueltype'] == 'Lignite') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_LIGN_EXT_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'].isnull()) & (df2['Set'] == 'CHP') & (df2['Fueltype'] == 'Lignite') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_LIGN_EXT_Y-{yr}-{yr +rangestep-1}'
            
            #Natural Gas
        
           # NGas_country_no_tec_stats_c_t=df2[(df2['Fueltype']=='Natural Gas') & (df2['Technology'].isnull()) & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep))].groupby(['Set'])['Capacity'].sum()
            #NGas_country_no_tec_ratio_c_t=df2[(df2['Fueltype']=='Natural Gas') & (df2['Technology'].isnull()) & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep))].groupby(['Set'])['Capacity'].sum()/df2[(df2['Fueltype']=='Natural Gas') & (df2['Technology'].isnull())].groupby(['Country'])['Capacity'].sum()
            
            
            #df_NGas_notec= df2.loc[(df2['Technology'].isnull()) & (df2['Fueltype'] == 'Natural Gas') & (df2['Country'] == c)]
            #df_NGas_notec_ocgt=df_NGas_notec.copy()
            #df_NGas_notec_ocgt.loc[:,'Technology']='OCGT'
            
           # df_NGas_notec_ST=df_NGas_notec.copy()
           # df_NGas_notec_ST.loc[:,'Technology']='Steam Turbine'
           # df_NGas_notec_ST.iloc[:,11:] = df_NGas_notec_ST.iloc[:,11:].mul(2)
    
            #df_NGas_notec_ccgt=df_NGas_notec.copy()
            #df_NGas_notec_ccgt.loc[:,'Technology']='CCGT'
            #df_NGas_notec_ccgt.iloc[:,11:] = df_NGas_notec_ccgt.iloc[:,11:].mul(2)
            
            
            
            #groupby(['Country', 'Fueltype'])['Capacity'].sum()
            #PP_ratio =
            #CHP_ratio
            #df2.loc[(df2['Technology'].isnull()) & (df2['Set'] == 'CHP') & (df2['Fueltype'] == 'Natural Gas') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_CC_NGAS_EXT_Y-{yr}-{yr +rangestep}'
            
            #xxsum['percentage']=xxsum/xxsum.groupby(['Country', 'Fueltype'])['Capacity'].sum()
            #xxsum['percentage']=xxsum['Capacity']/xxsum.groupby(['Country', 'Fueltype'])['Capacity'].transform('sum')
            
            
            
            df2.loc[(df2['Technology'] == 'CCGT') & (df2['Set'] == 'CHP') & (df2['Fueltype'] == 'Natural Gas') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_CC_NGAS_EXT_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'CCGT') & (df2['Set'] == 'PP') & (df2['Fueltype'] == 'Natural Gas') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_CC_NGAS_CND_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'CCGT, Thermal') & (df2['Set'] == 'PP') & (df2['Fueltype'] == 'Natural Gas') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_CC_NGAS_CND_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'OCGT') & (df2['Set'] == 'PP') & (df2['Fueltype'] == 'Natural Gas') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_GT_NGAS_EXT_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'OCGT') & (df2['Set'] == 'CHP') & (df2['Fueltype'] == 'Natural Gas') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_GT_NGAS_CND_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'Steam Turbine') & (df2['Set'] == 'PP') & (df2['Fueltype'] == 'Natural Gas') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_GT_NGAS_CND_Y-{yr}-{yr +rangestep-1}'
            df2.loc[(df2['Technology'] == 'Steam Turbine') & (df2['Set'] == 'CHP') & (df2['Fueltype'] == 'Natural Gas') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_ST_NGAS_EXT_Y-{yr}-{yr +rangestep-1}'
        
            #Nuclear
            df2.loc[(df2['Technology'] == 'Steam Turbine') & (df2['Set'] == 'PP') & (df2['Fueltype'] == 'Nuclear') & (df2['Country'] == c) & (df2['Retrofit'] >= yr) & (df2['Retrofit'] < (yr + rangestep)), 'Classification_name']=f'K{class_number}_GNR_ST_NUCL_CND_Y-{yr}-{yr +rangestep-1}'
        
        
    K5=df2.drop(columns=['Life', 'YearRetire','Retrofit'])
    K5=K5.drop(columns=['Name', 'Fueltype', 'Technology', 'Set', 'Capacity', 'YearCommissioned', 'Efficiency'])
    if 'Scaled Capacity' in df:
        K5=K5.drop(columns=['Scaled Capacity'])
    K5=K5.groupby(['Country','Classification_name',]).sum().reset_index()
    K5=K5.loc[(K5[baseyear] > 0)]

       
    if plausible:
        K5.to_excel(pm.core._data_out('Export_conv_PP_Balmorel.xlsx'))
        K5.to_csv(pm.core._data_out('Export_conv_PP_Balmorel.inc'), header=None, index=None, sep=' ', mode='a')
    return df_combinations, df2, K5

#df1=pm.heuristics.fill_missing_decommyears(df1)

def to_TIMES(df=None, use_scaled_capacity=False, baseyear=2015):
    """
    Transform a given dataset into the TIMES format and export as .xlsx.
    """
    if df is None:
        from .collection import matched_data
        df = matched_data()
        if df is None:
            raise RuntimeError("The data to be exported does not yet exist.")
    df = df.loc[(df.YearCommissioned.isnull()) |
                (df.YearCommissioned <= baseyear)]
    plausible = True

    # Set region via country names by iso3166-2 codes
    if 'Region' not in df:
        pos = [i for i, x in enumerate(df.columns) if x == 'Country'][0]
        df.insert(pos+1, 'Region', np.nan)
    df.Country = df.Country.replace({'Czech Republic': 'Czechia'})
    df.loc[:, 'Region'] = df.Country.apply(lambda c: cget(name=c).alpha_2)
    df = set_denmark_region_id(df)
    regions = sorted(set(df.Region))
    if None in regions:
        raise ValueError("There are rows without a valid country identifier "
                         "in the dataframe. Please check!")

    # add column with TIMES-specific type. The pattern is as follows:
    # 'ConELC-' + Set + '_' + Fueltype + '-' Technology
    df.loc[:, 'Technology'].fillna('', inplace=True)
    if 'TimesType' not in df:
        pos = [i for i, x in enumerate(df.columns) if x == 'Technology'][0]
        df.insert(pos+1, 'TimesType', np.nan)
    df.loc[:, 'TimesType'] = pd.Series('ConELC-' for _ in range(len(df))) +\
        np.where(df.loc[:, 'Set'].str.contains('CHP'), 'CHP', 'PP') +\
        '_' + df.loc[:, 'Fueltype'].map(fueltype_to_abbrev())
    df.loc[(df.Fueltype == 'Wind') &
           (df.Technology.str.contains('offshore', case=False)),
           'TimesType'] += 'F'
    df.loc[(df.Fueltype == 'Wind') &
           ~(df.Technology.str.contains('offshore', case=False)),
           'TimesType'] += 'N'
    df.loc[(df.Fueltype == 'Solar') &
           (df.Technology.str.contains('CSP', case=False)),
           'TimesType'] += 'CSP'
    df.loc[(df.Fueltype == 'Solar') &
           ~(df.Technology.str.contains('CSP', case=False)),
           'TimesType'] += 'SPV'
    df.loc[(df.Fueltype == 'Natural Gas') &
           (df.Technology.str.contains('CCGT', case=False)),
           'TimesType'] += '-CCGT'
    df.loc[(df.Fueltype == 'Natural Gas') &
           ~(df.Technology.str.contains('CCGT', case=False)) &
           (df.Technology.str.contains('OCGT', case=False)),
           'TimesType'] += '-OCGT'
    df.loc[(df.Fueltype == 'Natural Gas') &
           ~(df.Technology.str.contains('CCGT', case=False)) &
           ~(df['Technology'].str.contains('OCGT', case=False)),
           'TimesType'] += '-ST'
    df.loc[(df.Fueltype == 'Hydro') &
           (df.Technology.str.contains('pumped storage', case=False)),
           'TimesType'] += '-PST'
    df.loc[(df.Fueltype == 'Hydro') &
           (df.Technology.str.contains('run-of-river', case=False)) &
           ~(df.Technology.str.contains('pumped storage', case=False)),
           'TimesType'] += '-ROR'
    df.loc[(df.Fueltype == 'Hydro') &
           ~(df.Technology.str.contains('run-of-river', case=False)) &
           ~(df.Technology.str.contains('pumped storage', case=False)),
           'TimesType'] += '-STO'

    if None in set(df.TimesType):
        raise ValueError("There are rows without a valid TIMES-Type "
                         "identifier in the dataframe. Please check!")

    # add column with technical lifetime
    if 'Life' not in df:
        pos = [i for i, x in enumerate(df.columns) if x == 'Retrofit'][0]
        df.insert(pos+1, 'Life', np.nan)
    df.loc[:, 'Life'] = df.TimesType.map(timestype_to_life())
    if df.Life.isnull().any():
        raise ValueError("There are rows without a given lifetime in the "
                         "dataframe. Please check!")

    # add column with decommissioning year
    if 'YearRetire' not in df:
        pos = [i for i, x in enumerate(df.columns) if x == 'Life'][0]
        df.insert(pos+1, 'YearRetire', np.nan)
    df.loc[:, 'YearRetire'] = df.loc[:, 'Retrofit'] + df.loc[:, 'Life']
    df = set_known_retire_years(df)

    # Now create empty export dataframe with headers
    columns = ['Attribute', '*Unit', 'LimType', 'Year']
    columns.extend(regions)
    columns.append('Pset_Pn')

    # Loop stepwise through technologies, years and countries
    df_exp = pd.DataFrame(columns=columns)
    cap_column = 'Scaled Capacity' if use_scaled_capacity else 'Capacity'
    row = 0
    for tt, df_tt in df.groupby('TimesType'):
        for yr in range(baseyear, 2055, 5):
            df_exp.loc[row, 'Year'] = yr
            data_regions = df_tt.groupby('Region')
            for reg in regions:
                if reg in data_regions.groups:
                    ct_group = data_regions.get_group(reg)
                    # Here, all matched units existing in the dataset are being
                    # considered. This is needed since there can be units in
                    # the system which are actually already beyond their
                    # assumed technical lifetimes but still online in baseyear.
                    if yr == baseyear:
                        series = ct_group.apply(lambda x: x[cap_column],
                                                axis=1)
                    # Here all matched units that are not retired in yr,
                    # are being filtered.
                    elif yr > baseyear:
                        series = ct_group.apply(lambda x: x[cap_column]
                                                if yr >= x['YearCommissioned']
                                                and yr <= x['YearRetire']
                                                else 0, axis=1)
                    else:
                        message = 'loop yr({}) below baseyear({})'
                        raise ValueError(message.format(yr, baseyear))
                    # Divide the sum by 1000 (MW->GW) and write into export df
                    df_exp.loc[row, reg] = series.sum()/1000.0
                else:
                    df_exp.loc[row, reg] = 0.0
                # Plausibility-Check:
                if (yr > baseyear and (df_exp.loc[row, reg] >
                                       df_exp.loc[row-1, reg])):
                    plausible = False
                    logger.error("For region '{}' and timestype '{}' the value \
                                 for year {} ({0.000}) is higher than in the \
                                 year before ({0.000})."
                                 .format(reg, tt, yr, df_exp.loc[row, reg],
                                         df_exp.loc[row-1, reg]))
            df_exp.loc[row, 'Pset_Pn'] = tt
            row += 1
    df_exp.loc[:, 'Attribute'] = 'STOCK'
    df_exp.loc[:, '*Unit'] = 'GW'
    df_exp.loc[:, 'LimType'] = 'FX'

    # Write resulting dataframe to file
    if plausible:
        df_exp.to_excel(_data_out('Export_Stock_TIMES.xlsx'))
    return df_exp


def store_open_dataset():
    from .collection import matched_data, reduce_matched_dataframe
    m = (matched_data(reduced=False)
         .reindex(columns=['CARMA', 'ENTSOE', 'GEO', 'GPD', 'OPSD'], level=1)
         [lambda df: df.Name.notnull().any(1)])
    m.to_csv(_data_out('powerplants_large.csv'))
    m = m.pipe(reduce_matched_dataframe)
    m.to_csv(_data_out('powerplants.csv'))
    return m


def fueltype_to_abbrev():
    """
    Return the fueltype-specific abbreviation.
    """
    data = {'Bioenergy': 'BIO',
            'Geothermal': 'GEO',
            'Hard Coal': 'COA',
            'Hydro': 'HYD',
            'Lignite': 'LIG',
            'Natural Gas': 'NG',
            'Nuclear': 'NUC',
            'Oil': 'OIL',
            'Other': 'OTH',
            'Solar': '',  # DO NOT delete this entry!
            'Waste': 'WST',
            'Wind': 'WO'}
    return data

def Balmorel_fueltype_to_life():
    
    data = {'Natural Gas': 30,
            'Hard Coal': 40,
            'Lignite': 40,
            'Bioenergy': 35,
            'Nuclear': 60,
            'Oil': 40,
            'Waste': 35}
    
    return data

def timestype_to_life():
    """
    Returns the timestype-specific technical lifetime.
    """
    data = {'ConELC-PP_COA': 45,
            'ConELC-PP_LIG': 45,
            'ConELC-PP_NG-OCGT': 40,
            'ConELC-PP_NG-ST': 40,
            'ConELC-PP_NG-CCGT': 40,
            'ConELC-PP_OIL': 40,
            'ConELC-PP_NUC': 50,
            'ConELC-PP_BIO': 25,
            'ConELC-PP_HYD-ROR': 200,  # According to A.K. Riekkolas comment,
            'ConELC-PP_HYD-STO': 200,  # these will not retire after 75-100 a,
            'ConELC-PP_HYD-PST': 200,  # but exist way longer at retrofit costs
            'ConELC-PP_WON': 25,
            'ConELC-PP_WOF': 25,
            'ConELC-PP_SPV': 30,
            'ConELC-PP_CSP': 30,
            'ConELC-PP_WST': 30,
            'ConELC-PP_SYN': 5,
            'ConELC-PP_CAES': 40,
            'ConELC-PP_GEO': 30,
            'ConELC-PP_OTH': 5,
            'ConELC-CHP_COA': 45,
            'ConELC-CHP_LIG': 45,
            'ConELC-CHP_NG-OCGT': 40,
            'ConELC-CHP_NG-ST': 40,
            'ConELC-CHP_NG-CCGT': 40,
            'ConELC-CHP_OIL': 40,
            'ConELC-CHP_BIO': 25,
            'ConELC-CHP_WST': 30,
            'ConELC-CHP_SYN': 5,
            'ConELC-CHP_GEO': 30,
            'ConELC-CHP_OTH': 5,
            }
    return data
