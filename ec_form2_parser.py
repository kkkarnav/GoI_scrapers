import os
import requests
import warnings
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint
from tqdm import tqdm
import random
import json

tqdm.pandas()
warnings.filterwarnings("ignore")


def parse_form1_html(soup, pid):
    # Construct the row of data
    prow = {"pid": pid, "parivesh_id": None, "caf_id": None, "ec_id": None, "status": None}

    try:
        first_table = soup.find_all('table')[6]

        prow["project_name"] = first_table.find_all('tr')[0].find_all('td')[1].get_text(strip=True)
        prow["project_description"] = None
        prow["organization"] = first_table.find_all('tr')[0].find_all('td')[3].get_text(strip=True)
        prow["organization_status"] = first_table.find_all('tr')[1].find_all('td')[3].get_text(strip=True)
    except:
        pass

    try:
        second_table = soup.find_all('table')[8]

        prow["applicant"] = second_table.find_all('tr')[1].find_all('td')[1].get_text(strip=True)
        prow["applicant_email"] = second_table.find_all('tr')[5].find_all('td')[1].get_text(strip=True)
        prow["applicant_pincode"] = second_table.find_all('tr')[4].find_all('td')[1].get_text(strip=True)
        prow["applicant_street"] = second_table.find_all('tr')[3].find_all('td')[1].get_text(strip=True)
    except:
        pass

    try:
        prow["applicant_state"] = soup.find_all('table')[13].find_all('tr')[2].find_all('td')[1].get_text(strip=True)
        prow["applicant_district"] = soup.find_all('table')[13].find_all('tr')[2].find_all('td')[2].get_text(strip=True)
        prow["applicant_tehsil"] = soup.find_all('table')[13].find_all('tr')[2].find_all('td')[3].get_text(strip=True)
        prow["applicant_village"] = soup.find_all('table')[13].find_all('tr')[2].find_all('td')[4].get_text(strip=True)
    except:
        pass

    try:
        third_table = soup.find_all('table')[9]

        prow["proposal_num"] = third_table.find_all('tr')[5].find_all('td')[1].get_text(strip=True)
        prow["sw_num"] = third_table.find_all('tr')[6].find_all('td')[1].get_text(strip=True)
        prow["major_activity"] = third_table.find_all('tr')[2].find_all('td')[1].get_text(strip=True)
        prow["minor_activity"] = third_table.find_all('tr')[3].find_all('td')[1].get_text(strip=True)
        prow["category"] = third_table.find_all('tr')[4].find_all('td')[1].get_text(strip=True)

        prow["date_clearance_creation"] = None
        prow["date_clearance_update"] = None
        prow["date_submission"] = None
        prow["date_undertaking"] = None
        prow["date_last_submission"] = None
    except:
        pass

    return prow


