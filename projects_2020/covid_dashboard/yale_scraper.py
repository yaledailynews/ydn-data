from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


DASHBOARD_URL = "https://app.powerbi.com/view?r=eyJrIjoiZjA4YThmNTgtYTc2My00N2JhLTgzNmQtNWI5MjEwMTQzMTRlIiwidCI6ImRkOGNiZWJiLTIxMzktNGRmOC1iNDExLTRlM2U4N2FiZWI1YyIsImMiOjF9&pageName=ReportSection6dffac37686d834a1306"
SHEETS_URL = "https://docs.google.com/spreadsheets/d/14GY3gnoUgsS5b26H0xXXQvyB3xXhAFBj4-lXxhtcWw0"

# XPATHS
XPATH_TABLE = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[1]/transform/div"
XPATH_DATES = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[1]/transform/div/div[3]/div/visual-modern/div/div/div[2]/div[1]/div[2]"
XPATH_DATA = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[1]/transform/div/div[3]/div/visual-modern/div/div/div[2]/div[1]/div[4]/div/div"
XPATH_POP = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[1]/transform/div/div[3]/div/visual-modern/div/div/div[2]/div[1]/div[3]/div"

scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('service_account.json', scope)
client = gspread.authorize(creds)

# gc = gspread.service_account("service_account.json", scope)
# gc = gspread.oauth(scope)
doc = client.open_by_url(SHEETS_URL)
s = doc.sheet1
LAST_DATE = datetime.strptime(s.col_values(1)[-1], "%m/%d/%Y")

driver = webdriver.Chrome()
driver.get(DASHBOARD_URL)

sleep(1)

try:
    # wait until the data has loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, XPATH_TABLE))
    )

    print("Table succesfully loaded!")

    # get the dates
    datesRow = driver.find_element_by_xpath(XPATH_DATES)
    datesList = list(map(lambda x : x.strip(' \n'), datesRow.text.split('\n')))[0:7]

    data = driver.find_element_by_xpath(XPATH_DATA)
    dataHTML = data.get_attribute("innerHTML")

    popColumn = driver.find_element_by_xpath(XPATH_POP)
    popList = list(map(lambda x : x.strip(' \n'), popColumn.text.split('\n')))

    dataSoup = BeautifulSoup(dataHTML, 'html.parser')

    for col in range(0, 7):
        # new day
        dayData = list(list(dataSoup.children)[col].children)

        underGradTest = dayData[4].text
        underGradPos = dayData[5].text

        gradTest = dayData[7].text
        gradPos = dayData[8].text

        facultyTest = dayData[10].text
        facultyPos = dayData[11].text

        monthDay = datetime.strptime(datesList[col], '%b %d')
        fullDatetime = datetime(year=datetime.today().year,
                                month=monthDay.month,
                                day=monthDay.day)
        row_date = fullDatetime.strftime("%m/%d/%Y")
        
        if (fullDatetime > LAST_DATE):
            row_entry = [row_date, underGradTest, underGradPos, gradTest, gradPos, facultyTest, facultyPos]
            print("Adding Row: ", row_entry)
            s.append_row(row_entry)


except Exception as e:
    print(e)
    driver.quit()

print("Done updating spreadsheet!")
driver.quit()