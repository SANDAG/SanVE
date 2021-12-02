# -*- coding: utf-8 -*-
"""
Get GIS layer from SQL

@author: jyen
"""

import pyodbc
import pandas as pd
import geopandas as gpd
from shapely import wkt


def get_gis_lyr(sql, server, database):
    # establish SQL connection
    conn = pyodbc.connect("Driver={SQL Server};"
                          f"Server={server};"
                          f"Database={database};"
                          "Trusted_Connection=yes;")
    # run query
    resultDF = pd.read_sql_query(sql, conn)
    
    # convert to GeoDF
    resultDF["geometry"] = [wkt.loads(x) for x in resultDF["geometry"]]
    resultDF = gpd.GeoDataFrame(resultDF, crs="EPSG:2230", geometry="geometry")
    
    return resultDF