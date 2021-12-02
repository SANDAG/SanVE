'''
Calculate freeway and arterial lane-miles and vehichle class propostoin within metropolitan areas (Marea)

Author: C Liu
Created on 07/13/2021
Updated on 08/27/2021, vehichle class proportions of LDV, truck and transit
'''
import os
from csv import reader
import yaml
import pandas as pd
from collections import OrderedDict
import inro.emme.database.emmebank as _eb                                   
import inro.emme.desktop.app as _app
import inro.modeller as _m

_join = os.path.join

CONFIG = r'T:/ABM/ABM_FY22/RSM/VisionEval/Model/Update_Automations/settings.yml'
with open(CONFIG) as cff:
    config =yaml.safe_load(cff)
target_path = ''.join(config['target_path'])
scenpath = ''.join(config['scenpath'])
#source_path = ''.join(config['source_path'])
scenario_list = config['scenario_list']
road_list = config['road_list']

df_geo = pd.read_csv(_join(target_path, 'defs\geo.csv'))[['Marea']]
Marea_List = df_geo['Marea'].unique().tolist()
df_geo = df_geo.fillna("None")
Marea_List = df_geo['Marea'].unique().tolist()

# Open the first reference Emme project
scenario_name = scenario_list[0][1]
my_app = _app.start_dedicated(project = _join(scenpath, scenario_name, 'emme_project\emme_project.emp'), visible = True, user_initials = 'sd')
m = _m.Modeller(my_app)
netcalc = _m.Modeller().tool("inro.emme.network_calculation.network_calculator")
create_attribute = m.tool("inro.emme.data.extra_attribute.create_extra_attribute")
matrix_calc = _m.Modeller().tool("inro.emme.matrix_calculation.matrix_calculator")

