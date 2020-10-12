import re
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

loa_directory = pd.read_csv("yc_loa.txt")

# these rosters are updated: soccer, squash, tennis (all women's)
# these WOMEN'S rosters are NOT updated: softball, swimming & diving, tennis, track & field 
# these MEN'S rosters are NOT updated: baseball, basketball, heavyweight crew, lightweight crew

updated_teams = [["womens_soccer", "https://yalebulldogs.com/sports/womens-soccer/roster"],
                 ["womens_squash", "https://yalebulldogs.com/sports/womens-squash/roster"],
                 ["womens_volleyball", "https://yalebulldogs.com/sports/womens-volleyball/roster"]]

outdated_teams = [["womens_softball", "https://yalebulldogs.com/sports/softball/roster"],
                  ["womens_swimming_diving", "https://yalebulldogs.com/sports/womens-swimming-and-diving/roster"],
                  ["womens_tennis", "https://yalebulldogs.com/sports/womens-tennis/roster"],
                  ["womens_track_field", "https://yalebulldogs.com/sports/womens-track-and-field/roster"],
                  ["mens_baseball", "https://yalebulldogs.com/sports/baseball/roster"],
                  ["mens_basketball", "https://yalebulldogs.com/sports/mens-basketball/roster"],
                  ["mens_heavyweight_crew", "https://yalebulldogs.com/sports/mens-crew/roster"],
                  ["mens_lightweight_crew", "https://yalebulldogs.com/sports/mens-rowing/roster"]]

# regex filter for alphabet + some other characters
regex = re.compile("[^a-zA-Z,. ]")

# dictionary for converting academic year to graduation year
convert_year = {"Fy." : 2024,
                "So." : 2023,
                "Jr." : 2022,
                "Sr." : 2021}

for team in updated_teams + outdated_teams:
    page = requests.get(team[1])
    soup = bs(page.content, "html.parser")
    
    # names: find text, apply regex filter, then strip
    all_names = soup.find_all("div", class_ = "sidearm-roster-player-name")
    all_names = [regex.sub("", name.text).strip() for name in all_names]
    
    # repeat for academic year, but use convert_year to get graduation year
    all_years = soup.find_all("span", class_ = "sidearm-roster-player-academic-year")
    all_years = [regex.sub("", year.text).strip() for year in all_years]
    
    # for some reason, we get duplicate years and hometowns. lets just take every other element
    all_years = all_years[::2]
    
    # convert academic year to graduation year. note that this year will be incorrect if the roster is outdated, but this will be corrected when we merge with the loa csv
    all_years = [convert_year[yr] for yr in all_years] 
    
    # repeat for hometowns
    all_hometowns = soup.find_all("span", class_ = "sidearm-roster-player-hometown")
    all_hometowns = [regex.sub("", hometown.text).strip() for hometown in all_hometowns]
    all_hometowns = all_hometowns[::2]
    
    # zip all player information and convert to list
    team[1] = [list(a) for a in zip(all_names, all_years, all_hometowns)]
    
    # create pandas dataframe with correct column names
    df = pd.DataFrame(team[1], columns = ["full_name", "year", "hometown"])
    
    # flag outdated rosters
    if team in outdated_teams:
        df["outdated"] = True
    else:
        df["outdated"] = False                       
                            
    # inner merge with loa csv
    df = df.merge(loa_directory, on = "full_name", how = "inner")
    
    # rearrange and rename columns
    df = df[["full_name", "leave", "year_y", "hometown", "outdated", "dup_year_name"]]
    df.columns = ["full_name", "leave", "year", "hometown", "outdated", "dup_year_name"]
    
    # write to csv
    df.to_csv((team[0] + "_roster.csv"), index = False)
