import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from pprint import pprint
import os
import sys
import re
import warnings
from llama_cpp import Llama
from pypdf import PdfReader
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import download
from transformers import pipeline
from textblob import TextBlob


BASE_PATH = "D:/assorted/Dropbox/UP_SEAC"
verbose = False
tqdm.pandas()
warnings.filterwarnings("ignore")
classifier = pipeline("text-classification", model="nlpaueb/legal-bert-base-uncased")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def parse_members(text):
    pattern = r'\d+\.\s*(.*?)(?=\d+\.|$)'
    matches = re.findall(pattern, text, re.DOTALL)
    result = [[x.strip() for x in match.strip().split(",")][:2] for match in matches]
    result = "; ".join([f"{x[0]} ({x[1]})" for x in result])
    return result


def construct_parsed_csv():
    files = [file for file in os.listdir(f"{BASE_PATH}") if file.endswith(".pdf")]
    members = []

    for minutes_file in tqdm(files):
        
        try:
            reader = PdfReader(f"{BASE_PATH}/{minutes_file}")
            text = reader.pages[0].extract_text().replace("\n", "")
            
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text().replace("\n", "")
            
            pattern = r'(?:\S*)/?[A-Za-z]+/UP/[A-Za-z]+/\d+/\d+'
            matches = "; ".join(re.findall(pattern, full_text))
            
            pattern = r'\d+/\d+/20\d+'
            found_date = re.findall(pattern, text)[0]
            
            if text.strip().split(" ")[0] == "Minutes" and "The Chairman welcomed" in text:
                if "Following members " in text:
                    parsed_text = (minutes_file, parse_members(text.split("The Chairman welcomed")[0].split("Following members ")[1]), matches, found_date)
                else:
                    parsed_text = (minutes_file, parse_members(text.split("The Chairman welcomed")[0]), matches, found_date)
            elif text.strip().split(" ")[0] == "Minutes" and "The Chairperson welcomed" in text:
                if "Following members " in text:
                    parsed_text = (minutes_file, parse_members(text.split("The Chairperson welcomed")[0].split("Following members ")[1]), matches, found_date)
                else:
                    parsed_text = (minutes_file, parse_members(text.split("The Chairperson welcomed")[0]), matches, found_date)
            else:
                if "Following members " in text:
                    parsed_text = (minutes_file, parse_members(text[:1000].split("Following members ")[1]), matches, found_date)
                else:
                    parsed_text = (minutes_file, parse_members(text[:1000]), matches, found_date)
        
        except:
            parsed_text = (minutes_file, "", "", "")

        members.append(parsed_text)
    
    df = pd.DataFrame(members, columns=["filename", "member_text", "project_ids", "date"])
    df.to_csv(f"D:/code/polsci_scrapers/parivesh/parsed_data.csv", index=False)


def sentiment_analysis():
    
    download('vader_lexicon')
    sia = SentimentIntensityAnalyzer()
    
    files = [file for file in os.listdir(f"{BASE_PATH}") if file.endswith(".pdf")]
    extracted = []
    for minutes_file in tqdm(files):
        
        reader = PdfReader(f"{BASE_PATH}/{minutes_file}")
        text = reader.pages[0].extract_text().replace("\n", "")
        
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text().replace("\n", "")
        
        pattern = r'(?:\S*)/?[A-Za-z]+/UP/[A-Za-z]+/\d+/\d+'
        matches = list(dict.fromkeys(re.findall(pattern, full_text)))
        
        for index, match in enumerate(matches):
            
            ender = "Annexure-1" if index == len(matches)-1 else matches[index+1]
            instances = full_text.split(match)[1:]
            text = " ".join(" ".join(instances).split(ender)[:-1])
            
            sentiment = sia.polarity_scores(text)
            first512 = classifier(text[:512])[0]["score"]
            last512 = classifier(text[-512:])[0]["score"]
            blob = TextBlob(text).sentiment
            
            extracted.append([index+1, match, len(instances), len(text), sentiment["neg"], sentiment["neu"], sentiment["pos"], sentiment["compound"], first512, last512, blob.polarity, blob.subjectivity])
            
    extract_df = pd.DataFrame(extracted, columns=["meeting_index", "project_id", "num_instances", "num_words", "neg", "neu", "pos", "compound", "first512", "last512", "polarity", "subjectivity"])
    extract_df.to_csv(f"D:/code/polsci_scrapers/parivesh/sentiment_data.csv", index=False)
    print(extract_df)


def summarize_text():
    
    files = [file for file in os.listdir(f"{BASE_PATH}") if file.endswith(".pdf")]
    summarized = []
    for minutes_file in tqdm(files[:10]):
        
        reader = PdfReader(f"{BASE_PATH}/{minutes_file}")
        text = reader.pages[0].extract_text().replace("\n", "")
        
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text().replace("\n", "")
        
        pattern = r'(?:\S*)/?[A-Za-z]+/UP/[A-Za-z]+/\d+/\d+'
        matches = list(dict.fromkeys(re.findall(pattern, full_text)))
        
        for index, match in enumerate(matches):
            
            ender = "Annexure-1" if index == len(matches)-1 else matches[index+1]
            instances = full_text.split(match)[1:]
            text = " ".join(" ".join(instances).split(ender)[:-1])
            
            firstsummary = summarizer(text[:2048], max_length=300, min_length=30, do_sample=False)
            lastsummary = summarizer(text[-2048:], max_length=300, min_length=30, do_sample=False)
            summarized.append([index+1, match, firstsummary[0]['summary_text'], lastsummary[0]['summary_text']])
        
    sum_df = pd.DataFrame(summarized, columns=["meeting_index", "project_id", "firstsummary", "lastsummary"])
    sum_df.to_csv(f"D:/code/polsci_scrapers/parivesh/summary_data.csv", index=False)
    print(sum_df)


def llm_parse():
    llm = Llama.from_pretrained(
        repo_id="TheBloke/SynthIA-7B-v2.0-16k-GGUF",
        filename="synthia-7b-v2.0-16k.Q2_K.gguf",
        n_ctx=4096,
        # number of layers to offload to the GPU 
        # GPU is not strictly required but it does help
        n_gpu_layers=32,
        # number of tokens in the prompt that are fed into the model at a time
        n_batch=1024,
        # use half precision for key/value cache; set to True per langchain doc
        f16_kv=True,
        verbose=verbose,
    )

    question = input("Give me the question and data:")
    output = llm(
        question,
        max_tokens=2048,
        temperature=0.3,
        top_p=0.1
    )
    print(f"\n{output}")
    print(output["choices"][0]["text"])


if __name__ == "__main__":
    # construct_parsed_csv()
    # sentiment_analysis()
    summarize_text()