def parse_jv_html(soup, pid):
    # Construct the row of data
    prow = {"pid": pid, "parivesh_id": None, "caf_id": None, "ec_id": None, "status": None}

    try:
        first_table = soup.find_all('table')[5]

        prow["project_name"] = first_table.find_all('tr')[3].find_all('td')[1].get_text(strip=True)
        prow["project_description"] = None
        prow["organization"] = first_table.find_all('tr')[4].find_all('td')[1].get_text(strip=True)
        prow["organization_status"] = first_table.find_all('tr')[6].find_all('td')[1].get_text(strip=True)
    except:
        pass

    try:
        second_table = soup.find_all('table')[9]

        prow["applicant"] = second_table.find_all('tr')[2].find_all('td')[1].get_text(strip=True)
        prow["applicant_email"] = second_table.find_all('tr')[6].find_all('td')[1].get_text(strip=True)
        prow["applicant_pincode"] = second_table.find_all('tr')[5].find_all('td')[1].get_text(strip=True)
        prow["applicant_street"] = second_table.find_all('tr')[4].find_all('td')[1].get_text(strip=True)
    except:
        pass

    try:
        prow["applicant_state"] = soup.find_all('table')[16].find_all('tr')[2].find_all('td')[1].get_text(strip=True)
        prow["applicant_district"] = soup.find_all('table')[16].find_all('tr')[2].find_all('td')[2].get_text(strip=True)
        prow["applicant_tehsil"] = soup.find_all('table')[16].find_all('tr')[2].find_all('td')[3].get_text(strip=True)
        prow["applicant_village"] = soup.find_all('table')[16].find_all('tr')[2].find_all('td')[4].get_text(strip=True)
    except:
        pass

    try:
        third_table = soup.find_all('table')[11]

        prow["proposal_num"] = third_table.find_all('tr')[5].find_all('td')[1].get_text(strip=True)
        prow["sw_num"] = third_table.find_all('tr')[6].find_all('td')[1].get_text(strip=True)
        prow["major_activity"] = third_table.find_all('tr')[2].find_all('td')[1].get_text(strip=True)
        prow["minor_activity"] = third_table.find_all('tr')[3].find_all('td')[1].get_text(strip=True)
        prow["category"] = third_table.find_all('tr')[4].find_all('td')[1].get_text(strip=True)

        prow["date_clearance_creation"] = None
        prow["date_clearance_update"] = None
        prow["date_submission"] = None
        prow["date_undertaking"] = None
        prow["date_last_submission"] = None
    except:
        pass

    try:
        lat_long = soup.find_all('table')[13]

        if lat_long.find_all('tr')[7].find_all('td')[1].get_text(strip=True):
            prow["lat_south"] = lat_long.find_all('tr')[6].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[7].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[8].find_all('td')[1].get_text(strip=True)
            prow["lat_north"] = lat_long.find_all('tr')[10].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[11].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[12].find_all('td')[1].get_text(strip=True)
            prow["long_west"] = lat_long.find_all('tr')[15].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[16].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[17].find_all('td')[1].get_text(strip=True)
            prow["long_east"] = lat_long.find_all('tr')[19].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[20].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[21].find_all('td')[1].get_text(strip=True)
        else:
            prow["lat_south"] = lat_long.find_all('tr')[6].find_all('td')[1].get_text(strip=True)
            prow["lat_north"] = lat_long.find_all('tr')[10].find_all('td')[1].get_text(strip=True)
            prow["long_west"] = lat_long.find_all('tr')[15].find_all('td')[1].get_text(strip=True)
            prow["long_east"] = lat_long.find_all('tr')[19].find_all('td')[1].get_text(strip=True)
    except:
        pass

    try:
        product_table = soup.find_all('table')[27]

        prow["product_id"] = None
        prow["product"] = product_table.find_all('tr')[2].find_all('td')[1].get_text(strip=True)
        prow["quantity"] = product_table.find_all('tr')[2].find_all('td')[2].get_text(strip=True)
        prow["quantity_unit"] = product_table.find_all('tr')[2].find_all('td')[3].get_text(strip=True)
        prow["transport"] = product_table.find_all('tr')[2].find_all('td')[5].get_text(strip=True)
    except:
        pass

    return prow


