# -*- coding: utf-8 -*-
"""
xref Marea-specific MGRA and VE Marea

@author: jyen
"""

import os
import pyodbc
import pandas as pd
import geopandas as gpd
from shapely import wkt

# Set workspace to current script directory
os.chdir(os.path.dirname(os.path.abspath('__file__')))

# Load geography definition
geo = pd.read_csv(r"..\defs\geo.csv")

# Load the MGRA from SQL as a Pandas DataFrame
def get_gis_layer(sql):
    # establish SQL connection
    conn = pyodbc.connect("Driver={SQL Server};"
                          "Server=sql2014b8;" # TODO: specify server
                          "Database=GeoDepot;" # TODO: specify database
                          "Trusted_Connection=yes;")
    # run query
    resultDF = pd.read_sql_query(sql, conn)
    
    # convert to GeoDF
    resultDF["geometry"] = [wkt.loads(x) for x in resultDF["geometry"]]
    resultDF = gpd.GeoDataFrame(resultDF, crs="EPSG:2230", geometry="geometry")
    
    return resultDF

# get Bzone (TAZ) layer
series_ver = 13 #TODO: specify TAZ version
sql = ("SELECT [taz], [Shape].ToString() AS [geometry]"
        f" FROM [GeoDepot].[gis].[TAZ{series_ver}]")
sql2 = ("SELECT [mgra], [taz], [Shape].ToString() AS [geometry]"
        f" FROM [GeoDepot].[gis].[MGRA{series_ver}]")
taz = get_gis_layer(sql)
mgra = get_gis_layer(sql2)

# load VE-specific MGRA area type (provided by Grace Chung & Mike Calandra)
# SQL2014b8\RM.DBO.AreaType_MGRA
area_type = gpd.read_file(r"..\data\RM.DBO.AreaType_MGRA.shp")[['MGRA', 'Loc_Type']]

# xref mgra with taz
mgra2taz = mgra.merge(taz, on='taz')[['mgra', 'taz']]

# xref mgra with Marea
resultDF = mgra2taz.merge(geo, left_on='taz', right_on='Bzone')[['mgra', 'Marea']]
resultDF = resultDF.fillna("None")
resultDF.to_csv(r"..\output\mgra_Marea_xref.csv", index=False)