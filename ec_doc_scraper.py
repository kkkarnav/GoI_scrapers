import os
import requests
import warnings
import pandas as pd
from bs4 import BeautifulSoup
from pprint import pprint
from tqdm import tqdm

tqdm.pandas()
warnings.filterwarnings("ignore")

base_url = "https://environmentclearance.nic.in"
state_codes = {"Andhra_Pradesh": "02", "Arunachal_Pradesh": "03", "Assam": "04", "Bihar": "05", "Chhattisgarh": "33",
               "Goa": "10", "Gujarat": "11", "Haryana": "12", "Himachal_Pradesh": "13", "Jammu_And_Kashmir": "14",
               "Jharkhand": "34", "Karnataka": "15", "Kerala": "16", "Ladakh": "37",
               "Madhya_Pradesh": "17", "Maharashtra": "18", "Manipur": "20", "Meghalaya": "21", "Mizoram": "22",
               "Nagaland": "23", "Orissa": "24", "Puducherry": "25", "Punjab": "26", "Rajasthan": "27", "Sikkim": "28",
               "Tamil_Nadu": "29", "Telangana": "36", "Tripura": "30", "Uttar_Pradesh": "31", "Uttarakhand": "35",
               "West_Bengal": "32"}


# Grabs the pdf links from a particular project's main page
def grab_project_pdf_links(main_link):

    file_links = {}

    # Grab the main data page for this project
    try:
        response = requests.get(main_link)
        if response.status_code != 200:
            print(f"Failed to load page: {main_link}")
            return ""
    except Exception as e:
        print(f"Failed to load page: {main_link}, error: {e}")
        return ""

    # Extract the document links
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the main table
    target_table = None
    for table in soup.find_all('table'):
        if "Attached Files" in str(table):
            target_table = table
            break

    # Grab and store each document name and link
    cells = target_table.find_all('td')
    for cell in cells[-2].find("span").find_all("span", recursive=False):
        file_type = cell.find("span").find("a")["title"] if cell.find("span") else cell.find("a")["title"]
        file_link = cell.find("span").find("a")["href"] if cell.find("span") else cell.find("a")["href"]
        file_links[file_type] = file_link

    return file_links


# Create a csv with all the pdf links for each project
def generate_pdf_links(state):

    # Exit if pdf_links has already been generated
    output_path = f"../{state}/{state}_ec_pdf_links.csv"
    if os.path.isfile(output_path):
        return pd.read_csv(output_path)

    # Load maindata.csv
    main_df = pd.read_csv(f"../{state}/{state}_ec_maindata.csv")
    main_df.rename({"Unnamed: 0": "index"}, axis=1, inplace=True)

    # Add a column with each project's pid
    main_df["pid"] = main_df["Link"].apply(lambda x: x.split("=")[-1])

    # Append separate columns with download links for each file type
    print("Grabbing document download links for each project...")
    links_df = main_df.loc[:, "Link"].progress_apply(lambda row: grab_project_pdf_links(row)).apply(pd.Series)

    df = pd.concat([main_df, links_df], axis=1)
    df.to_csv(output_path, index=False)
    return df


# Download all the pdfs for a particular project
def download_project_pdfs(project, directory, column_name):

    pdf_path = f"{directory}{project['pid']}_{column_name}"
    pdf_path = pdf_path + ".pdf" if column_name != "Form2" else pdf_path + ".html"

    # Quit if the link doesn't exist or the pdf is already downloaded
    if type(project[column_name]) != str or str(project[column_name]) == "NaN" or str(project[column_name]) == "" or os.path.isfile(pdf_path):
        return

    # Construct the link to download the pdf from
    if project[column_name].startswith("http://") or project[column_name].startswith("https://"):
        link = project[column_name]
    elif project[column_name].startswith("../"):
        link = base_url + project[column_name][2:]
    elif project[column_name].startswith("state/") or project[column_name].startswith("timeline.aspx"):
        link = base_url + "/" + project[column_name]
    else:
        link = base_url + project[column_name]

    # Download and store the pdf
    try:
        response = requests.get(link, verify=False) if project[column_name].startswith("http://") else requests.get(link)
        if response.status_code == 200:
            with open(pdf_path, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Failed to download PDF from: {link}")
    except Exception as e:
        print(f"Failed to download PDF from: {link}, error: {e}")


def download_all_pdfs(df, state):

    # Find or create the folder to store the pdfs to
    output_directory = f"../{state}/pdfs/"
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)

    # For each type of file to download
    for column_index in range(15, len(df.columns)):
        # Download it for each project
        print(f"Downloading {df.columns[column_index] + 's'}...")
        df.progress_apply(download_project_pdfs, axis=1, args=(output_directory, df.columns[column_index],))


if __name__ == "__main__":

    state_name = "Kerala"

    # Placing the below code inside this loop should allow every state to be scraped in one run
    # for state_name in state_codes.keys():

    df_with_links = generate_pdf_links(state_name)
    download_all_pdfs(df_with_links, state_name)
