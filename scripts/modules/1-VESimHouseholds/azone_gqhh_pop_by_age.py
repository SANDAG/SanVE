# -*- coding: utf-8 -*-
"""
azone_gq_pop_by_age.csv

@author: jyen
"""

import os
import re
import pandas as pd
import numpy as np

# Set workspace to the script directory
os.chdir(os.path.dirname(os.path.abspath('__file__')))

# TODO: initialize ABM scenarioList
scenario = ['2016', '2035build']

# Load geography definition from mgra13_city_xref
"""
Upon Cherry's inspection, the mgra-taz-city xref in mgra input file doesn't meeet VE requirement
which only allows one-to-one mgra xref city. So Jeff created mgra13_city_xref table that ensure
this relation between mgra and city. And geo.csv provides the relation of taz-city xref.
Decsision: use mgra13_city_xref for all Azone related input and output files.
"""
mgraXrefCity = pd.read_csv(r"..\defs\mgra13_city_xref.csv")
mgraXrefCity.columns = ['mgra', 'Azone']

#
azSorter = [12, 19, 18,  7, 15,  1, 14,  6, 13, 17,  4, 16,  5,  9, 10,  3, 11, 2,  8]

# Functions
# Calculate age group for each person in syn_POP
def age_group(sub_pop, choicelist):
    #create age group
    sub_pop['Age_Group'] = (np.select(
                                        condlist = [(sub_pop.age >= 0) & (sub_pop.age <= 14),
                                                    (sub_pop.age >= 15) & (sub_pop.age <= 19),
                                                    (sub_pop.age >= 20) & (sub_pop.age <= 29),
                                                    (sub_pop.age >= 30) & (sub_pop.age <= 54),
                                                    (sub_pop.age >= 55) & (sub_pop.age <= 64),
                                                    sub_pop.age >= 65],
                                        choicelist = choicelist,
                                        default = 'Other')
                            )
    
    #aggregate subsynPOP by Age Group in each Azone (Geo)
    sub_pop = sub_pop.groupby(['Geo', 'Age_Group', 'Year'])['perid'].count().reset_index(name = 'subtotalPOP')
    
    #pivot subsynPOP
    sub_pop = (pd.pivot(
                        sub_pop,
                        index=['Geo', 'Year'],
                        columns = 'Age_Group',
                        values = 'subtotalPOP')
                        .reset_index(level=['Geo', 'Year'])
                        )
    
    #fill NaN with zero population
    sub_pop = sub_pop.fillna(0)
    
    #assign zero population to missing age groups
    missing_header = list(set(choicelist).difference(sub_pop.columns))
    if missing_header is not []:
        for miss in missing_header:
            sub_pop[miss] = 0
            
        #convert all values in resulting DF to integer
        sub_pop = sub_pop.astype('int64')
        
        #re-order the columns in resulting DF
        sub_pop = sub_pop[['Geo', 'Year'] + choicelist]
    
    return sub_pop

# Convert SANDAG SynPopulation to VE Azone Population
def convert_population(scenario):
    #initialize choicelist(header) for subsynPOP
    gq_choicelist = ['GrpAge0to14', 'GrpAge15to19', 'GrpAge20to29',
                     'GrpAge30to54', 'GrpAge55to64', 'GrpAge65Plus']
    reg_choicelist = ['Age0to14', 'Age15to19', 'Age20to29',
                     'Age30to54', 'Age55to64', 'Age65Plus']
    
    #for year_id, year in enumerate(yearList):
    for scen in scenario:
        #extract scenario year
        year = re.split(r'(\d+)', scen)[1]
        
        #load SANDAG syn_POP
        person = pd.read_csv(r"T:\RTP\2021RP\2021rp_draft_v2\abm_runs\{}\input\persons.csv".format(scen))
        household = pd.read_csv(r"T:\RTP\2021RP\2021rp_draft_v2\abm_runs\{}\input\households.csv".format(scen))

        #add Azone to the syn_POP
        synPOP = person.merge(household[['hhid', 'unittype', 'mgra']], on='hhid')
        synPOP = synPOP.merge(mgraXrefCity, on='mgra')
        synPOP = synPOP.rename(columns={'Azone':'Geo'})
        synPOP['Year'] = year

        #separate regular pop and group quarter pop
        gqPOP = synPOP.query("unittype == 1")
        regPOP = synPOP.query("unittype == 0")
        
        #calculate age group for each person in syn_POP
        gqPOP = age_group(gqPOP, gq_choicelist)
        regPOP = age_group(regPOP, reg_choicelist)
        
        #apeend missing Azone ID to gpPOP
        missingAzone = list(mgraXrefCity.loc[~mgraXrefCity.Azone.isin(gqPOP.Geo)]['Azone'].unique())
        gqPOP = gqPOP.append(pd.DataFrame(missingAzone, columns=['Geo'])).fillna(0)
        gqPOP['Year'] = year
        gqPOP = gqPOP.astype('int64').sort_values(['Geo'])
        
        #sort resulting DFs by azone sorter
        gqPOP = gqPOP.set_index('Geo')
        gqPOP = gqPOP.loc[azSorter].reset_index()
        regPOP = regPOP.set_index('Geo')
        regPOP = regPOP.loc[azSorter].reset_index()
        
        #append result DataFrames to resultList
        resultList.append([gqPOP, regPOP])
        
    return resultList
        
# Run the conversion
resultList = []
resultList = convert_population(scenario)

# Update resultList
zipped = list(zip(*resultList))
resultList = [pd.concat(i) for i in zipped]

# Export resultDF from resultList
resultList[0].to_csv(r"..\output\azone_gq_pop_by_age.csv", index=False) #group quarter POP
resultList[1].to_csv(r"..\output\azone_hh_pop_by_age.csv", index=False) #regular POP