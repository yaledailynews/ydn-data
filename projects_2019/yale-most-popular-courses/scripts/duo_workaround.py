import sys
import os
import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import numpy as np
import pandas as pd

def getSubjects(fileName, driver: webdriver.Chrome):
    print("in getSubjects!")

    # get URL and pass to BeautifulSoup
    url = 'https://ivy.yale.edu/course-stats/'
    driver.get(url)
    html_source_code = driver.execute_script("return document.body.innerHTML;")
    s = BeautifulSoup(html_source_code, 'html.parser')

    # get all the dropdown options and split into subject code + subject name
    subjects_elems = s.select('#subjectCode option')
    subjects_codes = [elem.text.split(" - ", 2)[0] for elem in subjects_elems[1:]]
    subjects_names = [elem.text.split(" - ", 2)[1] for elem in subjects_elems[1:]]

    # make a dataframe and save it to csv
    pd.DataFrame({
        'subject': subjects_codes,
        'name': subjects_names
    }).to_csv(fileName, index=False)

    return subjects_codes

def getDates(sem, driver: webdriver.Chrome):
    # get URL and pass to BeautifulSoup
    # using AMTH as arbitary subject
    url = 'https://ivy.yale.edu/course-stats/?termCode=' + sem + '&subjectCode=AMTH'
    driver.get(url)
    time.sleep(15)
    html_source_code = driver.execute_script("return document.body.innerHTML;")
    s = BeautifulSoup(html_source_code, 'html.parser')

    # select date elements
    with open('getDates_debug.txt', 'w') as f:
        print(html_source_code, file=f)
    dates_elems = s.select('table')[0].select('tr')[0].select('th')
    dates = [date.text.strip() for date in dates_elems]
    print(dates)

    return dates[1:]

if __name__ == '__main__':
    start_time = datetime.now()

    # 1. Setup automated chrome browser
    # Be sure to check "remember me for 90 days" when logging into Duo Mobile
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://ivy.yale.edu/course-stats/")


    # 2. Set output directory -----
    # Be sure to escape '\' with another '\'

    outdir = "/Users/leonlufkin/Desktop/yale-most-popular-courses/raw-data"


    # 3. Set semester -----
    # Manually input or pass using command line arguments
    # Examples: 202001 = 2020 Spring, 201903 = 2019 Fall
    semester = '202201'

    if len(sys.argv) > 1:
        semester = str(sys.argv[1])


    # 4. Get list of subjects -----
    time.sleep(25) # sleeping to allow for user to log in
    subjects = getSubjects(outdir + '/subjects.csv', driver)


    # 5. Get the array of dates -----
    dates = getDates(semester, driver)
    print(dates)

    # 6. Scrape courses
    # Most of the code here is to deal with cross-listed courses, and to avoid having duplicate data

    courses = [] # containers for courses: format is id, code, name
    demands = [] # container for demand: format is id, date, count
    i = 2392 # iterator for assigning course id
    subject_counter = 120
    num_subjects = len(subjects)

    skip_flag = True
    for subject in subjects:
        # get URL and pass to BeautifulSoup
        if subject != 'HPM' and skip_flag:
            continue
        else:
            skip_flag = False
            

        # '.replace("&", "%26")' escapes the ampersand
        url = 'https://ivy.yale.edu/course-stats/?termCode=' + semester + '&subjectCode=' + subject.replace("&", "%26")
        driver.get(url)
        time.sleep(1.5)
        html_source_code = driver.execute_script("return document.body.innerHTML;")
        s = BeautifulSoup(html_source_code, 'html.parser')
        with open('subjects_debug.txt', 'w') as f:
            print(html_source_code, file=f)

        # selects all the courses info and demand info
        # each element in course_containers contains code, name, and demand for one course
        course_containers = s.select("div#content > div")[0].select('table > tbody > tr') # s.select("div#content > div > table > tbody > tr")
        # print(course_containers)

        for container in course_containers:
            # extract name and code
            code = container.select("td a")[0].text.strip().replace(";", "")
            name = container.select("td span")[0].text.strip().replace(";", "")
            # print(code)
            # print(name)

            # 'code' might be a long list of cross-listed couses (e.g. 'S&DS 262/S&DS 562/CPSC 262'),
            # so we need to split all of the codes and look at them separately
            full_strings_all = code.split("/")
            # print(full_strings_all)

            # sometimes we'll get a course code that isn't actually an academic subject,
            # so this line filters that out
            full_strings = [string.strip() for string in full_strings_all if string.strip().split(" ")[0] in subjects]
            # print(full_strings)

            # now, we need to identify the course code corresponding to the subject we're working
            # on in the loop — this finds the course code with 'subject' in it
            code_this_subject = [string for string in full_strings if subject in string][0]
            # print(code_this_subject)

            # Test if we've already added the demand for this course (due to cross-listing) into the 
            # data structure. We don't want duplicate data, so if we already have the demand, we simply skip it
            if full_strings.index(code_this_subject) == 0:
                # if this is our first time coming across this course, we need to add all of the
                # cross-listed course numbers into our 'courses' list
                for string in full_strings:
                    courses.append([i, string, name])

                # selects each of the individual counts
                # each element in count is one count corresponding to one day
                counts = container.select("td.trendCell")
                # print(len(dates))
                # print(len(counts))

                # add the count for each into our 'demands' list
                for j in range(len(dates)):
                    # there aren't any statistics for 1/11 for GSAS 903 01 for some reason
                    if code_this_subject == 'GSAS 903 01':
                        if j == 0:
                            demands.append([i, dates[j], '0'])    
                        else:
                            demands.append([i, dates[j], counts[j-1].text.strip()])    
                    else:
                        demands.append([i, dates[j], counts[j].text.strip()])
            
            i += 1

        print('Scraped ' + str(i) + ' courses up to ' + subject + ', ' + str(datetime.now() - start_time) + ' elapsed')

        subject_counter += 1

        if subject_counter%20 == 0 or subject_counter == num_subjects-1:
            # write courses to csv
            pd.DataFrame(
                courses,
                columns = ['id', 'code', 'name']
            ).to_csv(outdir + '/courses.csv', index = False)

            # write demand to csv
            pd.DataFrame(
                demands,
                columns = ['id', 'date', 'count']
            ).to_csv(outdir + '/demand.csv', index = False)
            print(f"finished saving after {subject_counter} subjects!")

    print('Complete, ' + str(datetime.now() - start_time) + ' elapsed')