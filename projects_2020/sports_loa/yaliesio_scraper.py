import requests
import pandas as pd

CSV_NAME = "yc_loa.csv"

headers = {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MDE1OTYzMTMsImV4cCI6MTYzMzEzMjMxMywic3ViIjoiZGQ4MzgifQ.uZnVMZweV0V_iV0u2FMgrYtJkKQx6a0T5Fwhwc1VWxI"}
endpoint = "https://yalies.io/api/students"

# sends a POST request to yaliesio for ALL students in database
# returns a list of JSON elements with each element representing 1 entry in Yale FaceBook
res = requests.post(endpoint, json={"query": "", "filters": {}}, headers=headers).json()

# take this list of JSON entries and turn it into a pandas dataframe where each key in the JSON structure is a column
df = pd.json_normalize(res)


# now we should figure out how to deal with potential athletes who have the same name as someone else in Yale college
# Using class year should be a pretty way to designate between people w/ the same names (lets call them clones) but
# let's not be too super confident 


# get list of people with same first name AND last name
clones = df[df.duplicated(['first_name', 'last_name'], keep=False)]
print("Number of clones: ", len(clones))

# find number of clones who are in the same class, hopefully there won't be a lot and hopefully non of them are athletes
clones_same_year = df[df.duplicated(['first_name', 'last_name', 'year'], keep=False)]
print("Number of clones in the same class: ", len(clones_same_year))

# only 19, we're probably good, as of writing this, we don't have the full updated yale athletics roster scraped
# so I'll still mark the same year clones

# make new column called "dup_year_name" that contains `True` if the person shares the same name with
# someone else in their class and `False` otherwise  
df['dup_year_name'] = df.index.isin(clones_same_year.index)

# combine the first_name and last_name columns to make a single 'full_name' column
df['full_name'] = df['first_name'] + " " + df['last_name']

# keep only the important columns
df = df[['full_name', 'year', 'leave', 'dup_year_name']]

# drop our newly cleaned LoA data into a csv
df.to_csv(CSV_NAME, index=False)
print("Created {}!".format(CSV_NAME))