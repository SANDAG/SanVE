# -*- coding: utf-8 -*-
"""
bzone_unprotected_area.csv

Developable area (bzone_unprotected_area.csv): This file contains the 
information about unprotected (i.e., developable) area within the zone.

@author: jyen
"""
import os
import re
import numpy as np
import pandas as pd
import geopandas as gpd
from utilities.get_gis_layer import get_gis_lyr

# Set workspace to the script directory
os.chdir(os.path.dirname(os.path.abspath('__file__')))

def create_devple_land(series_ver):
    # load overlay mgra and consve
    overlay = gpd.read_file(r"..\data\land_use\mgra_overlay_consveDisolve.shp")[['MGRA', 'Shape_Area']]
    overlay = overlay.rename(columns={'MGRA':'mgra'})
    overlay['ov_acres'] = overlay.Shape_Area * 0.000022956 # convert square ft to acre
    
    # load MGRA from GeoDepot
    server = 'sql2014b8'
    database = 'GeoDepot'
    sql = ("SELECT [mgra], [taz], [Shape].ToString() AS [geometry]"
            f" FROM [GeoDepot].[gis].[mgra{series_ver}]")
    mgra = get_gis_lyr(sql, server, database)
    mgra['mgra_acres'] = mgra.area * 0.000022956 # convert square ft to acre

    # calculate overlayed area % indicating the area % of mgra in consve land
    mgraDF = mgra.merge(overlay[['mgra', 'ov_acres']], on='mgra', how='left').fillna(0)
    mgraDF['area_ratio'] =  (mgraDF.ov_acres / mgraDF.mgra_acres).round(6) # ov_acres is the conserved acres in mgra

    # apply the unprotected area % to totoal area of mgra (in acre) => get the acres in unprotected (aka. developable) land
    mgraDF['developable_acres'] = (np.select(condlist = [mgraDF['area_ratio'] == 0,
                                                         mgraDF['area_ratio'] == 1],
                                             choicelist = [mgraDF['mgra_acres'], 0],
                                             default = mgraDF['mgra_acres'] - mgraDF['ov_acres'])
    )
    
    return mgraDF

# TODO: parameter settings
scenarioList = ['2016', '2035build'] # specify scenario year
series_ver = 13 # specify MGRA & TAZ version
resultList = []

# Get developabale MGRA
devpleMGRA = create_devple_land(series_ver)

# load VE-specific MGRA area type (provided by Grace Chung & Mike Calandra)
veMGRA = gpd.read_file(r"..\data\RM.DBO.AreaType_MGRA.shp")[['MGRA', 'Loc_Type']]

# Load geography definition
geo = pd.read_csv(r"..\defs\geo.csv")

# Classify developabale MGRA by VE-specific land use (use base year 2016 for future year)
mgraDF = devpleMGRA.merge(veMGRA, left_on='mgra', right_on='MGRA')
resultDF = mgraDF.groupby(['taz', 'Loc_Type'])['developable_acres'].sum().reset_index()
resultDF = pd.pivot_table(resultDF, values='developable_acres', index=['taz'],
                          columns=['Loc_Type'], fill_value=0).reset_index()

# Format outputDF
resultDF.columns = ['Geo', 'RuralArea', 'TownArea', 'UrbanArea']
resultDF = resultDF.sort_values(['Geo']) # sort by Bzone

# Iterate through each scenario
for scen in scenarioList:
    # extract scenario year
    year = re.split(r'(\d+)', scen)[1]
    
    # insert scenario year to resultDF (assuming base year land use is applied to future year)
    outputDF = resultDF.copy()
    outputDF.insert(1, 'Year', year)
    
    # append outputDF to resultList
    resultList.append(outputDF)

# Export outputDF
masterDF = pd.concat(resultList)
masterDF.to_csv(r"..\output\bzone_unprotected_area.csv", index=False)

