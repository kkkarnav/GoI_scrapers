import os
from dotenv import load_dotenv
from io import StringIO

from pprint import pprint
from tqdm import tqdm
import warnings

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

tqdm.pandas()
warnings.filterwarnings("ignore")

base_url = "https://myneta.info"
PATH = "D:/assorted/Dropbox/Environment_Clearance/Election_data/"


def scrape_election_page(state, year):

    election_url = f"https://myneta.info/{state}{year}/index.php?action=show_winners&sort=default"
    driver.get(election_url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    winners_table = None
    for table in soup.find_all('table'):
        if '<a href="/candidate.php?' in str(table):
            winners_table = table
            break

    if not winners_table:
        print(f"Couldn't find the winners' table for {election_url}")

    candidate_ids = []
    for tr in winners_table.find_all("tr"):
        for link in tr.find_all("a"):
            if link.get("href")[:10] != "/candidate":
                candidate_ids.append(link.get("href").split("=")[1])
                break

    winners_table = pd.read_html(StringIO(str(soup)))[2]
    winners_table["id"] = candidate_ids

    return winners_table


def scrape_elections():

    parameters = get_parameters()
    winners_tables = []

    for i in tqdm(range(len(parameters))):

        state = parameters.loc[i, "state"]
        year = parameters.loc[i, "year"]

        # Unscheduled elections will have their winners in the
        # by election table for the previous election (can be specifically scraped)
        # List: MP 2018, MH 2022, TN 2009
        if state == "andhrapradesh" and year == 2014:
            state = "andhra"
        elif state == "andhrapradesh" and year == 2009:
            state, year = "ap", "09"
        elif state == "bihar" and year == 2010:
            state = "bih"
        elif state == "chhattisgarh" and year == 2008:
            state, year = 2008, "chhattisgarh"
        elif state == "haryana" and year == 2009:
            state = "ha"
        elif state == "himachalpradesh" and year == 2012:
            state = "hp"
        elif state == "jharkhand" and year == 2009:
            state, year = "jarka", "09"
        elif state == "madhyapradesh" and year == 2013:
            state = "mp"
        elif state == "madhyapradesh" and year == 2008:
            state, year = "2008", "mp"
        elif state == "maharashtra" and year == 2009:
            state = "mh"
        elif state == "odisha" and year == 2009:
            state = "orissa"
        elif state == "punjab" and year == 2012:
            state = "pb"
        elif state == "rajasthan" and year == 2008:
            state = "rj"
        elif state == "uttarpradesh" and year == 2012:
            state = "up"
        elif state == "uttarakhand" and year == 2012:
            state = "utt"
        elif state == "madhyapradesh" and year == 2020:
            continue
        elif state == "maharashtra" and year == 2022:
            continue
        elif state == "telangana" and year == 2009:
            continue

        winners = scrape_election_page(state, year)
        winners["state"], winners["year"] = parameters.loc[i, "state"], parameters.loc[i, "year"]
        winners["statecode"], winners["yearcode"] = state, str(year)
        winners_tables.append(winners)

    main_data = pd.concat(winners_tables, ignore_index=True)
    return main_data


def get_parameters():

    ruling_parties_path = f"{PATH}/state_ruling_party_timings_final.csv"
    ruling_parties = pd.read_csv(ruling_parties_path)

    states = ruling_parties["State"].apply(lambda x: str(x).lower().replace("_", ""))
    years = ruling_parties["Year"].apply(lambda x: int(x))
    parameters = pd.DataFrame({'state': states, 'year': years})

    return parameters


if __name__ == "__main__":

    # Selenium initialization
    load_dotenv()
    options = Options()
    options.headless = True
    options.binary_location = (os.getenv("BINARY_LOCATION"))

    driver = webdriver.Firefox(options=options, service=Service('D:/code/scripts/geckodriver.exe'))

    elections_df = scrape_elections()
    elections_df.to_csv(f"{PATH}/myneta_main_data.csv", index=False)
    print(elections_df)

    driver.quit()
