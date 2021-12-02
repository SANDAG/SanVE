# -*- coding: utf-8 -*-
"""
bzone_employment.csv

This file contains the total, retail and service 
employment by zone for each of the base and future years.

@author: Jeff Yen

"""

import re
import pandas as pd
from utilities.emp_re_classification import emp_rec

# Load geography definition
geo = pd.read_csv(r"..\defs\geo.csv")

# Modules
def bz_employment(mgra, scen_year, scaleFactor):
    # Employment re-classification
    mgra = emp_rec(mgra)
        
    # Get employment in Bzone and apply scaleFactor
    df = geo.merge(mgra, left_on='Bzone', right_on='taz', how='left')
    df['TotEmp'] = (df['emp_total'] * scaleFactor).round(0).astype('int64')
    df['SvcEmp'] = (df['SvcEmp'] * scaleFactor).round(0).astype('int64')
    df['RetEmp'] = (df['RetEmp'] * scaleFactor).round(0).astype('int64')
    df['OtherEmp'] = (df['OtherEmp'] * scaleFactor).round(0).astype('int64')
    
    # Get total employment in Bzone, # of jobs in retail / service sector in Bzone
    leBzone = df.groupby(['Bzone'])[['RetEmp', 'SvcEmp', 'TotEmp']].sum().reset_index()
    
    # Format Bzone Table
    leBzone['Year'] = scen_year
    leBzone = leBzone.rename(columns={'Bzone':'Geo'})
    leBzone = leBzone[['Geo', 'Year', 'TotEmp', 'RetEmp', 'SvcEmp']]
    leBzone = leBzone.sort_values(['Geo']) #sort by Bzone
    
    
    return leBzone
    

# TODO: specify scenario year
"""
ScaleFactor to adjust ABM total employment were computed by Susan Xu
The scale was calculated to the number of workers divided by the number of jobs.
"""
scenarioDicts = {'2016':0.92, '2035build':0.85}
resultList = []

# Run modules throughout each scenario year
for scen, scaleFactor in scenarioDicts.items():
    #extract scenario year
    year = re.split(r'(\d+)', scen)[1]
    
    #load MGRA from ABM input
    mgra = pd.read_csv(r"T:\RTP\2021RP\2021rp_draft_v2\abm_runs\{}\input\mgra13_based_input{}.csv".format(scen, year))
    
    #run modules
    resultDF = bz_employment(mgra, year, scaleFactor)
    
    #append resultDF to resultList
    resultList.append(resultDF)

# Export resulting bzoneDF to .csv
outputDF = pd.concat(resultList)
outputDF.to_csv(r"..\output\bzone_employment.csv", index=False)