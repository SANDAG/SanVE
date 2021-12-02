# -*- coding: utf-8 -*-
"""
bzone_hh_inc_qrtl_prop


Household proportion by income (bzone_hh_inc_qrtl_prop.csv): This file contains the proportion of Bzone 
non-group quarters households by quartile of Azone household income category for each of the base and future years.

@author: jyen
"""

import os
import re
import numpy as np
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
    household = household.merge(geo, left_on='taz', right_on='Bzone')
    household = household.query("unittype == 0") # restrict to Bzone non-group quarters households
    
    # compute each hhic quartile by Azone (key: Azone, values: quartile stats)
    # initialize dictionary of matched links to stations
    azDict = {x:np.nan for x in geo["Azone"]}
    
    azHincStat = household.groupby(["Azone"])['hinc'].describe().reset_index()
    azHincStat = azHincStat.rename(columns={'25%':'Q1',
                                            '50%':'Q2',
                                            '75%':'Q3'})
    for hh in azHincStat.itertuples():
        azDict[hh.Azone] = [hh.Q1, hh.Q2, hh.Q3]
    
    #
    azHincStatDF = pd.DataFrame(azDict).transpose().reset_index().sort_values('index')
    azHincStatDF.columns = ['Azone', 'Q1', 'Q2', 'Q3']
    
    # join household with quartile of Azone household income category
    hh = household.merge(azHincStatDF, on='Azone')[['Azone', 'Bzone', 'hinc', 'Q1', 'Q2', 'Q3']]
    
    #
    hh['hh_quartile'] = np.select(condlist = [hh.hinc <= hh.Q1,
                                              hh.hinc.between(hh.Q1, hh.Q2, inclusive='right'),
                                              hh.hinc.between(hh.Q2, hh.Q3, inclusive='right'),
                                              hh.hinc > hh.Q3],
                                  choicelist = ['HhIncQ1', 'HhIncQ2', 'HhIncQ3', 'HhIncQ4'],
                                  default = np.nan
    )
    
    # compute the proportion of Bzone non-group quarters households by quartile of Azone household income category
    bzQart = hh.groupby(['Bzone','hh_quartile'])['hh_quartile'].count().reset_index(name='hh_quartile_count')
    bzTotHH = hh.groupby(['Bzone'])['hinc'].count().reset_index(name='totHH')
    bzDF = bzQart.merge(bzTotHH, on='Bzone')
    bzDF['hh_quartile_prop'] = bzDF.hh_quartile_count / bzDF.totHH
    
    #
    resultDF = pd.pivot_table(bzDF, values='hh_quartile_prop', index=['Bzone'],
                              columns=['hh_quartile'], fill_value=0).reset_index()
    
    #
    resultDF = geo[['Bzone']].merge(resultDF, on='Bzone', how='left')
    
    # format resultDF
    resultDF.columns = ['Geo', 'HhPropIncQ1', 'HhPropIncQ2', 'HhPropIncQ3', 'HhPropIncQ4']
    resultDF = resultDF.sort_values(['Geo']) # sort by Bzone
    resultDF = resultDF.fillna(0)
    resultDF.insert(1,'Year', year)
    
    #append resultDF to resultList
    resultList.append(resultDF)
    
    
# Export outputDF
outputDF = pd.concat(resultList).round(2)
outputDF.to_csv(r"..\output\bzone_hh_inc_qrtl_prop.csv", index=False)