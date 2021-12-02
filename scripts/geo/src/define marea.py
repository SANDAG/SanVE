# -*- coding: utf-8 -*-
"""
Define Marea

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

# Specify spatial queries (TAZ, City)
taz = ("SELECT [TAZ], [Shape].ToString() AS [geometry]"
        "FROM [GeoDepot].[gis].[TAZ13]"                 )

# Get TAZ layer
tazDF = get_gis_layer(taz)

# Initialize model year of interest
year = [2016, 2035] #TODO

# Join TAZ with xref and export to .shp and .csv
for yr in year:
    #load year-specific transit stop and TAZ xref
    xref = pd.read_csv(r"..\data\Stops_TAZs_{}.csv".format(yr%100))
    
    #join TAZ with xref
    resultDF = tazDF.merge(xref, on='TAZ', how='left')
    
    #sum total number of transit stops in each TAZ
    resultDF = resultDF.groupby('TAZ')['FREQUENCY'].sum().reset_index()
    resultDF['FREQUENCY'] = resultDF['FREQUENCY'].astype('int64')
    
    #join TAZ geography with resultDF
    resultDF = tazDF.merge(resultDF, on='TAZ')
    
    #check if there is any Null FREQUENCY
    if len(resultDF.loc[resultDF['FREQUENCY'].isna()]) != 0:
        print("Check Null FREQUENCY values...")
    
    #export results
    resultDF[['TAZ', 'FREQUENCY']].to_csv(r"..\output\{}initial_Marea.csv".format(yr), index=False)


