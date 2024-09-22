import os
import requests
import re
import warnings
import pandas as pd
from pypdf import PdfReader
from pprint import pprint
from tqdm import tqdm
import pymupdf

tqdm.pandas()
warnings.filterwarnings("ignore")


def parse_one_pdf(file_name, read_pdf):

    budget = {}

    for index, page in enumerate(read_pdf.pages):

        text = page.extract_text().replace("\n", "")
        if "PARA: 4 FINANCIAL POSITION" in text:

            if "GRANDTOTAL" in text or "GRAND TOTAL" in text:
                text = text.replace("GRAND TOTAL", "GRANDTOTAL").replace("Details of Closing Balance and Comments", "Comments")
            else:
                text = read_pdf.pages[index + 1].extract_text().replace("\n", "").replace("GRAND TOTAL", "GRANDTOTAL").replace("Details of Closing Balance and Comments", "Comments")
                index += 1

            try:
                budget_string = text.split("GRANDTOTAL ")[1].split("Comments")[0]

                keys = ["Opening_Balance", "Receipt", "Expenditure", "Closing_Balance", "Check"]
                values = [float(x) for i, x in enumerate(re.findall(r'\d*\.\d{2}', budget_string)) if i in [0, 1, 3, 4, 5]]

                budget = dict(zip(keys, values))
                budget["PDF Number"] = file_name
                budget["Page text"] = text

            except:
                print(f"Failed to extract from Page {index} of {file_name}")

            break

    return budget


def read_details(file_name, read_pdf):

    budget = []

    for index, page in enumerate(read_pdf):

        text = page.get_text().replace("\n", "")
        if "PARA: 4 FINANCIAL POSITION" in text:

            if "GRANDTOTAL" in text or "GRAND TOTAL" in text:
                text = text.replace("GRAND TOTAL", "GRANDTOTAL").replace("Details of Closing Balance and Comments", "Comments")
            else:
                text = read_pdf[index + 1].get_text().replace("\n", "").replace("GRAND TOTAL", "GRANDTOTAL").replace("Details of Closing Balance and Comments", "Comments")
                index += 1

            tables = page.find_tables()

            found_correct_table = 0
            for table in tables:

                for name in table.header.names:
                    formatted_name = str(name).replace("_", "").replace("\n", "")
                    if "closingbalance" in formatted_name.lower():
                        found_correct_table = 1
                        break

                if found_correct_table == 1:
                    break

            if found_correct_table == 0:
                print(f"Couldn't find the correct table on page {index}")
                return

            try:
                df = table.to_pandas().replace({"\n": ""}, regex=True)
                print(df.iloc[-1])
                budget.append(df)
            except:
                print(f"Couldn't find the correct table on page {index}")
                continue

        return budget


def parse_one_municipality(path):

    municipality_budgets = []
    municipality_budget_details = []

    for file_name in tqdm(os.listdir(path)):

        if ".pdf" not in file_name:
            continue

        reader = PdfReader(path + file_name)
        municipality_budgets.append(parse_one_pdf(file_name, reader))

        reader2 = pymupdf.open(path + file_name)
        municipality_budget_details.append(read_details(file_name, reader2))

    df = pd.DataFrame(municipality_budgets)
    pdf_column = df.pop("PDF Number")
    df.insert(0, "PDF Number", pdf_column.apply(lambda x: x.split(".pdf")[0]))

    return df


def check_against_manual(df):

    manual = pd.read_csv("D:/assorted/Dropbox/ULB_Data_Odisha/Urban/Budget_Coded/BMC_Budget_Ankit.csv").dropna(subset=["PDF Number"])
    merged = pd.merge(df, manual, how="left", on="PDF Number", suffixes=("_s", "_m"))
    merged.to_csv("./ulb_budgets_merged_methods.csv", index=False)

    match = pd.DataFrame()
    match["PDF Number"] = merged["PDF Number"]
    match["OB_match"] = merged["Opening_Balance_s"] - merged["Opening_Balance_m"]
    match["Receipt_match"] = merged["Receipt_s"] - merged["Receipt_m"]
    match["Exp_match"] = merged["Expenditure_s"] - merged["Expenditure_m"]
    match["CB_match"] = merged["Closing_Balance_s"] - merged["Closing_Balance_m"]
    match["Check_match"] = merged["Check_s"] - merged["Check_m"]
    match["CB_Check_s_match"] = merged["Closing_Balance_s"] - merged["Check_s"]
    match["CB_Check_m_match"] = merged["Closing_Balance_m"] - merged["Check_m"]
    match.iloc[:, 1:] = match.iloc[:, 1:].map(lambda x: float(x) if (float(x) > 5 or float(x) < -5) else False)
    match.to_csv("./ulb_budgets_matched_methods.csv", index=False)


if __name__ == "__main__":

    municipality_name = "Dhenkanal"
    dir_path = f"D:/assorted/Dropbox/ULB_Data_Odisha/Municipality/{municipality_name}/"

    data = parse_one_municipality(dir_path)
    data.to_csv("./ulb_budgets_parsed.csv", index=False)

    check_against_manual(data)
