import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns
import csv

from urllib.request import urlopen 
from bs4 import BeautifulSoup

url = "http://catalog.yale.edu/ycps/majors-in-yale-college/"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')

all_links = soup.find_all('a')
major_links = []

for link in all_links: 
    if link.has_attr('href'):
        major_links.append(link.attrs['href'])

major_links = major_links[23:103]
link_header = 'http://catalog.yale.edu'

with open('major_prerequisites.csv', mode='w') as major_file: 
    major_writer = csv.writer(major_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for major in major_links: 
        major_url = link_header + major
        html_major = urlopen(major_url) 
        soup_major = BeautifulSoup(html_major, 'lxml')

        prereq_tag = soup_major.find('p', class_='rotmCategoryText')

        if prereq_tag == None: 
            if major.endswith('/'):
                major_writer.writerow([major[30:-1], 'NONE'])
            else:
                major_writer.writerow([major[30:], 'NONE'])
        else:
            prereq_list = prereq_tag.find_all('a', class_='bubblelink code')

            for prereq in prereq_list: 
                text_only = prereq.text
                if text_only[0].isdigit(): 
                    full_course = coursecode + ' ' + prereq.text
                    if major.endswith('/'): 
                        major_writer.writerow([major[30:-1], full_course])
                    else: 
                        major_writer.writerow([major[30:], full_course])
                else:
                    if major.endswith('/'): 
                        major_writer.writerow([major[30:-1], prereq.text])
                    else:
                        major_writer.writerow([major[30:], prereq.text])
                    coursecode = prereq.text[0:4]

major_file.close()