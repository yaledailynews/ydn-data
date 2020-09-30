import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import re

# Functions to extract ratings. Basically, keep trying until we get rating that's a valid number.

def attempt_rating(x, name):
    try:
        return x['same_class'][name]
    except:
        # try: 
        #     return x['same_class'][name]
        # except:
        #         return np.nan
        return np.nan
    


def get_rating(x):
    return attempt_rating(x, 'rating')

def get_workload(x):
    return attempt_rating(x, 'workload')

def graph_rw(ct, code):
    ratings = ct["rating"][ct["subject"] == code]
    workload = ct["workload"][ct["subject"] == code]
    comb = pd.concat([ratings, workload], axis=1)

    # comb = comb.sort_values(by=["workload"])
    print(comb)

    comb.plot.scatter(x="workload", y="rating")

    plt.title(code + " Courses Ratings vs Workload")
    plt.legend(loc="best")

    plt.show()

    pass

# get the json for the specific season
# https://coursetable.com/GetDataFile.php?season=202001

ct = pd.read_json("coursetable2020s.json")

ct = ct[['subject', 'number', 'section', 'times', 'locations_summary', 'areas', 'skills', 'average', 'evaluations', 'num_students']]
ct = ct.rename(columns = {'locations_summary': 'locations'})
ct['times'] = [elem['summary'] for elem in ct['times']]
ct['rating'] = ct.average.apply(get_rating)
ct['workload'] = ct.average.apply(get_workload)

# clean areas + skills
ct["areas"] = ct["areas"].apply(lambda x: ", ".join(x))
ct["skills"] = ct["skills"].apply(lambda x: x[0] if len(x) > 0 else [])
ct["Hu"] = ct["areas"].apply(lambda x: "Hu" in x)
ct["Sc"] = ct["areas"].apply(lambda x: "Sc" in x)
ct["So"] = ct["areas"].apply(lambda x: "So" in x)
ct["L"] = ct["skills"].apply(lambda x: "L" in x)
ct["QR"] = ct["skills"].apply(lambda x: "QR" in x) 
ct["WR"] = ct["skills"].apply(lambda x: "WR" in x)

course_rating_history = pd.DataFrame()
for index, row in ct.iterrows():
    
    # DEBUG BREAK
    break

    # skip grad courses
    if int(re.findall('\d+', row.number)[0]) > 500:
        continue

    print("Looking at course (" + str(index) + "): " + row.subject + str(row.number))
    # new row that contains just course name, number, date, and ranking for that date
    course_row = {'subject': row.subject, 'number': row.number}

    ### NOTE: This will overwrite previous values if multiple sections (should only affect workload)

    # go through previous classes taught by same professor
    for course in row.evaluations['same_both']:
        course_row['year'] = course['year']
        course_row['term'] = course['term']

        if 'average' in course.keys() and 'rating' in course['average'].keys():
            course_row['rating'] = course['average']['rating']
                    
        if 'average' in course.keys() and 'workload' in course['average'].keys():
            course_row['workload'] = course['average']['workload']

        # print("Same Both: " + row.subject + " " + str(row.number) + " " + str(course['year']) + course['term'])
        print(course_row)

        course_rating_history = course_rating_history.append(course_row, ignore_index=True)

    # go through previous classes
    for course in row.evaluations['same_class']:
        course_row['year'] = course['year']
        course_row['term'] = course['term']

        if 'average' in course.keys() and 'rating' in course['average'].keys():
            course_row['rating'] = course['average']['rating']
                    
        if 'average' in course.keys() and 'workload' in course['average'].keys():
            course_row['workload'] = course['average']['workload']

        # print("Same Both: " + row.subject + " " + str(row.number) + " " + str(course['year']) + course['term'])
        print(course_row)

        course_rating_history = course_rating_history.append(course_row, ignore_index=True)
    
    print()

print(course_rating_history)
print("Done mutating data")

coursetable_csv_name = "coursetable2020s_class.csv"
print("Dropping: " + coursetable_csv_name)

# graph_rw(ct, "CPSC")

# cpsc_ratings = ct["rating"][ct["subject"] == "CPSC"]
# cpsc_workload = ct["workload"][ct["subject"] == "CPSC"]

# cs_list = [cpsc_ratings, cpsc_workload]

# cs_ratings_workload = pd.concat(cs_list, axis=1)
# cs_ratings_workload = cs_ratings_workload.sort_values(by=["workload"])

# print(cs_ratings_workload)

# cs_ratings_workload.plot(x="workload", y="rating")

# plt.title("CPSC Courses Ratings vs Workload")
# plt.legend(loc="best")

# plt.show()

coursetable = ct.drop(columns = ['average', "evaluations"])
coursetable.to_csv(coursetable_csv_name, index=False)
# course_rating_history.to_csv('coursetable2019f_history.csv', index=False)