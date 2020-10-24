import requests
from bs4 import BeautifulSoup

URL = "https://covid19.columbia.edu/content/columbia-surveillance-testing-results"

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='table-3494')

week_results = results.findall('tr', class_='ng-scope')

for res in week_results:
    dates = res.find('td', class_='ng-binding ng-scope')
    students_tested = res.find('td', class_='ng-binding ng-scope')
    students_postive = res.find('td', class_='ng-binding ng-scope')
    facultystaff_tested = res.find('td', class_='ng-binding ng-scope')
    facultystaff_positive = res.find('td', class_='ng-binding ng-scope')
# unsure about extracting the text from HTML elements as all of the labels seem to be the same when I inspect element
    if None in (dates, students_tested, students_postive, facultystaff_tested, facultystaff_positive):
        continue
    print(dates)
    print(students_tested)
    print(students_postive)
    print(facultystaff_tested)
    print(facultystaff_positive)
    print()

