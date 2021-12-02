# -*- coding: utf-8 -*-
"""
Build City and TAZ Xref

@author: Jeff Yen


"""

import os
import pyodbc
import pandas as pd
import geopandas as gpd
from shapely import wkt

# Set workspace to current script directory
os.chdir(os.path.dirname(os.path.abspath('__file__')))

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

# Specify spatial queries (MGRA, TAZ, City)
mgra = ("SELECT [MGRA], [TAZ], [Shape].ToString() AS [geometry]"
        "FROM [GeoDepot].[gis].[MGRA13]"                                )
taz = ("SELECT [TAZ], [Shape].ToString() AS [geometry]"
        "FROM [GeoDepot].[gis].[TAZ13]"                 )
city = ("SELECT [City], [Name], [Code], [Shape].ToString() AS [geometry]"
        "FROM [GeoDepot].[gis].[Cities]"                                )

# Get gis layers as GeoDFs
tazDF = get_gis_layer(taz)
tazDF['geometry'] = tazDF.centroid # transform TAZ geometry from POLYGON to POINT
cityDF = get_gis_layer(city)
mgraDF = get_gis_layer(mgra)[['MGRA', 'TAZ']]

# Spatial join TAZ centroids with City boundary
resultDF = gpd.sjoin(tazDF, cityDF, how="left")
resultDF = resultDF.loc[resultDF['City'].notna()]

# Format lookup table
resultDF = resultDF[['City', 'TAZ']]
resultDF = resultDF.rename(columns={'City':'Azone', 'TAZ':'Bzone'})
resultDF['Azone'] = resultDF.Azone.astype('int64')
resultDF['Czone'] = 'NA'

# Load Marea (use 2016 to represent all scenario years for now)
mAreaTS = pd.read_csv(r"..\output\2016initial_Marea.csv")
mAreaTS = mAreaTS.query("FREQUENCY > 0")

# load VE-specific MGRA area type (provided by Grace Chung & Mike Calandra)
# SQL2014b8\RM.DBO.AreaType_MGRA
# assumption: a TAZ covers at leat one Urban/Town MGRA can be counted as Marea
area_type = gpd.read_file(r"..\data\RM.DBO.AreaType_MGRA.shp")[['MGRA', 'Loc_Type']]
urbanMGRA = area_type.query("Loc_Type in ('Urban')")
mAreaUR = mgraDF.merge(urbanMGRA, on='MGRA')
mAreaUR = mAreaUR.groupby(['TAZ', 'Loc_Type']).size().reset_index().drop_duplicates(subset=['TAZ'])

#
union = mAreaUR.TAZ.append(mAreaTS.TAZ).reset_index().drop(['index'], axis=1)
mArea = pd.DataFrame(union.TAZ.unique(), columns=['TAZ'])
resultDF = resultDF.merge(mArea, left_on='Bzone', right_on='TAZ', how='left')
resultDF['Marea'] = resultDF.apply(lambda x: 'SD-Urban-TransitService' if x.TAZ > 0 else 'None', axis = 1)

# format resultDF
resultDF = resultDF[['Azone', 'Bzone', 'Czone', 'Marea']]
resultDF = resultDF.sort_values(['Bzone'])

# Export lookup table as csv
resultDF.to_csv(r"..\output\geo.csv", index = False)
