# -*- coding: utf-8 -*-
"""
hwycov in Marea

@author: Jeff Yen

"""

import os
import re
import numpy as np
import pandas as pd
import geopandas as gpd
from utilities.get_gis_layer import get_gis_lyr

# Set workspace to current script directory
os.chdir(os.path.dirname(os.path.abspath('__file__')))

# Load geography definition
geo = pd.read_csv(r"..\defs\geo.csv")

# Get TAZ layer
sql = ("SELECT [TAZ], [Shape].ToString() AS [geometry]"
        "FROM [GeoDepot].[gis].[TAZ13]"                 )
taz = get_gis_lyr(sql, 'sql2014b8', 'GeoDepot')

# Join TAZ with geo definition
tazDF = taz.merge(geo, left_on='TAZ', right_on='Bzone').reset_index().drop('index', axis=1)

# Initialize result scenario list
resultList = []
scenarioList = ['2016', '2035build'] #TODO: specify scenario year

# Get qualifying hwycov links from input scenario years
for scen in scenarioList:
    # extract scenario year
    year = re.split(r'(\d+)', scen)[1]
    
    # load hwycov from ABM  Scenario
    hwycov = gpd.read_file(r"..\data\{}_hwycov.shp".format(scen))
    hwycov['geometry'] = hwycov.centroid
    hwycov = hwycov[['HWYCOV-ID', 'IFC', 'geometry']]
    
    # spatial join hwycov centroids with TAZ boundary
    resultDF = gpd.sjoin(hwycov, tazDF, how="left")
    
    # exclude hwycov links not in Marea or not in SD city boundary
    resultDF = resultDF.loc[resultDF['Marea'] == 'SD-Urban-TransitService']
    resultDF = resultDF[['HWYCOV-ID', 'IFC', 'Azone', 'Bzone', 'Czone', 'Marea']]
    
    # slice resultDF by freeway and arterial
    resultDF['road_type'] = np.select(
                                      condlist = [resultDF['IFC'].isin([1,8]),
                                                  resultDF['IFC'].isin([2,3]),
                                                  ~resultDF['IFC'].isin([1,8,2,3])],
                                      choicelist = ['freeway', 'arterial', 'other'],
                                      default = np.nan
                                      )
    freewayDF = resultDF.query("road_type == 'freeway'")
    arterialDF = resultDF.query("road_type == 'arterial'")
    otherDF = resultDF.query("road_type == 'other'")
    
    # export "HWYCOV-ID"
    freewayDF['HWYCOV-ID'].to_csv(r"..\output\{}_freeway.csv".format(year), index=False)
    arterialDF['HWYCOV-ID'].to_csv(r"..\output\{}_arterial.csv".format(year), index=False)
    otherDF['HWYCOV-ID'].to_csv(r"..\output\{}_other.csv".format(year), index=False)
    
    # export resultDF to csv
    resultDF['year'] = year
    resultDF.to_csv(r"..\output\{}hwycov_in_Marea.csv".format(year), index=False)