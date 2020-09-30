import pandas as pd
import numpy as np
import json

import os
wd = "C:\\Users\\Daniel\\Google Drive\\Projects\\2020.01 Yale's Most Popular Courses\\raw-data"
os.chdir(wd)

def attempt_rating(x, name):
    try:
        return x['same_both'][name]
    except:
        try: 
            return x['same_class'][name]
        except:
            try:
                return x['same_professors'][name]
            except:
                return np.nan
            
def get_rating(x):
    return attempt_rating(x, 'rating')

def get_workload(x):
    return attempt_rating(x, 'workload')

# do basic proccessing
ct = pd.read_json("coursetable_202001.json")
ct = ct[['subject', 'number', 'section', 'times', 'locations_summary', 'areas', 'skills', 'average']]
ct = ct.rename(columns = {'locations_summary': 'locations'})
ct['times'] = [elem['summary'] for elem in ct['times']]
ct['rating'] = ct.average.apply(get_rating)
ct['workload'] = ct.average.apply(get_workload)

coursetable = ct.drop(columns = ['average', 'areas', 'skills'])
coursetable.to_csv('coursetable.csv', index=False)