def parse_form2_html(state, pid):
    try:
        file_name = f"../{state}/pdfs/{pid}_Form2.html"
        with open(file_name, "r", encoding="utf8") as html_file:
            html = html_file.read()
        soup = BeautifulSoup(html, 'html.parser')

        if "<u>Form-1</u>" in str(soup):
            return parse_form1_html(soup, pid)
        elif "Name of the JV Partner" in str(soup):
            return parse_jv_html(soup, pid)
    except:
        pass

    # Construct the row of data
    prow = {"pid": pid, "parivesh_id": None, "caf_id": None, "ec_id": None, "status": None}

    try:
        first_table = soup.find_all('table')[5]

        prow["project_name"] = first_table.find_all('tr')[3].find_all('td')[1].get_text(strip=True)
        prow["project_description"] = None
        prow["organization"] = first_table.find_all('tr')[4].find_all('td')[1].get_text(strip=True)
        prow["organization_status"] = first_table.find_all('tr')[6].find_all('td')[1].get_text(strip=True)
    except:
        pass

    try:
        second_table = soup.find_all('table')[7]

        prow["applicant"] = second_table.find_all('tr')[2].find_all('td')[1].get_text(strip=True)
        prow["applicant_email"] = second_table.find_all('tr')[6].find_all('td')[1].get_text(strip=True)
        prow["applicant_pincode"] = second_table.find_all('tr')[5].find_all('td')[1].get_text(strip=True)
        prow["applicant_street"] = second_table.find_all('tr')[4].find_all('td')[1].get_text(strip=True)
    except:
        pass

    try:
        prow["applicant_state"] = soup.find_all('table')[16].find_all('tr')[2].find_all('td')[1].get_text(strip=True)
        prow["applicant_district"] = soup.find_all('table')[16].find_all('tr')[2].find_all('td')[2].get_text(strip=True)
        prow["applicant_tehsil"] = soup.find_all('table')[16].find_all('tr')[2].find_all('td')[3].get_text(strip=True)
        prow["applicant_village"] = soup.find_all('table')[16].find_all('tr')[2].find_all('td')[4].get_text(strip=True)
    except:
        pass

    try:
        third_table = soup.find_all('table')[9]

        prow["proposal_num"] = third_table.find_all('tr')[5].find_all('td')[1].get_text(strip=True)
        prow["sw_num"] = third_table.find_all('tr')[6].find_all('td')[1].get_text(strip=True)
        prow["major_activity"] = third_table.find_all('tr')[2].find_all('td')[1].get_text(strip=True)
        prow["minor_activity"] = third_table.find_all('tr')[3].find_all('td')[1].get_text(strip=True)
        prow["category"] = third_table.find_all('tr')[4].find_all('td')[1].get_text(strip=True)

        prow["date_clearance_creation"] = None
        prow["date_clearance_update"] = None
        prow["date_submission"] = None
        prow["date_undertaking"] = None
        prow["date_last_submission"] = None
    except:
        pass

    try:
        lat_long = soup.find_all('table')[11]

        if lat_long.find_all('tr')[7].find_all('td')[1].get_text(strip=True):
            prow["lat_south"] = lat_long.find_all('tr')[6].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[7].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[8].find_all('td')[1].get_text(strip=True)
            prow["lat_north"] = lat_long.find_all('tr')[10].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[11].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[12].find_all('td')[1].get_text(strip=True)
            prow["long_west"] = lat_long.find_all('tr')[15].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[16].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[17].find_all('td')[1].get_text(strip=True)
            prow["long_east"] = lat_long.find_all('tr')[19].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[20].find_all('td')[1].get_text(strip=True) + "," + \
                                lat_long.find_all('tr')[21].find_all('td')[1].get_text(strip=True)
        else:
            prow["lat_south"] = lat_long.find_all('tr')[6].find_all('td')[1].get_text(strip=True)
            prow["lat_north"] = lat_long.find_all('tr')[10].find_all('td')[1].get_text(strip=True)
            prow["long_west"] = lat_long.find_all('tr')[15].find_all('td')[1].get_text(strip=True)
            prow["long_east"] = lat_long.find_all('tr')[19].find_all('td')[1].get_text(strip=True)

    except:
        pass

    try:
        product_table = soup.find_all('table')[25]

        prow["product_id"] = None
        prow["product"] = product_table.find_all('tr')[2].find_all('td')[1].get_text(strip=True)
        prow["quantity"] = product_table.find_all('tr')[2].find_all('td')[2].get_text(strip=True)
        prow["quantity_unit"] = product_table.find_all('tr')[2].find_all('td')[3].get_text(strip=True)
        prow["transport"] = product_table.find_all('tr')[2].find_all('td')[5].get_text(strip=True)
    except:
        pass

    return prow


def construct_form2_df(state):
    # Create the path to store the Parivesh data to
    output_path = f"../{state}/{state}_ec_form2_data.csv"
    if os.path.isfile(output_path):
        return pd.read_csv(output_path)

    df = pd.read_csv(f"../{state}/{state}_ec_pdf_links.csv")
    form2_df = df.progress_apply(lambda row: parse_form2_html(state, row["pid"]), axis=1)
    form2_df = pd.json_normalize(form2_df)

    print(form2_df)
    form2_df.to_csv(output_path, index=False)


def merge_sources(state, output_path):
    p_df = pd.read_csv(f"../{state}/{state}_ec_parivesh_data.csv")
    f_df = pd.read_csv(f"../{state}/{state}_ec_form2_data.csv")

    compiled_df = p_df.apply(lambda row: row if row["is_parivesh"] == 1 else f_df.loc[row.name], axis=1)
    compiled_df.loc[compiled_df["is_parivesh"] != 1, "is_parivesh"] = 0

    print(compiled_df)
    compiled_df.to_csv(output_path, index=False)


if __name__ == "__main__":
    state_name = "Andhra_Pradesh"
    path = f"../{state_name}/{state_name}_ec_compiled_data.csv"

    # Placing the below code inside this loop should allow every state to be scraped in one run
    # for state_name in state_codes.keys():

    construct_form2_df(state_name)
    merge_sources(state_name, path)
