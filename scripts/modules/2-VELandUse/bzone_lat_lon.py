# -*- coding: utf-8 -*-
"""
Prepare bzone_lat_lon.csv (VE input)

@author: jyen
"""

import os
import re
import pandas as pd
from utilities.get_gis_layer import get_gis_lyr

# Set workspace to current script directory
os.chdir(os.path.dirname(os.path.abspath('__file__')))

# Get TAZ (Bzone) layer
taz_ver = 13 #TODO: specify TAZ version
server = 'sql2014b8'
database = 'GeoDepot'
sql = ("SELECT [taz], [Shape].ToString() AS [geometry]"
        f" FROM [GeoDepot].[gis].[TAZ{taz_ver}]")
taz = get_gis_lyr(sql, server, database)

# Get TAZ centroid with GCS
taz = taz.to_crs("EPSG:4326")
taz['Latitude'] = taz.geometry.centroid.y
taz['Longitude'] = taz.geometry.centroid.x

# Load geography definition
geo = pd.read_csv(r"..\defs\geo.csv")
df = geo.merge(taz, left_on="Bzone", right_on="taz")

# Initialize ABM Scenario List
scenarioList = ['2016', '2035build'] # TODO: specify scenario year

for idx, scen in enumerate(scenarioList):
    #extract scenario year
    year = re.split(r'(\d+)', scen)[1]
    
    # initialize the output DataFrame
    if idx == 0:
        initDF = df.copy()
        initDF['Year'] = year
        initDF['Geo'] = df.Bzone
        initDF = initDF[['Geo','Year','Latitude', 'Longitude']]
        initDF = initDF.sort_values(['Geo']) # sort by Bzone
        resultList = [initDF]
    # append otehr DF from scenario years
    else:
        otherDF = initDF.copy()
        otherDF['Year'] = year # update scenario year
        resultList.append(otherDF)

# Export resultDF
resultDF = pd.concat(resultList)
resultDF.to_csv(r"..\output\bzone_lat_lon.csv", index=False)
        
