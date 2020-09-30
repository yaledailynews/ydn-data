from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select

# setwd
import os
wd = "C:\\Users\\Daniel\\Google Drive\\Projects\\2020.01 Yale's Most Popular Courses\\raw-data"
os.chdir(wd)

# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import numpy as np

# Set url here
url = 'https://ivy.yale.edu/course-stats/'

# Set Chrome options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# Open webdriver
driver = webdriver.Chrome(chrome_options = options)
driver.get(url)

# GET LIST OF SUBJECTS

subjects_names = []
subjects_codes = []
subjects_elems = driver.find_elements_by_css_selector("#subjectCode option")

for elem in subjects_elems[1:]: # first element is blank
    texts = elem.text.split(" - ", 2)
    subjects_codes.append(texts[0])
    subjects_names.append(texts[1])

df_subjects = pd.DataFrame({'subject': subjects_codes, 
                            'name': subjects_names})
df_subjects.to_csv('subjects.csv', index = False)
# df_subjects.head(10)

# GET LIST OF DATE

dropdown = Select(driver.find_element_by_id("subjectCode"))
dropdown.select_by_value("AMTH") # since AMTH definitely isn't a blank table

dates_table = driver.find_element_by_css_selector("table table").find_elements_by_css_selector("td")
dates_headers = []
for elem in dates_table:
    dates_headers.append(elem.text.strip())
    
# np.array(dates_headers) # use nparray to show on one line

# SCRAPE DEMAND

courses_ids = []
courses_codes = []
courses_names = []

demand_ids = []
demand_codes = []
demand_dates = []
demand_counts = []

i = 1

for subject in subjects_codes:
    dropdown = Select(driver.find_element_by_id("subjectCode"))
    dropdown.select_by_value(subject)
    sleep(2)

    courses = driver.find_elements_by_css_selector("div#content > div > table > tbody > tr")
    
    for course in courses:
        code = course.find_element_by_css_selector("td a").text.strip()
        name = course.find_element_by_css_selector("td span").text.strip()

        full_strings_all = code.split("/") # a list with each possible cross-listed code
        full_strings = [s for s in full_strings_all if s.split(" ")[0] in subjects_codes]
        code_this_subject = [s for s in full_strings if subject in s][0]
        
        if full_strings.index(code_this_subject) == 0:
            for string in full_strings:
                courses_ids.append(i)
                courses_codes.append(string)
                courses_names.append(name)
            
            demands_containers = course.find_elements_by_css_selector("td.trendCell")

            for j in range(len(dates_headers)):
                demand_ids.append(i)
                demand_codes.append(code_this_subject)
                demand_dates.append(dates_headers[j])
                demand_counts.append(demands_containers[j].text.strip())
     
        i += 1

# WRITE TO CSV

df_courses = pd.DataFrame({'id': courses_ids, 
                           'code': courses_codes, 
                           'name': courses_names})
df_demand = pd.DataFrame({'id': demand_ids,
                          'date': demand_dates,
                          'count': demand_counts})

df_courses.to_csv('courses.csv', index = False)
df_demand.to_csv('demand.csv', index = False)