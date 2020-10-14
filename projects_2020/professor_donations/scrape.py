from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import time
import csv

options = ChromeOptions()
options.add_argument('headless')
# must have chromedriver in path
driver = Chrome("/home/thomas/Dropbox/chromedriver")


def get_url(search_str):
    return "https://directory.yale.edu/?queryType=field&lastname=" + search_str + "&title=professor"


def search(original_search_str, professors_scraped, writer):
    for letter in range(ord("a"), ord("z")+1):
        letter = chr(letter)
        search_str = original_search_str + letter
        driver.get(get_url(search_str))
        while driver.find_element_by_id("loading-indicator").value_of_css_property("display") != "none":
            time.sleep(0.05)
        for element in driver.find_elements_by_css_selector("article.directory_item"):
            if element.get_attribute("id") == "bpa-final-result-article":
                continue
            try:
                info = {}
                for content in element.find_elements_by_css_selector(".directory_item_detail_content"):
                    try:
                        link = content.find_element_by_css_selector("a")
                        if "@" in link.text:
                            info["email"] = link.text
                    except NoSuchElementException:
                        if "+" not in content.text:
                            info["department"] = content.text
                            break
                info["name"] = element.find_element_by_class_name("bps-result-name").text
                info["title"] = element.find_element_by_class_name("bps_title").text
                immutable_info = tuple(sorted(info.items()))
                if immutable_info not in professors_scraped:
                    professors_scraped.add(immutable_info)
                    writer.writerow(info)
            except Exception as e:
                print(e)
        if driver.find_element_by_class_name("alert-message").text:
            search(search_str, professors_scraped, writer)
    return professors_scraped


f = open("professors_and_lecturers.csv", "w")
writer = csv.DictWriter(f, fieldnames=["name", "title", "email", "department"])
writer.writeheader()
search("", set(), writer)
f.close()
driver.quit()