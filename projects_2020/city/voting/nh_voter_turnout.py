from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd


driver = webdriver.Chrome()
driver.get("https://ctemspublic.pcctg.net/")

election_select = Select(driver.find_element_by_name("ddlElection"))

all_nhelection_data = []

for options in election_select.options[2:]:
    sleep(0.5)
    print("----------------------------{}----------------------------".format(options.text))
    options.click()

    # wait for voter turnout to be available and click on it
    try:
        sleep(0.5)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(((By.NAME, "statewide"))))
        
        driver.find_element_by_name("statewide").click()
        print("clicked statewide")
        

        sleep(0.5)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(((By.NAME, "voterTurnout"))))
        
        driver.find_element_by_name("voterTurnout").click()
        print("clicked turnout")
        
        sleep(0.5)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dvVoterTurnout_Summary"))
        )
        
        print("turnout table loaded")
    except:
        driver.quit()

    

    # grab the html for this specific election and parse it using beautifulsoup
    soup = BeautifulSoup(driver.page_source, "html.parser") 

    # grab the row in the table that has the New Haven Data 
    nh_row = soup.find("div", id="dvVoterTurnout_Summary").find("a", text="New Haven")

    # check if a new haven entry is even there
    if nh_row is None:
        continue
    
    # if there is an entry, go up 2 levels so we grab the table from the data at this row
    nh_row = nh_row.parent.parent

    # get all the voter data for this specific election
    data_list = [options.text]
    for td in nh_row.find_all("td")[2:]:
        data_list.append(td.text)

    # append to master list
    all_nhelection_data.append(data_list)


data = pd.DataFrame(all_nhelection_data,
columns=["Election", "ELIGIBLE VOTERS IN THE TOWN", "NUMBER OF VOTERS VOTED IN THE TOWN",
    "NUMBER OF ABSENTEE BALLOT RECEIVED", "NUMBER OF ABSENTEE BALLOT COUNTED",
    "NUMBER OF EDR ISSUED", "NUMBER OF EDR COUNTED", "TURNOUT"])

data.to_csv("nh_voting.csv")
