# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 11:06:15 2021
##### ALLOWS to transform the JRC hydropower plant 
@author: geipel
"""

import pandas as pd
from nuts_finder import NutsFinder


# read JRC hydropower plant database https://github.com/energy-modelling-toolkit/hydro-power-database/tree/master/data
df = pd.read_csv('C:/Users/geipel/Downloads/hydro-power-database-master/hydro-power-database-master/data/jrc-hydro-power-plant-database.csv')
df.loc[:, 'NUTS3'] =0


#pip install NUTSFINDER

#RUN NUTSFINDER im schnelldurchgang mit vorgegebener niedriger Skalierung
nf = NutsFinder()
for row in range(0,4130):
    try:
        df.loc[row, 'NUTS3']=nf.find(lat=df.loc[row,'lat'], lon=df.loc[row,'lon'])[3]['NUTS_ID']
    except:
        print(range(row))
        pass

#SETZE NUTSfinder auf höhere Skalierung und lasse für nicht gefundene Werte erneut durchlaufen
nf = NutsFinder(year=2021, scale=60)
for row in range(0,4130):
    try:
        if df.loc[row, 'NUTS3']==0:    
            df.loc[row, 'NUTS3']=nf.find(lat=df.loc[row,'lat'], lon=df.loc[row,'lon'])[3]['NUTS_ID']
    except:
        print(range(row))
        pass
#Setze für Kosovo und Bosnien Herzegovina die NUTScode auf country Code.
find_BA_emptyNUTS3=df.query('country_code ==  "BA"').index
df.loc[find_BA_emptyNUTS3,'NUTS3']="BA"

find_BA_emptyNUTS3=df.query('country_code ==  "XK"').index
df.loc[find_BA_emptyNUTS3,'NUTS3']="XK"

#Checke manuell nach fehlenden einträgen: zunächst suche die Indizes und gucke dann per GOOGLE nach dem entsprechenden Gebiet: Hier nur für ein Kraftwerk im Grenzgebiet zur Ukraine relevant. 
find_emptyNUTS3=df.query('NUTS3 ==  0').index
df.loc[141,'NUTS3']="RO212"

#Entferne überflüssige Spalten
df=df.drop(columns=['pypsa_id', 'GEO', 'WRI'])
df['NUTS3'] = df['NUTS3'].astype(str)


#Gruppieren nach NUTS3
hydrpernuts3 = df.copy()
hydrpernuts3 = hydrpernuts3.groupby(['NUTS3'])['installed_capacity_MW'].sum().reset_index()

## Export to excel
df.to_excel('HYDRO_NUTS3.xlsx')
hydrpernuts3.to_excel('hydrpernuts3.xlsx')
