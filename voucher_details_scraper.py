import requests
import warnings
from pprint import pprint
import ast
from tqdm import tqdm
import pandas as pd
from bs4 import BeautifulSoup
import os

tqdm.pandas()
warnings.filterwarnings("ignore")

base_url = "https://egramswaraj.gov.in/"


def grab_voucher_data(voucher_link):
    with requests.Session() as session:

        url = f"{base_url}{voucher_link}"

        response = session.get(url)
        if response.status_code != 200:
            # Return an error code if not successful
            print(f"Failed to download Voucher data from: {url}, status code: {response.status_code}", )
            return response.status_code
        soup = BeautifulSoup(response.content, 'html.parser')

        target_table = None
        for table in soup.find_all('table'):
            if "Type Of Transaction" in str(table):
                target_table = table
                break

        return target_table


def parse_payment(target_table, voucher_row):
    entry = []
    details_df = pd.DataFrame()

    entry.append(target_table.find_all('tr')[2].find_all('td')[1].get_text(strip=True))
    entry.append("Payment")
    entry.append(target_table.find_all('tr')[2].find_all('td')[-1].get_text(strip=True))
    entry.append(target_table.find_all('tr')[1].find_all('td')[1].get_text(strip=True))
    entry.append(target_table.find_all('tr')[3].find_all('td')[-1].get_text(strip=True))
    entry.append(target_table.find_all('tr')[4].find_all('td')[1].get_text(strip=True))

    heads = ast.literal_eval("{\"" +
                             (target_table.find_all('tr')[3].find_all('td')[1].get_text())
                             .replace("\t\n", "").replace("\t", "").strip().replace("\n", ",")
                             .replace("-", ":").replace("Expenditure Heads,", "")
                             .replace(":in:", "-in-").replace(": in:", "-in-")
                             .replace("other Exp:", "other Exp - ").replace("Other :", "Other -")
                             .replace("other Expenditure:", "other Expenditure - ")
                             .replace("Other Expenditure :", "Other Expenditure - ")
                             .replace("Tube:wells", "Tubewells").replace("Non:tax", "Non-tax")
                             .replace(':', '":"').replace(',', '","') +
                             "\"}")

    bank_details = \
        {"Account Type": ""} if target_table.find_all('tr')[-1].find_all('td')[1].get_text(strip=True) == "" else \
            ast.literal_eval("{\"" + (target_table.find_all('tr')[-1].find_all('td')[1].get_text())
                             .replace("\t\n", "").replace("\t", "").strip().replace("\n", ",")
                             .replace("-", ":").replace(':', '":"').replace(',', '","') +
                             "\"}") if target_table.find_all('tr')[-1].find_all('td')[
                                           1].get_text() != '\nDeduction\n' else \
                ast.literal_eval("{\"" + (target_table.find_all('tr')[6].find_all('td')[1].get_text())
                                 .replace("\t\n", "").replace("\t", "").strip().replace("\n", ",")
                                 .replace("-", ":").replace(':', '":"').replace(',', '","') +
                                 "\"}")

    heads = str({key.strip(): value.strip() for key, value in heads.items()})
    bank_details = {key.strip(): value.strip() for key, value in bank_details.items()}

    bank_details_df = pd.json_normalize(bank_details)
    entry_df = pd.DataFrame([entry], columns=["date", "entry", "code", "scheme", "amount", "particulars"])
    entry_df["account_head"] = heads
    details_df = pd.concat([entry_df, bank_details_df], axis=1).reset_index(drop=True)
    details_df[
        ["state_code", "state_name", "district_code", "district_name", "block_code", "block_name", "gp_code", "gp_name",
         "N_vil"]] = voucher_row.loc[
        ["state_code", "state_name", "district_code", "district_name", "block_code", "block_name", "gp_code", "gp_name",
         "N_vil"]]

    return details_df


