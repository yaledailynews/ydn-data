from selenium.webdriver import Chrome, ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import time
import csv

options = ChromeOptions()
options.add_argument('headless')
# must have chromedriver in path
driver = Chrome("/Users/thomaswoodside/chromedriver")


def get_url(search_str):
    return "https://directory.yale.edu/?queryType=field&lastname=" + search_str + "&title=professor"


def search(original_search_str, professor_ids_scraped, writer):
    for letter in range(ord("a"), ord("z")+1):
        letter = chr(letter)
        search_str = original_search_str + letter
        driver.get(get_url(search_str))
        print(search_str)
        print(len(professor_ids_scraped))
        while driver.find_element_by_id("loading-indicator").value_of_css_property("display") != "none":
            time.sleep(0.05)
        #time.sleep(2)
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
                if "email" not in info:
                    info["email"] = ""

                # if "email" not in info:
                #     print(element.find_element_by_class_name("bps-result-name").text)
                #     continue
                info["name"] = element.find_element_by_class_name("bps-result-name").text
                info["title"] = element.find_element_by_class_name("bps_title").text
                if info["name"] + info["email"] not in professor_ids_scraped:
                    professor_ids_scraped.add(info["name"] + info["email"])
                    writer.writerow(info)
            except Exception as e:
                print(e)
        if driver.find_element_by_class_name("alert-message").text:
            search(search_str, professor_ids_scraped, writer)
    return professor_ids_scraped


f = open("professors.csv", "w")
writer = csv.DictWriter(f, fieldnames=["name", "title", "email", "department"])
writer.writeheader()
search("", set(), writer)
f.close()
driver.quit()