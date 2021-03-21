import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import csv

from urllib.request import urlopen 
from bs4 import BeautifulSoup

majors = ['applied-mathematics', 'applied-physics', 'architecture', 'art', 'astronomy',
            'astrophysics', 'biomedical-engineering', 'chemical-engineering', 'chemistry',
            'cognitive-science', 'computer-science-psychology', 'computing-arts', 'geology-geophysics',
            'east-asian-languages-literatures', 'ecology-evolutionary-biology', 'economics-mathematics',
            'electrical-engineering', 'electrical-engineering-computer-science', 'chemical-engineering', 
            'electrical-engineering', 'environmental-engineering', 'mechanical-engineering', 
            'environmental-studies', 'film-studies', 'french', 'italian', 'mathematics', 'mathematics-philosophy', 
            'mathematics-physics', 'molecular-biophysics-biochemistry', 'molecular-cellular-developmental-biology', 
            'neuroscience', 'physics', 'physics-geosciences', 'physics-philosophy', 'portuguese', 'psychology', 
            'russian', 'spanish', 'statistics', 'theater-studies']

prereq_dict = {}

for major in majors: 
    url = "http://catalog.yale.edu/ycps/subjects-of-instruction/" + major
    html = urlopen(url)

    soup = BeautifulSoup(html, 'lxml')
    
    course_links = soup.find_all('a', class_="bubbleline code")
    for i in range(len(course_links)):
        course_links[i] = course_links[i].text.strip()
    prereq_dict[major] = course_links

with open('major_prereqs.csv', mode='w') as prereq_file: 
    prereq_writer = csv.writer(prereq_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for major in majors: 
        prereq_dict[major].insert(major, 0)
        prereq_writer.writerow(prereq_dict[major])

