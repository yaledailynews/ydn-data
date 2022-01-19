import pandas as pd
import numpy as np

import os
wd = "/Users/leonlufkin/Desktop/yale-most-popular-courses/raw-data"
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
ct = pd.read_json("coursetable_202201.json")
ct = ct[['subject', 'number', 'section', 'times_summary', 'locations_summary', 'areas', 'skills', 'average_rating', 'average_workload']]
ct = ct.rename(columns = {'locations_summary': 'locations', 'times_summary': 'times', 'average_rating': 'rating', 'average_workload': 'workload'})
# ct['times'] = [elem['summary'] for elem in ct['times_summary']]
# ct['rating'] = ct.average.apply(get_rating)
# ct['workload'] = ct.average.apply(get_workload)

coursetable = ct.drop(columns = ['areas', 'skills'])
coursetable.to_csv('coursetable.csv', index=False)