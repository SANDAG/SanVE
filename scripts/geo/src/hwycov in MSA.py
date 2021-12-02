# -*- coding: utf-8 -*-
"""
EMME @tcov in MSA for base year only

@author: Jeff Yen

"""

import geopandas as gpd
from utilities.get_gis_layer import get_gis_lyr

# Get MSA layer
msaSQL = ("SELECT [MSA], [NAME], [Shape].ToString() AS [geometry]"
          " FROM [GeoDepot].[gis].[MSA]")
msa = get_gis_lyr(msaSQL, 'sql2014b8', 'GeoDepot')

# TODO
baseYear = 2016 # specify base yaer
emmeLink = gpd.read_file(r"..\data\2016 Shapefile\emme_links.shp") #T:\RTP\2021RP\2021rp_draft_v2\abm_runs\2016\emme_project\Database
emmeLink = emmeLink.to_crs("EPSG:2230")
emmeLink['geometry'] = emmeLink.centroid

# Get qualifying tcov links from input scenario years
# spatial join tcov centroids with MSA boundary
resultDF = gpd.sjoin(emmeLink[['@tcov_id','geometry']], msa, how="left")

# format resultDF
resultDF['YEAR'] = baseYear
resultDF.columns = resultDF.columns.str.lower()
resultDF = resultDF.drop(['geometry', 'index_right'],axis=1)

# # Export resultDF
# resultDF.to_csv(r"..\output\tcov_in_MSA.csv", index=False)