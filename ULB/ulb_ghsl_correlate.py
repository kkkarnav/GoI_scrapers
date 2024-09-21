import os
import requests
import warnings
import pandas as pd
from pprint import pprint
from tqdm import tqdm
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import seaborn as sns
import matplotlib.pyplot as plt

tqdm.pandas()
warnings.filterwarnings("ignore")

import matplotlib
matplotlib.use("QtAgg")

BUDGET_DIR = "D:/assorted/Dropbox/ULB_Data_Odisha/Urban/Budget_Coded"
GHSL_DIR = "D:/code/polsci_scrapers/copernicus"


def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=2):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with both keys and matches
    """

    s = df_2[key2].tolist()

    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))
    df_1['matches'] = m

    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2

    return df_1


def match_datasets():

    ghsl = pd.read_csv(f"{GHSL_DIR}/ghsl/ghsl_main_data.csv")

    budget = cumulate_budget()

    ghsl["tv_name"] = ghsl["tv_name"].apply(lambda x: str(x))

    merged = fuzzy_merge(ghsl[["d_name", "tv_name"]], budget[["District", "Name"]], "tv_name", "Name", threshold=80, limit=1)
    merged.to_csv(f"{GHSL_DIR}/ghsl/ghsl_budget_matches.csv", index=False)


def construct_merged_dataset():

    ghsl = pd.read_csv(f"{GHSL_DIR}/ghsl/ghsl_main_data.csv")
    budget = cumulate_budget()
    matches = pd.read_csv(f"{GHSL_DIR}/ghsl/ghsl_budget_matches.csv")[["d_name", "matches"]]

    df = pd.concat([ghsl, matches["matches"]], axis=1)
    df = pd.merge(df, budget, how="inner", left_on=["d_name", "tv_name", "year"], right_on=["District", "Name", "Year"])
    df.to_csv(f"{GHSL_DIR}/ghsl/ghsl_budget_merged.csv", index=False)

    return df


def cumulate_budget():

    budget1 = pd.read_csv(f"{BUDGET_DIR}/BMC_Budget_Ankit.csv").dropna(subset=["PDF Number"])
    budget2 = pd.read_csv(f"{BUDGET_DIR}/BMC_Budget_Sahil.csv").dropna(subset=["PDF Number"])
    budget3 = pd.read_csv(f"{BUDGET_DIR}/BMC_Budget_Zavir.csv").dropna(subset=["PDF Number"])
    budget = pd.concat([budget1, budget2, budget3], ignore_index=True)

    budget = budget[["Year", "Receipt", "Expenditure", "Name", "District"]]
    budget["Year"] = budget["Year"].apply(lambda x: int(x.split("-")[0]))
    budget["Name"] = budget["Name"].apply(lambda x: str(x).replace("NAC", "").replace("Municipality", ""))

    tens = budget[budget["Year"].isin([2011, 2012, 2013, 2014, 2015])].groupby(["Name", "District"]).sum().reset_index()
    tens["Year"] = 2015
    fifteens = budget[budget["Year"].isin([2016, 2017, 2018, 2019, 2020])].groupby(["Name", "District"]).sum().reset_index()
    fifteens["Year"] = 2020
    twentys = budget[budget["Year"].isin([2021, 2022, 2023, 2024, 2025])].groupby(["Name", "District"]).sum().reset_index()
    twentys["Year"] = 2025

    fiveyearbudget = pd.concat([tens, fifteens, twentys], ignore_index=True)
    return fiveyearbudget


if __name__ == "__main__":

    # match_datasets()
    # df = construct_merged_dataset()
    df = pd.read_csv(f"{GHSL_DIR}/ghsl/ghsl_budget_merged.csv")
    df = df[df["_median"] != 0]

    print(df[["tv_name", "d_name", "year", "_median", "_median_buffer", "_growth", "_growth_buffer", "Expenditure"]])

    sns.lmplot(x="_growth", y="Expenditure", data=df)
    plt.show()
