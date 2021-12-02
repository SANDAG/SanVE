# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 16:30:38 2021

@author: jyen
"""

import os
import re
import pandas as pd


# Set workspace to the script directory
os.chdir(os.path.dirname(os.path.abspath('__file__')))

# Load geography definition
geo = pd.read_csv(r"..\defs\geo.csv")

# Run modules throughout each scenario year
scenarioList = ['2016', '2035build'] #TODO: specify scenario year
resultList = []

for scen in scenarioList:
    #extract scenario year
    year = re.split(r'(\d+)', scen)[1]
    
    # Load Household from ABM Scenario
    household = pd.read_csv(r"T:\RTP\2021RP\2021rp_draft_v2\abm_runs\{}\input\households.csv".format(scen))
    mgra = pd.read_csv(r"T:\RTP\2021RP\2021rp_draft_v2\abm_runs\{}\input\mgra13_based_input{}.csv".format(scen, year))
    
    """
    SFDU: Number of single family dwelling units (PUMS codes 01 - 03) in zone (Please include mobile home to SF)
    MFDU: Number of multi-family dwelling units (PUMS codes 04 - 09) in zone
    GQDU: Number of qroup quarters population accommodations in zone
    """
    # Summarize SFDU and MFDU in Bzone
    mgraDF = geo.merge(mgra, left_on='Bzone', right_on='taz')
    mgraDF['SFDU'] = mgraDF.hs_sf + mgraDF.hs_mh
    mgraDF['MFDU'] = mgraDF.hs_mf
    bzoneDF = mgraDF.groupby(['Bzone'])[['SFDU', 'MFDU']].sum().reset_index()
    
    # Summarize GQDU in Bzone
    gq = household.query("unittype == 1")
    gqPOP = gq.groupby(['taz'])['persons'].sum().reset_index(name='GQDU') #SANDAG does not have GQDU, use GOPOP as an imputed value
    
    # Combine resulting DU
    bzoneDF = bzoneDF.merge(gqPOP, left_on='Bzone', right_on='taz', how='left').fillna(0)
    bzoneDF['Geo'] = bzoneDF.Bzone.copy()
    bzoneDF['Year'] = year
    bzoneDF = bzoneDF[['Geo', 'Year', 'SFDU', 'MFDU', 'GQDU']].astype('int64')
    bzoneDF = bzoneDF.sort_values(['Geo']) # sort by Bzone
    
    #append resultDF to resultList
    resultList.append(bzoneDF)


# Export outputDF
outputDF = pd.concat(resultList)
outputDF.to_csv(r"..\output\bzone_dwelling_units.csv", index=False)
