from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from pyvirtualdisplay import Display
import gspread


DASHBOARD_URL = "https://app.powerbi.com/view?r=eyJrIjoiODU1ZmZmNGMtYzMwMy00M2FjLWJkMmMtYTRlMGI3NzU3M2Y0IiwidCI6ImRkOGNiZWJiLTIxMzktNGRmOC1iNDExLTRlM2U4N2FiZWI1YyIsImMiOjF9"
SHEETS_URL = "https://docs.google.com/spreadsheets/d/14GY3gnoUgsS5b26H0xXXQvyB3xXhAFBj4-lXxhtcWw0"

# XPATHS
XPATH_TABLE = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[1]/transform/div"
XPATH_DATES = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[1]/transform/div/div[3]/div/visual-modern/div/div/div[2]/div[1]/div[2]"
XPATH_DATA = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[1]/transform/div/div[3]/div/visual-modern/div/div/div[2]/div[1]/div[4]/div/div"
XPATH_POP = "//*[@id=\"pvExplorationHost\"]/div/div/exploration/div/explore-canvas-modern/div/div[2]/div/div[2]/div[2]/visual-container-repeat/visual-container-modern[1]/transform/div/div[3]/div/visual-modern/div/div/div[2]/div[1]/div[3]/div"

# SPREADSHEET CONSTS
DATE_COL = 1

scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('/home/pi/Documents/yale_covid_scrape/service_account.json', scope)
client = gspread.authorize(creds)

# gc = gspread.service_account("service_account.json", scope)
# gc = gspread.oauth(scope)
doc = client.open_by_url(SHEETS_URL)
# sheet for new format with on/off campus location
s = doc.worksheet("Location")

display = Display(visible=0, size=(800,600))
display.start()

driver = webdriver.Firefox()

driver.get(DASHBOARD_URL)

sleep(1)

try:
    # wait until the data has loaded
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, XPATH_TABLE))
    )

    print("Table succesfully loaded!")
    
    sleep(10)

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
        
        onCampusUnderGradTest = dayData[4].text
        onCampusUnderGradPos = dayData[5].text

        offCampusUnderGradTest = dayData[7].text
        offCampusUnderGradPos = dayData[8].text

        gradTest = dayData[10].text
        gradPos = dayData[11].text

        facultyTest = dayData[13].text
        facultyPos = dayData[14].text

        monthDay = datetime.strptime(datesList[col], '%b %d')
        fullDatetime = datetime(year=datetime.today().year,
                                month=monthDay.month,
                                day=monthDay.day)
        row_date = fullDatetime.strftime("%m/%d/%Y")
        row_entry = [row_date, onCampusUnderGradTest, onCampusUnderGradPos, offCampusUnderGradTest, offCampusUnderGradPos, gradTest, gradPos, facultyTest, facultyPos]


        start_cell = None

        # data already entered, check if it's still accurate
        if row_date in s.col_values(DATE_COL):
            row_index = s.col_values(DATE_COL).index(row_date) + 1
            if s.row_values(row_index) != row_entry:
                print("Updating Row: ", row_entry)
                start_cell = gspread.utils.rowcol_to_a1(row_index, DATE_COL)

        # new data
        else:
            print("Adding Row: ", row_entry)
            start_cell = gspread.utils.rowcol_to_a1(len(s.col_values(DATE_COL)) + 1, DATE_COL)
        
        if start_cell is not None:
            s.update(start_cell, [[cell] for cell in row_entry], major_dimension='columns')   


except Exception as e:
    print(e)

finally:
    display.stop()
    driver.quit()

print("Done updating spreadsheet!")
