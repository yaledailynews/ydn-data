# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 16:05:34 2022

@author: antho
"""

import requests
from bs4 import BeautifulSoup as bs

Engl_URL = "https://english.yale.edu/graduate-program/student-directory"
Engl_page = requests.get(Engl_URL)

Engl_soup = bs(Engl_page.content, "html.parser")

Engl_table = Engl_soup.find_all("td", class_="views-field views-field-name")

for Engl_table_elements in Engl_table:
    links = Engl_table_elements.find_all("a")
    for link in links:
        link_url = link["href"] 
        print(link.text.strip())
        
Ital_URL = "https://italian.yale.edu/people/graduate-students" 
Ital_page = requests.get(Ital_URL)

Ital_soup = bs(Ital_page.content, "html.parser")

Ital_table  = Ital_soup.find_all("td", class_="views-field views-field-name")

for Ital_table_elements in Ital_table:
    links = Ital_table_elements.find_all("a")
    for link in links:
        link_url = link["href"] 
        print(link.text.strip())
        
Afr_Stu_URL = "https://african.macmillan.yale.edu/people/current-students"
Afr_Stu_page = requests.get(Afr_Stu_URL)

Afr_Stu_soup = bs(Afr_Stu_page.content, "html.parser")

Afr_Stu_table = Afr_Stu_soup.find_all("td", class_="views-field views-field-name")

for Afr_Stu_table_elements in Afr_Stu_table:
    links = Afr_Stu_table_elements.find_all("a")
    for link in links:
        link_url = link["href"] 
        print(link.text.strip())


