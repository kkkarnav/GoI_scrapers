import requests
from pprint import pprint
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import os

tqdm.pandas()

base_url = "https://egramswaraj.gov.in/voucherWiseReport.do?"


def grab_month_data(finyear, month, village_row):

    voucherwise = "Y"
    schemewise = "P"
    schemecode = "-1"

    with requests.Session() as session:

        url = f"{base_url}" \
              f"voucherWise={voucherwise}" \
              f"&finYear={finyear}" \
              f"&month={str(month) if month >= 10 else '0' + str(month)}" \
              f"&schemewise={schemewise}" \
              f"&state={village_row.loc['state_code']}" \
              f"&district={village_row.loc['district_code']}" \
              f"&block={village_row.loc['block_code']}" \
              f"&village={village_row.loc['gp_code']}" \
              f"&schemeCode={schemecode}"

        response = session.get(url)
        if response.status_code != 200:
            # Return an error code if not successful
            print(f"Failed to download CAF data from: {url}, status code: {response.status_code}", )
            return response.status_code
        soup = BeautifulSoup(response.content, 'html.parser')

        target_table = None
        for table in soup.find_all('table'):
            if "Journal" in str(table):
                target_table = table
                break

        return target_table


def grab_data(village_row, finyear):
    entries = []

    for month in range(1, 13):

            balance = (f"01/"
                       f"{str(month) if month >= 10 else '0'+str(month)}/"
                       f"{(finyear[2:4] if month >= 4 else finyear[-2:])}",
                       target_table.find_all('tr')[0].find_all('td')[1].get_text(strip=True))
            entries.append([balance[0], "Opening Balance", "Balance", balance[1]])

            for row in target_table.find_all('tr')[3:-1]:
                if f"{row.find_all('td')[0].get_text(strip=True)}" == "No Data Found!!":
                    break

                if f"{row.find_all('td')[0].get_text(strip=True)}" != "":
                    receipt = [row.find_all('td')[0].get_text(strip=True), "Receipt", row.find_all('td')[2].get_text(strip=True), row.find_all('td')[3].get_text(strip=True)]
                    entries.append(receipt)
                if f"{row.find_all('td')[4].get_text(strip=True)}" != "":
                    payment = [row.find_all('td')[4].get_text(strip=True), "Payment", row.find_all('td')[6].get_text(strip=True), row.find_all('td')[7].get_text(strip=True)]
                    entries.append(payment)

    # print(opening_balances)
    village_df = pd.DataFrame(entries, columns=["date", "entry", "type", "amount"])
    village_df["date"] = village_df["date"].apply(lambda x: pd.to_datetime(x, dayfirst=True))
    village_df = village_df.sort_values(by=["date"]).reset_index(drop=True)
    village_df["state"] = village_row["state_name"]
    village_df["district"] = village_row["district_name"]
    village_df["block"] = village_row["block_name"]
    village_df["gp"] = village_row["gp_name"]
    village_df["N_vil"] = village_row["N_vil"]

    return village_df


if __name__ == "__main__":
    state = "Odisha"
    start_year = 2015
    end_year = 2016

    code_df = pd.read_csv("./lgd_code_odisha_gp.csv", index_col=0).reset_index(drop=True)

    for year in range(start_year, end_year):

        dfs = []
        raw_df = code_df.progress_apply(grab_data, axis=1, args=(f"{year}-{year+1}",))
        for index, village in raw_df.items():
            dfs.append(village)
        df = pd.concat(dfs, ignore_index=True)

        print(df)
        df.to_csv(f"./{state}_{year}_voucher_data.csv")
