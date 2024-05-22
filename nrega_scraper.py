import requests
from pprint import pprint
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import os

base_url = "https://nreganarep.nic.in/netnrega/"
state_codes = {"ANDAMAN AND NICOBAR": "01", "ANDHRA PRADESH": "02",
               "ARUNACHAL PRADESH": "03", "ASSAM": "04", "BIHAR": "05", "CHHATTISGARH": "33", "DN HAVELI AND DD": "07",
               "GOA": "10", "GUJARAT": "11", "HARYANA": "12", "HIMACHAL PRADESH": "13", "JAMMU AND KASHMIR": "14",
               "JHARKHAND": "34", "KARNATAKA": "15", "KERALA": "16", "LADAKH": "37", "LAKSHADWEEP": "19",
               "MADHYA PRADESH": "17", "MAHARASHTRA": "18", "MANIPUR": "20", "MEGHALAYA": "21", "MIZORAM": "22",
               "NAGALAND": "23", "ODISHA": "24", "PUDUCHERRY": "25", "PUNJAB": "26", "RAJASTHAN": "27", "SIKKIM": "28",
               "TAMIL NADU": "29", "TELANGANA": "36", "TRIPURA": "30", "UTTAR PRADESH": "31", "UTTARAKHAND": "35",
               "WEST BENGAL": "32"}


def grab_districts(session, state, year):
    page = "dmd"
    resolution = "s"
    state_name = state.upper().replace(" ", "+")
    state_code = state_codes[state.upper()]
    url = f"https://nreganarep.nic.in/netnrega/demand_emp_demand.aspx?file1={page}&page1={resolution}&lflag=eng&state_name={state_name}&state_code={state_code}&fin={year}&fin_year={year}&source=national&Digest=p2+izqLOjHDJzROMBL2FVA"
    response = session.get(url)

    districts = []

    soup = BeautifulSoup(response.content, 'html.parser')
    target_table = None
    for table in soup.find_all('table'):
        if "Month wise Household" in str(table):
            target_table = table
            break

    for row in target_table.find_all('tr'):
        cells = row.find_all('td')
        second_column = cells[1].find('a')
        if second_column:
            link_text = second_column.get_text(strip=True)
            href_link = second_column['href']
            districts.append((link_text, href_link))

    return districts


def grab_blocks(session, district):
    url = base_url + district[1]
    response = session.get(url)

    blocks = []

    soup = BeautifulSoup(response.content, 'html.parser')
    target_table = None
    for table in soup.find_all('table'):
        if "Month wise Household" in str(table):
            target_table = table
            break

    for row in target_table.find_all('tr'):
        cells = row.find_all('td')
        second_column = cells[1].find('a')
        if second_column:
            link_text = second_column.get_text(strip=True)
            href_link = second_column['href']
            blocks.append((link_text, href_link))

    return blocks


def grab_panchayats(session, district, block):
    url = base_url + block[1]
    response = session.get(url)

    panchayats = []

    soup = BeautifulSoup(response.content, 'html.parser')
    target_table = None
    for table in soup.find_all('table'):
        if "Month wise Household" in str(table):
            target_table = table
            break

    for row in target_table.find_all('tr')[5:-1]:
        panchayat = [district[0], block[0]]
        cells = row.find_all('td')
        for i in range(1, 14):
            column_text = cells[i].get_text(strip=True)
            panchayat.append(column_text)
        panchayats.append(panchayat)

    return panchayats


def grab_data(state, year):
    data = []

    with requests.Session() as session:

        districts = grab_districts(session, state, year)

        for district in tqdm(districts):
            blocks = grab_blocks(session, district)

            for block in blocks:
                panchayats = grab_panchayats(session, district, block)
                data += panchayats

    return data


if __name__ == "__main__":
    state = "Odisha"
    start_year = 2012
    end_year = 2013

    for year in range(start_year, end_year):

        df = pd.DataFrame(grab_data(state, str(year)+"-"+str(year+1)))

        filename = f'../mnrega/{state.replace(" ", "_")}/mnrega_dmd_{str(year)+"-"+str(year+1)}.csv'

        # create the folder if none exists
        foldername = "/".join(filename.split("/")[:-1])
        if not os.path.exists(foldername):
            os.mkdir(foldername)

        df.to_csv(filename, index=True)
