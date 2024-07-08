import os
import requests
import warnings
import pandas as pd
import json
from pprint import pprint
from tqdm import tqdm

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


def parse_kml_jsons(state, pid, cid):

    json_path = f"D:/assorted/Dropbox/Environment_Clearance/{state}/pdfs/{pid}_parivesh.json"
    if not os.path.exists(json_path):
        return ""

    with open(json_path, "r") as file:
        json_data = json.load(file)
        kml_data = json_data["proponentApplications"]["projectDetailDto"]["commonFormDetails"][0]["cafKML"][0]["caf_kml"]

    # Construct and return the row of data
    link_string = f"{base_url}/dms/okm/downloadDocument?&docTypemappingId={str(kml_data['document_mapping_id'])}&refId={str(int(cid))}&refType={kml_data['type']}&uuid={kml_data['uuid']}&version={str(kml_data['version'])}"
    row = {"pid": pid, "uuid": kml_data["uuid"], "mappingid": kml_data["document_mapping_id"], "document_name": kml_data["document_name"], "type": kml_data["type"], "version": kml_data["version"], "link": link_string}
    return row


# Download all the pdfs for a particular project
def download_project_kml(project, directory, column_name):

    kml_path = f"{directory}{project['pid']}.kml"
    link = project[column_name]

    # Quit if the link doesn't exist or the kml is already downloaded
    if type(link) != str or str(link) == "NaN" or str(link) == "" or os.path.isfile(kml_path):
        return

    # Download and store the pdf
    try:
        response = requests.get(link, verify=False) if project[column_name].startswith("http://") else requests.get(link)
        if response.status_code == 200:
            with open(kml_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download KML from: {link}")
    except Exception as e:
        print(f"Failed to download KML from: {link}, error: {e}")


def download_all_kmls(df, state):

    # Find or create the folder to store the pdfs to
    output_directory = f"D:/assorted/Dropbox/Environment_Clearance/{state}/kmls/"
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # Download it for each project
    print(f"Downloading KMLs...")
    df.progress_apply(download_project_kml, axis=1, args=(output_directory, "link"))


def construct_kml_df(state):
    # Create the path to store the Form 2 data to
    output_path = f"D:/assorted/Dropbox/Environment_Clearance/{state}/{state}_ec_kml_data.csv"
    if os.path.isfile(output_path):
        return pd.read_csv(output_path)

    df = pd.read_csv(f"D:/assorted/Dropbox/Environment_Clearance/{state}/{state}_ec_compiled_data.csv")
    kml_df = df.progress_apply(lambda row: parse_kml_jsons(state, row["pid"], row["caf_id"]), axis=1)
    kml_df = pd.json_normalize(kml_df)
    kml_df[["pid", "proposal_num"]] = df[["pid", "proposal_num"]]

    print(kml_df)
    kml_df.to_csv(output_path, index=False)
    return kml_df


if __name__ == "__main__":

    state_name = "Punjab"

    # Placing the below code inside this loop should allow every state to be scraped in one run
    # for state_name in state_codes.keys():

    kml_df = construct_kml_df(state_name)
    download_all_kmls(kml_df, state_name)
