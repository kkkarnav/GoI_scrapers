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


# Grab a particular candidate's page and return the tables from it as dataframes
def scrape_table_data(state, year, candidate_id, search_string):

    try:
        candidate_url = f"{base_url}/{state}{year}/candidate.php?candidate_id={candidate_id}"
        driver.get(candidate_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        found = None
        for table in soup.find_all('table'):
            if search_string in str(table):
                found = table
                break

        found_table = pd.read_html(str(found), flavor="bs4")[0]
        found_table["statecode"] = state
        found_table["yearcode"] = year
        found_table["id"] = candidate_id

        return found_table

    except Exception as e:
        print(f"Error {e} while scraping {candidate_url}")
        return pd.DataFrame()


def scrape_criminal_cases(state, year, candidate_id):

    try:
        candidate_url = f"{base_url}/{state}{year}/candidate.php?candidate_id={candidate_id}"
        driver.get(candidate_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        found = None
        for ulist in soup.find_all('ul'):
            if 'class="w3-badge w3-red w3-tiny"' in str(ulist):
                found = ulist
                break

        items = [li.get_text(strip=True).replace("charges", " charges") for li in found.find_all("li")]
        df = pd.DataFrame(items, columns=["charges"])
        df[["count", "charge"]] = df["charges"].str.split(" charges related to ", n=1, expand=True)

        df.drop("charges", axis=1, inplace=True)
        df["statecode"] = state
        df["yearcode"] = year
        df["id"] = candidate_id

        return df

    except Exception as e:
        print(f"Error {e} while scraping {candidate_url}")
        return pd.DataFrame()


if __name__ == "__main__":

    # Selenium initialization
    load_dotenv()
    options = Options()
    options.headless = True
    options.binary_location = (os.getenv("BINARY_LOCATION"))

    driver = webdriver.Firefox(options=options, service=Service('D:/code/scripts/geckodriver.exe'))

    # main_df = scrape_elections()
    # print(elections_df)
    main_df = pd.read_csv(f"{PATH}/myneta_main_data.csv")

    '''itr_data = main_df.progress_apply(lambda x: scrape_table_data(x["statecode"], x["yearcode"], x["id"], 'id="income_tax"'), axis=1)
    itr_data = pd.concat(list(itr_data), ignore_index=True)
    itr_data.to_csv(f"{PATH}/myneta_itr_data.csv", index=False)

    asset1_data = main_df.progress_apply(lambda x: scrape_table_data(x["statecode"], x["yearcode"], x["id"], 'id="movable_assets"'), axis=1)
    asset1_data = pd.concat(list(asset1_data), ignore_index=True)
    asset1_data.to_csv(f"{PATH}/myneta_asset1_data.csv", index=False)

    asset2_data = main_df.progress_apply(lambda x: scrape_table_data(x["statecode"], x["yearcode"], x["id"], 'id="immovable_assets"'), axis=1)
    asset2_data = pd.concat(list(asset2_data), ignore_index=True)
    asset2_data.to_csv(f"{PATH}/myneta_asset2_data.csv", index=False)

    liability_data = main_df.progress_apply(lambda x: scrape_table_data(x["statecode"], x["yearcode"], x["id"], 'id="liabilities"'), axis=1)
    liability_data = pd.concat(list(liability_data), ignore_index=True)
    liability_data.to_csv(f"{PATH}/myneta_liability_data.csv", index=False)'''

    cases_data = main_df.progress_apply(lambda x: scrape_criminal_cases(x["statecode"], x["yearcode"], x["id"]), axis=1)
    cases_data = pd.concat(list(cases_data), ignore_index=True)
    cases_data.to_csv(f"{PATH}/myneta_cases_data.csv", index=False)
    print(cases_data)

    driver.quit()
