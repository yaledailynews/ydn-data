from selenium import webdriver
from bs4 import BeautifulSoup
from string import ascii_lowercase


class Directory:
    def __init__(self, driver_path="./chromedriver") -> None:
        self.alphabet = list(ascii_lowercase)
        self.name_trips = [
            f"{first}{second}{third}"
            for first in self.alphabet
            for second in self.alphabet
            for third in self.alphabet
        ]
        self.driver = webdriver.Chrome(driver_path)
        self.driver.get("https://directory.yale.edu/advanced")

    def search_directory(self, school, name):
        self.driver.get(f"https://directory.yale.edu/?queryType=field&firstname={name}&school={school}")
        html_source_code = self.driver.execute_script("return document.body.innerHTML;")
        self.soup = BeautifulSoup(html_source_code, "html.parser")

    def max_reached(self):
        return "Your search returned more than the maximum number of listings that can be presented. Below are only the first 25 results."in self.soup.text

    def scrape_emails_from_site(self) -> list:
        s = self.soup.find_all("div", {"class": "directory_results_list"})[3]
        emails = [e.text for e in s.select("a") if "@" in e.text]
        return emails

    def scrape_school_emails_from_names(self, school, names) -> list:
        emails = []
        for name in names:
            self.search_directory(school, name)
            if self.max_reached():
                refined_names = [f"{name}{letter}" for letter in self.alphabet]
                refined_emails = self.scrape_school_emails_from_names(school, refined_names)
                return refined_emails
            else:
                emails += self.scrape_emails_from_site()
        return emails

    def scrape_school_emails(self, school):
        return self.scrape_school_emails_from_names(school, self.name_trips)


# import requests
# import cookiecache
# from bs4 import BeautifulSoup

# session = requests.Session()
# cookies =

# opener = build_opener(HTTPCookieProcessor())

# with urllib.request.urlopen('https://directory.yale.edu/?queryType=field&firstname=abc&school=GS') as response:
#    html = response.read()
#    print(html)