# Caculated lane miles for freeways and arterial roads
print
periods = ["EA", "AM", "MD", "PM", "EV"]
base_scenario_id = 100
period_scenario_ids = OrderedDict((v, i) for i, v in enumerate(periods, start=base_scenario_id + 1))
lanemile_list = []
NMlanemile_list = []
LtTrkProp_list = []
total_vmt = 0
for year, scenario_name in scenario_list:
    proportion_list = []
    NMproportion_list = []
    emmebank_path = _join(scenpath, scenario_name, r'emme_project\Database\emmebank')
    emmebank = _eb.Emmebank(emmebank_path)
    exp0 = ""
    with open(_join(CONFIG[:-13], str(year) + '_hwycov_outside_SD_cities_boundary.csv'), 'r') as read_obj:
        csv_reader = reader(read_obj)
        next(csv_reader)
        for row in csv_reader:
            exp0 = exp0 + "@tcov_id = %d or @tcov_id = %d or " % (int(row[0]), -int(row[0])) 
        exp0 = exp0[:-3]       
    for period, scenario_id in period_scenario_ids.iteritems(): 
        scenario = emmebank.scenario(scenario_id)
        ###
        # create @marea and set values for the entire region
        att = create_attribute("LINK", "@marea", "Marea, 1,4-fwy,2,5-arterial,3,6-rest", 0, overwrite=True, scenario=scenario)    
        # set up for the engire region (@tcov_id not equal 0)
        spec9 = {
            "type": "NETWORK_CALCULATION",
            "expression": "6",
            "result": "@marea",
            "aggregation": None,
            "selections": {"link": "type=1,9 and mode=d"}}
        spec10 = {
            "type": "NETWORK_CALCULATION",
            "expression": "5",
            "result": "@marea",
            "aggregation": None,
            "selections": {"link": "type = 2,3 and mode=d"}}
        spec11 = {
            "type": "NETWORK_CALCULATION",
            "expression": "4",
            "result": "@marea",
            "aggregation": None,
            "selections": {"link": "type=1 or type=8 and mode=d"}}             
        report = netcalc([spec9,spec10,spec11], scenario = scenario) 
        ###
        for name, road_type in road_list:
            ###
            # set up @marea for marea only
            exp = ""
            #with open(_join(CONFIG[:-13], str(year) + '_marea_' + name + '.csv'), 'r') as read_obj:
            with open(_join(CONFIG[:-13], str(year) + '_' + name + '.csv'), 'r') as read_obj:
                csv_reader = reader(read_obj)
                next(csv_reader)
                for row in csv_reader:
                    exp = exp + "@tcov_id = %d or @tcov_id = %d or " % (int(row[0]), -int(row[0])) 
                exp = exp[:-3]            
            spec1 = {
                "type": "NETWORK_CALCULATION",
                "expression": "%d" % road_type,
                "result": "@marea",
                "aggregation": None,
                "selections": {"link": "%s" % exp}}
            report = netcalc([spec1], scenario = scenario) 
            # remove links outside of city boundary  
            spec16 = {
                "type": "NETWORK_CALCULATION",
                "expression": "0",
                "result": "@marea",
                "aggregation": None,
                "selections": {"link": "%s" % exp0}}
            report = netcalc([spec16], scenario = scenario) 
            print "line 114,", year, period, road_type, report[0]['num_results_obtained']            
            ###
            if year == 2016:
                # calculate vmt proportion by vehicle classes
                spec2 = {
                    "type" : "NETWORK_CALCULATION",
                    "result" : None,
                    "expression" : "(@sov_nt_all+@sov_tr_all+@hov2_all+@hov3_all)*length",
                    "aggregation" : None,
                    "selections" : {
                        "link" : "@marea = %d" %road_type}}
                spec3 = {
                    "type" : "NETWORK_CALCULATION",
                    "result" : None,
                    "expression" : "((@trk_l)/1.3 + (@trk_m)/1.5+(@trk_h)/2.5)*length",
                    "aggregation" : None,
                    "selections" : {
                        "link" : "@marea = %d" %road_type}}
                spec4 = {
                    "type" : "NETWORK_CALCULATION",
                    "result" : None,
                    "expression" : "(volad/3)*length",
                    "aggregation" : None,
                    "selections" : {
                        "link" : "@marea = %d" %road_type}}   
                spec12 = {
                    "type" : "NETWORK_CALCULATION",
                    "result" : None,
                    "expression" : "(@sov_nt_all+@sov_tr_all+@hov2_all+@hov3_all)*length",
                    "aggregation" : None,
                    "selections" : {
                        "link" : "@marea = %d" %(int(road_type)+3)}}
                spec13 = {
                    "type" : "NETWORK_CALCULATION",
                    "result" : None,
                    "expression" : "((@trk_l)/1.3 + (@trk_m)/1.5+(@trk_h)/2.5)*length",
                    "aggregation" : None,
                    "selections" : {
                        "link" : "@marea = %d" %(int(road_type)+3)}}
                spec14 = {
                    "type" : "NETWORK_CALCULATION",
                    "result" : None,
                    "expression" : "(volad/3)*length",
                    "aggregation" : None,
                    "selections" : {
                        "link" : "@marea = %d" %(int(road_type)+3)}}  
                report1 = netcalc([spec2, spec3, spec4,spec12, spec13, spec14], scenario = scenario)
                proportion_list.append([report1[0]['sum'], report1[1]['sum'], report1[2]['sum']])  # [freeway[LDV, Truck, transit], arterial[LDV, Truck, transit], other[LDV, Truck, transit],], 5 TODs
                NMproportion_list.append([report1[3]['sum'], report1[4]['sum'], report1[5]['sum']]) 

            # calculate lane miles - AM ONLY
            if period == "AM":  #get lane mile from AM only
                spec5 = {
                    "type" : "NETWORK_CALCULATION",
                    "result" : None,
                    "expression" : "length*lanes",
                    "aggregation" : None,
                    "selections" : {
                        "link" : "@marea = %d" %road_type}}
                spec15 = {
                    "type" : "NETWORK_CALCULATION",
                    "result" : None,
                    "expression" : "length*lanes",
                    "aggregation" : None,
                    "selections" : {
                        "link" : "@marea = %d" %(int(road_type)+3)}}                        
                report2 = netcalc([spec5, spec15], scenario = scenario)
                lanemile_list.append([report2[0]['sum']])  # [[freway lane miles],[arterial lane miles]] AM Marea ONLY  
                NMlanemile_list.append([report2[1]['sum']])  # [[freway lane miles],[arterial lane miles]] AM None Marea ONLY  
        #total heavy truck VMT                
        if year == 2016:
            scenario = emmebank.scenario(scenario_id)
            spec6 = {
                "type" : "NETWORK_CALCULATION",
                "result" : None,
                # "expression" : "(@sov_nt_all+@sov_tr_all+@hov2_all+@hov3_all+(@trk_l)/1.3 + (@trk_m)/1.5+(@trk_h)/2.5 + volad/3)*length",
                "expression" : "((@trk_l)/1.3 + (@trk_m)/1.5+(@trk_h)/2.5)*length",
                "aggregation" : None,
                "selections" : {
                    "link" : "all"}}
            report3 = netcalc([spec6], scenario = scenario)
            total_vmt += report3[0]['sum']    
                
            '''
            # calculate light truck demans (proportion)
            if period == "AM" and name == 'freeway':    
                spec7 = {
                    "expression": "mfEA_TRK_L+mfAM_TRK_L+mfMD_TRK_L+mfPM_TRK_L+mfEV_TRK_L",
                    "result": None,
                    "constraint": {
                        "by_value": None,
                        "by_zone": None
                    },
                    "aggregation": {
                        "origins": "+",
                        "destinations": "+"
                    },
                    "type": "MATRIX_CALCULATION"
                }
                spec8 = {
                    "expression": "mfEA_TRK_L+mfAM_TRK_L+mfMD_TRK_L+mfPM_TRK_L+mfEV_TRK_L+mfEA_TRK_M+mfAM_TRK_M+mfMD_TRK_M+mfPM_TRK_M+mfEV_TRK_M+mfEA_TRK_H+\
                                   mfAM_TRK_H+mfMD_TRK_H+mfPM_TRK_H+mfEV_TRK_H",
                    "result": None,
                    "constraint": {
                        "by_value": None,
                        "by_zone": None
                    },
                    "aggregation": {
                        "origins": "+",
                        "destinations": "+"
                    },
                    "type": "MATRIX_CALCULATION"
                }        
                report4 = matrix_calc([spec7, spec8], scenario = scenario) 
                LtTrkProp_list.append(report4[0]['sum']/report4[1]['sum'])
            '''

        # total VMT    
        # df_totalvmt = pd.read_csv(_join(target_path, 'inputs', 'region_base_year_dvmt.csv'))    
        # df_totalvmt = df_totalvmt.append({'HvyTrkDvmt': round(total_vmt,2)}, ignore_index = True)
        # df_totalvmt['HvyTrkDvmtGrowthBasis'] = 'Income'
        # df_totalvmt['ComSvcDvmtGrowthBasis'] = 'Population'
        # df_totalvmt = df_totalvmt.fillna("")
        # df_totalvmt.to_csv(_join(target_path, 'inputs', 'region_base_year_dvmt.csv'), index = False)     
    
    if year == 2016: 
        # total heavy truck vmt
        df_temp = pd.read_csv(_join(target_path, 'inputs', 'region_base_year_dvmt.csv'))    
        df_totalvmt = pd.DataFrame(columns=df_temp.columns)
        df_totalvmt = df_totalvmt.append({'HvyTrkDvmt': round(total_vmt,2)}, ignore_index = True)
        df_totalvmt['StateAbbrLookup'] = 'CA'
        df_totalvmt['HvyTrkDvmtGrowthBasis'] = 'Income'
        df_totalvmt['ComSvcDvmtGrowthBasis'] = 'Population'
        df_totalvmt = df_totalvmt.fillna("")
        df_totalvmt.to_csv(_join(target_path, 'inputs', 'region_base_year_dvmt.csv'), index = False)         

        df_vmtEMME = pd.DataFrame(proportion_list)
        #df_vmtEMME.to_csv('df_vmtEMME.csv')
        df_rdtp_vmt = df_vmtEMME.groupby(df_vmtEMME.index // 5).sum()  #Extrac vmt by road type and area type
        fwy_vmt = df_vmtEMME.iloc[[0,3,6,9,12]].sum().tolist()   
        arterial_vmt = df_vmtEMME.iloc[[1,4,7,10,13]].sum().tolist()       
        other_vmt = df_vmtEMME.iloc[[2,5,8,11,14]].sum().tolist()     

        df_vmtEMME_NM = pd.DataFrame(NMproportion_list)
        #df_vmtEMME_NM.to_csv('df_vmtEMME_NM.csv')
        nmfwy_vmt = df_vmtEMME_NM.iloc[[0,3,6,9,12]].sum().tolist()   
        nmarterial_vmt = df_vmtEMME_NM.iloc[[1,4,7,10,13]].sum().tolist()       
        nmother_vmt = df_vmtEMME_NM.iloc[[2,5,8,11,14]].sum().tolist()              
        
        df_temp = pd.read_csv(_join(target_path, 'inputs', 'marea_dvmt_split_by_road_class.csv'))
        df_vmtsp = pd.DataFrame(columns=df_temp.columns)       
        df_vmtsp = df_vmtsp.append({'Geo': Marea_List[0]}, ignore_index=True) 
        df_vmtsp['LdvFwyDvmtProp'][0] = round(fwy_vmt[0]/(fwy_vmt[0] + arterial_vmt[0] + other_vmt[0]), 8)
        df_vmtsp['LdvArtDvmtProp'][0] = round(arterial_vmt[0]/(fwy_vmt[0] + arterial_vmt[0] + other_vmt[0]), 8)
        df_vmtsp['LdvOthDvmtProp'][0] = round(other_vmt[0]/(fwy_vmt[0] + arterial_vmt[0] + other_vmt[0]), 8)
        df_vmtsp['HvyTrkFwyDvmtProp'][0] = round(fwy_vmt[1]/(fwy_vmt[1] + arterial_vmt[1] + other_vmt[1]), 8)
        df_vmtsp['HvyTrkArtDvmtProp'][0] = round(arterial_vmt[1]/(fwy_vmt[1] + arterial_vmt[1] + other_vmt[1]), 8)  
        df_vmtsp['HvyTrkOthDvmtProp'][0] = round(other_vmt[1]/(fwy_vmt[1] + arterial_vmt[1] + other_vmt[1]), 8)
        df_vmtsp['BusFwyDvmtProp'][0] = round(fwy_vmt[2]/(fwy_vmt[2] + arterial_vmt[2] + other_vmt[2]), 8)
        df_vmtsp['BusArtDvmtProp'][0] = round(arterial_vmt[2]/(fwy_vmt[2] + arterial_vmt[2] + other_vmt[2]), 8)
        df_vmtsp['BusOthDvmtProp'][0] = round(other_vmt[2]/(fwy_vmt[2] + arterial_vmt[2] + other_vmt[2]), 8)

        df_vmtsp = df_vmtsp.append({'Geo': Marea_List[1]}, ignore_index=True) 
        df_vmtsp['LdvFwyDvmtProp'][1] = round(nmfwy_vmt[0]/(nmfwy_vmt[0] + nmarterial_vmt[0] + nmother_vmt[0]), 8)
        df_vmtsp['LdvArtDvmtProp'][1] = round(nmarterial_vmt[0]/(nmfwy_vmt[0] + nmarterial_vmt[0] + nmother_vmt[0]), 8)
        df_vmtsp['LdvOthDvmtProp'][1] = round(nmother_vmt[0]/(nmfwy_vmt[0] + nmarterial_vmt[0] + nmother_vmt[0]), 8)
        df_vmtsp['HvyTrkFwyDvmtProp'][1] = round(nmfwy_vmt[1]/(nmfwy_vmt[1] + nmarterial_vmt[1] + nmother_vmt[1]), 8)
        df_vmtsp['HvyTrkArtDvmtProp'][1] = round(nmarterial_vmt[1]/(nmfwy_vmt[1] + nmarterial_vmt[1] + nmother_vmt[1]), 8)  
        df_vmtsp['HvyTrkOthDvmtProp'][1] = round(nmother_vmt[1]/(nmfwy_vmt[1] + nmarterial_vmt[1] + nmother_vmt[1]), 8)
        df_vmtsp['BusFwyDvmtProp'][1] = round(nmfwy_vmt[2]/(nmfwy_vmt[2] + nmarterial_vmt[2] + nmother_vmt[2]), 8)
        df_vmtsp['BusArtDvmtProp'][1] = round(nmarterial_vmt[2]/(nmfwy_vmt[2] + nmarterial_vmt[2] + nmother_vmt[2]), 8)
        df_vmtsp['BusOthDvmtProp'][1] = round(nmother_vmt[2]/(nmfwy_vmt[2] + nmarterial_vmt[2] + nmother_vmt[2]), 8)        
        df_vmtsp.to_csv(_join(target_path, 'inputs', 'marea_dvmt_split_by_road_class.csv'), index = False)  
        
        df_temp = pd.read_csv(_join(target_path, 'inputs', 'marea_base_year_dvmt.csv'))
        df_vmt = pd.DataFrame(columns=df_temp.columns)
        df_vmt = df_vmt.append({'Geo': Marea_List[0]}, ignore_index=True) 
        df_vmt['UzaNameLookup'][0] = 'San Diego/CA'
        df_vmt['UrbanLdvDvmt'][0] = fwy_vmt[0] + arterial_vmt[0] + other_vmt[0]
        df_vmt['UrbanHvyTrkDvmt'][0] = fwy_vmt[1] + arterial_vmt[1] + other_vmt[1]
        df_vmt = df_vmt.append({'Geo': Marea_List[1]}, ignore_index=True) 
        df_vmt['UzaNameLookup'][1] = 'San Diego/CA'
        df_vmt['UrbanLdvDvmt'][1] = 0
        df_vmt['UrbanHvyTrkDvmt'][1] = 0
        df_vmt.to_csv(_join(target_path, 'inputs', 'marea_base_year_dvmt.csv'), index = False)

df = pd.read_csv(_join(target_path, 'inputs', 'marea_lane_miles.csv'))
# df_ComSvcLtTrkProp = pd.read_csv(_join(target_path, 'inputs', 'region_comsvc_lttrk_prop.csv'))
#df = df.set_index('Year')
l = 0
for year, scenario_name in scenario_list:
    df['FwyLaneMi'][(df.Year == year) & (df.Geo == Marea_List[0])] = lanemile_list[2*l+l][0]
    df['ArtLaneMi'][(df.Year == year) & (df.Geo == Marea_List[0])] = lanemile_list[2*l+l+1][0]
    df['FwyLaneMi'][(df.Year == year) & (df.Geo == Marea_List[1])] = NMlanemile_list[2*l+l][0]
    df['ArtLaneMi'][(df.Year == year) & (df.Geo == Marea_List[1])] = NMlanemile_list[2*l+l+1][0]
    # df_ComSvcLtTrkProp['ComSvcLtTrkProp'][df_ComSvcLtTrkProp.Year == year] = round(LtTrkProp_list[l],2)
    l += 1
df.to_csv(_join(target_path, 'inputs', 'marea_lane_miles.csv'), index = False)         
# df_ComSvcLtTrkProp.to_csv(_join(target_path, 'inputs', 'region_comsvc_lttrk_prop.csv'), index = False)    
    
print ("Done!")