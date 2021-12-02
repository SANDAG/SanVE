# -*- coding: utf-8 -*-
"""
Update Attributes in highway_statistics by MSA
This update only applies to base year scenario

*RoadMiles: Total miles of all roadways in the urbanized area
*FwyMiles: Total miles of freeways
*FwyLaneMi: Total freeway lane miles

ref:
T:\ABM\ABM_FY22\RSM\VisionEval\Model\SanVE\sources\modules\VE2001NHTS\inst\extdata

@author: Jeff Yen

"""

import numpy as np
import pandas as pd
import geopandas as gpd

# Load data
xref = pd.read_csv(r"..\output\hwycov_in_MSA.csv") #hwycov-MSA xref table
hwycov = gpd.read_file(r"..\data\2016_hwycov.shp") #base year hwycov
hwycov['Miles'] = hwycov.LENGTH * 0.000189394
hwyMSA = hwycov.merge(xref, left_on='HWYCOV-ID', right_on='hwycov-id')

# RoadMiles by MSA
urbanMSA = ['CENTRAL','NORTH CITY','EAST SUBURBAN'] #TODO: provided by Susan
result1 = hwyMSA.groupby(['msa','name'])[['Miles']].sum().rename(columns={'Miles':'RoadMiles'})

# FwyMiles and FwyLaneMi by MSA
fwyMSA = hwyMSA.query("IFC in (1,8)")
fwyMSA['FwyLaneMi'] = fwyMSA.Miles * (fwyMSA.ABLNO + fwyMSA.BALNO)
result2 = fwyMSA.groupby(['msa','name'])[['Miles','FwyLaneMi']].sum().rename(columns={'Miles':'FwyMiles'})

# Merge results
resultDF = result1.merge(result2, left_index=True, right_index=True).reset_index().round(0)
# resultDF['RoadMiles'] = resultDF.apply(lambda x:x['RoadMiles'] if x['name'].isin(urbanMSA) else 0, axis=1)
resultDF['RoadMiles'] = np.where(resultDF['name'].isin(urbanMSA), resultDF['RoadMiles'], 0)

# Export resultDF
resultDF.to_csv(r"..\output\highway_statistics_by_MSA.csv", index=False)