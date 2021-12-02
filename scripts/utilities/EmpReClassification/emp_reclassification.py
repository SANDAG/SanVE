# -*- coding: utf-8 -*-
"""
Employment Re-Classification

This SANDAG ABM specific module classified exisitng employments
in mgra input to fit VE employment requirement. The classification
is identical to ActivitySim employment classification.

@author: jyen
"""

import pandas as pd


def emp_rec(mgra):
    # Mapping other / retail sector
    keep_emp_cols = {
        'RetEmp': ['emp_retail', 'emp_personal_svcs_retail'],                                           
        'OtherEmp': ['emp_ag', 'emp_const_non_bldg_prod', 'emp_utilities_prod',
                     'emp_const_bldg_prod', 'emp_mfg_prod', 'emp_trans', 'emp_fed_mil']
    }
    
    # Creating employment columns
    for col in keep_emp_cols.keys():
        sandag_cols = keep_emp_cols[col]
        mgra[col] = mgra[sandag_cols].sum(axis=1)
    
    # Other employment, not included in keep_emp_cols
    col_series = pd.Series(mgra.columns)
    all_emp_cols = col_series[col_series.str.startswith('emp_')]
    service_emp_cols = list(set(list(all_emp_cols)).difference(sum(list(keep_emp_cols.values()), [])))
    service_emp_cols.remove('emp_total')
    mgra['SvcEmp'] = mgra[service_emp_cols].sum(axis=1) #OtherEmp will not be in the output
    
    # Check if the service emp + retail emp + other emp = total emp
    if (mgra['RetEmp'] + mgra['SvcEmp'] + mgra['OtherEmp']).equals(mgra['emp_total']):
        print('pass')
    else:
        print('check service / retail emp / other emp')
        
    return mgra

