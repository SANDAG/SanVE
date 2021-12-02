# -*- coding: utf-8 -*-
"""
xref MGRA and VE Marea

@author: jyen
"""

import os
import pandas as pd
import geopandas as gpd
from utilities.get_gis_layer import get_gis_lyr


# Set workspace to current script directory
os.chdir(os.path.dirname(os.path.abspath('__file__')))

# Load geography definition
geo = pd.read_csv(r"..\defs\geo.csv")

# Load mgra adn city layers from GeoDepot
mgraSQL = ("SELECT [mgra], [Shape].ToString() AS [geometry]"
           " FROM [GeoDepot].[gis].[MGRA13pt]")
citySQL = ("SELECT [City], [Shape].ToString() AS [geometry]"
           " FROM [GeoDepot].[gis].[Cities]")
mgraPOINT = get_gis_lyr(mgraSQL, 'sql2014b8', 'GeoDepot')
city = get_gis_lyr(citySQL, 'sql2014b8', 'GeoDepot')

# Build mgra-City xref table
resultDF = gpd.sjoin(mgraPOINT, city, how="left")
resultDF = resultDF.sort_values(['mgra'])

# Export xref table
resultDF[['mgra','City']].to_csv(r"..\output\mgra13_city_xref.csv", index=False)