def parse_receipt(target_table, voucher_row):

    entry = []
    details_df = pd.DataFrame()

    entry.append(target_table.find_all('tr')[1].find_all('td')[0].get_text(strip=True).split(":")[1].strip())
    entry.append("Receipt")
    entry.append(target_table.find_all('tr')[1].find_all('td')[1].get_text(strip=True).split(":")[1].strip())
    entry.append(target_table.find_all('tr')[0].find_all('td')[1].get_text(strip=True).split(":")[1].strip())
    entry.append(target_table.find_all('tr')[3].find_all('td')[1].get_text(strip=True))
    entry.append(target_table.find_all('tr')[6].find_all('td')[0].get_text(strip=True).split(":")[1].strip())

    heads = ast.literal_eval("{" +
                             (target_table.find_all('tr')[3].find_all('td')[0].get_text())
                             .replace("\xa0", "").replace("\t", "").strip().replace("\r\n", ",")
                             .replace("-", ":").replace("Expenditure Heads ,", "")
                             .replace(":in:", "-in-").replace(": in:", "-in-")
                             .replace("other Exp:", "other Exp - ").replace("Other :", "Other -")
                             .replace("other Expenditure:", "other Expenditure - ")
                             .replace("Other Expenditure :", "Other Expenditure - ")
                             .replace("Tube:wells", "Tubewells").replace("Non:tax", "Non-tax")
                             .replace(':', '":"').replace(',', '","').split(":", 1)[1] +
                             "\"}")

    account_type = (
        target_table.find_all('tr')[4].find_all('td')[0].get_text(strip=True).split(":")[1].strip()).replace(
        "Panchayat(in Hand)", "Cash")
    account_no = target_table.find_all('tr')[4].find_all('td')[1].get_text(strip=True).split(":")[
        1].strip() if account_type == "Bank" else ""
    cheque_no = (target_table.find_all('tr')[5].find_all('td')[1].get_text(strip=True).split(":")[1].strip())
    cheque_date = target_table.find_all('tr')[5].find_all('td')[2].get_text(strip=True).split(":")[1].strip()

    heads = str({key.strip(): value.strip() for key, value in heads.items()})

    bank_details_df = pd.DataFrame([[account_type, account_no, cheque_no, cheque_date]],
                                   columns=["Account Type", "Account No.", "Cheque No", "Cheque Date"])
    entry_df = pd.DataFrame([entry], columns=["date", "entry", "code", "scheme", "amount", "particulars"])
    entry_df["account_head"] = heads
    details_df = pd.concat([entry_df, bank_details_df], axis=1).reset_index(drop=True)
    details_df[
        ["state_code", "state_name", "district_code", "district_name", "block_code", "block_name", "gp_code", "gp_name",
         "N_vil"]] = voucher_row.loc[
        ["state_code", "state_name", "district_code", "district_name", "block_code", "block_name", "gp_code", "gp_name",
         "N_vil"]]

    return details_df


def grab_details(voucher_row):
    entry = []
    details_df = pd.DataFrame()

    try:
        target_table = grab_voucher_data(voucher_row['link'])
    except:
        print(
            f"Error scraping voucher {voucher_row['code']} in {voucher_row['gp_name']}, in {voucher_row['district_name']}")
        return

    try:
        if "paymentVoucher" in voucher_row['link']:
            return parse_payment(target_table, voucher_row)
        if "receiptVoucher" in voucher_row['link']:
            return parse_receipt(target_table, voucher_row)
    except:
        print(
            f"Error scraping details for {voucher_row['code']} in {voucher_row['gp_name']}, in {voucher_row['district_name']}")
        return


if __name__ == "__main__":
    state = "Odisha"
    start_year = 2015
    end_year = 2016

    for year in range(start_year, end_year):

        link_df = pd.read_csv(f"./{state}_{year}_voucher_data.csv")
        link_df = link_df[link_df["entry"] != "Opening Balance"]

        dfs = []
        raw_df = link_df.progress_apply(grab_details, axis=1)
        for index, village in raw_df.items():
            dfs.append(village)
        df = pd.concat(dfs, ignore_index=True)
        df["date"] = df["date"].apply(lambda x: pd.to_datetime(x, dayfirst=True))
        df["Account Type"] = df["Account Type"].replace("", "Demand Draft")

        print(df)
        df.sort_values(by=["state_name", "district_name", "block_name", "gp_name", "date", "code"], inplace=True)
        df.to_csv(f"./{state}_{year}_voucher_details.csv", index=False)
