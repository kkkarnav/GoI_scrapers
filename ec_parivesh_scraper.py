import os
import requests
import warnings
import pandas as pd
from pprint import pprint
from tqdm import tqdm
import random
import json

tqdm.pandas()
warnings.filterwarnings("ignore")

base_url = "https://parivesh.nic.in"
state_codes = {"Andhra_Pradesh": "02", "Arunachal_Pradesh": "03", "Assam": "04", "Bihar": "05", "Chhattisgarh": "33",
               "Goa": "10", "Gujarat": "11", "Haryana": "12", "Himachal_Pradesh": "13", "Jammu_And_Kashmir": "14",
               "Jharkhand": "34", "Karnataka": "15", "Kerala": "16", "Ladakh": "37",
               "Madhya_Pradesh": "17", "Maharashtra": "18", "Manipur": "20", "Meghalaya": "21", "Mizoram": "22",
               "Nagaland": "23", "Orissa": "24", "Puducherry": "25", "Punjab": "26", "Rajasthan": "27", "Sikkim": "28",
               "Tamil_Nadu": "29", "Telangana": "36", "Tripura": "30", "Uttar_Pradesh": "31", "Uttarakhand": "35",
               "West_Bengal": "32"}
possible_headers = [
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 "
                      "(KHTML, like Gecko) Version/13.1.1 Safari/605.1.15"
    },
    {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"
    },
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    },
    {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0"
    },
    {
        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    },
]


# Send a request to Parivesh as the frontend asking for this proposal number's data
def grab_caf_data(session, proposal_num):

    base_url = "https://parivesh.nic.in/parivesh_api/proponentApplicant/getCafDataByProposalNo?proposal_no="
    url = base_url + proposal_num

    # HTTP headers to make the server accept the request
    headers = {
        "User-Agent": possible_headers[random.randrange(0, 5)]["User-agent"],
        "Accept": "application/json,text/plain",
        "Accept-Language": "en-GB,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "Origin": "https://parivesh.nic.in",
        "DNT": "1",
        "Connection": "keep-alive",
        "Referer": "https://parivesh.nic.in/newupgrade/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-GPC": "1",
    }
    post_data = "{}"

    # Note that it's normal to see a lot of these failure messages pop up on the console,
    # this happens because many of the projects aren't on Parivesh at all
    try:
        # Return the html if successful
        response = session.post(url, data=post_data, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            # Return an error code if not
            print(f"Failed to download CAF data from: {url}, status code: {response.status_code}", )
            return response.status_code
    except Exception as e:
        print(f"Failed to download CAF data from: {url}, error: {e}")
        return 0


# Convert a project's Parivesh json into an entry in the csv
def parse_caf_json(caf_json):

    # Return if the project isn't on Parivesh (it'll have an html Form-2 instead)
    if type(caf_json) == int:
        return {"parivesh_id": caf_json}

    prow = {}
    caf_data = json.loads(caf_json)["data"]

    # Some projects don't have product details included
    try:
        project_details = caf_data["proponentApplications"]["projectDetailDto"]["commonFormDetails"][0]
        product_details = caf_data["clearence"]["ecProdTransportDetails"][0]
    except:
        pass

    # Construct the row of data
    try:
        prow["parivesh_id"] = caf_data["proponentApplications"]["id"]
        prow["proposal_num"] = caf_data["clearence"]["proposal_no"]
        prow["sw_num"] = project_details["project_sw_no"]
        prow["caf_id"] = caf_data["proponentApplications"]["caf_id"]
        prow["ec_id"] = caf_data["proponentApplications"]["proposal_id"]
        prow["status"] = caf_data["proponentApplications"]["last_status"]
        prow["project_name"] = project_details["project_name"]
        prow["project_description"] = project_details["project_description"]
        prow["date_clearance_creation"] = caf_data["clearence"]["created_on"]
        prow["date_clearance_update"] = caf_data["clearence"]["updated_on"]
        prow["date_submission"] = caf_data["proponentApplications"]["last_submission_date"]
        prow["date_undertaking"] = caf_data["clearence"]["ecOthersDetail"]["undertaking_date"]
        prow["date_last_submission"] = caf_data["clearence"]["ecOthersDetail"]["submission_date"]
        prow["applicant_state"] = caf_data["proponentApplications"]["state"]
        prow["applicant_district_code"] = project_details["applicant_district"]
        prow["applicant_pincode"] = project_details["applicant_pincode"]
        prow["applicant_street"] = project_details["applicant_street"]
        prow["applicant"] = project_details["applicant_name"]
        prow["applicant_email"] = project_details["applicant_email"]
        prow["organization"] = project_details["organization_name"]
        prow["organization_status"] = project_details["organization_legal_status"]
        prow["product_id"] = product_details["product_id"]
        prow["product"] = product_details["product_name"]
        prow["quantity"] = product_details["quantity"]
        prow["quantity_unit"] = product_details["unit"]
        prow["transport"] = product_details["transport_mode"]
        # prow["kmls"] = {"kml": project_details["cafKML"], "location": project_details["cafLocationOfKml"]}
    except:
        pass

    # Dump a sample project json to file
    # with open('./sample.json', 'w') as json_file:
    #     json.dump(caf_data, json_file, indent=4)

    return prow


# Create a csv with the Parivesh data for every project
def scrape_parivesh_data(session, state):

    # Create the path to store the Parivesh data to
    output_path = f"../{state}/{state}_ec_parivesh_data.csv"
    df = pd.read_csv(f"../{state}/{state}_ec_pdf_links.csv")

    # Scrape Parivesh for each proposal number and add it to the df
    parivesh_df = df.progress_apply(lambda row: parse_caf_json(grab_caf_data(session, row["Proposal.No."])), axis=1)
    parivesh_df = pd.json_normalize(parivesh_df)

    # Insert PIDS and fill out other columns
    parivesh_df["pid"] = df["pid"].reset_index(drop=True)
    parivesh_df.loc[parivesh_df["parivesh_id"] == 500, "parivesh_id"] = ""
    parivesh_df["is_parivesh"] = parivesh_df["proposal_num"].apply(lambda row: 1 if row == row else 0)

    print(parivesh_df)
    parivesh_df.to_csv(output_path, index=False)


if __name__ == "__main__":

    state_name = "Kerala"

    # Placing the below code inside this loop should allow every state to be scraped in one run
    # for state_name in state_codes.keys():

    with requests.Session() as session:
        scrape_parivesh_data(session, state_name)
