import pandas as pd
import os

INPUT_PATH = os.path.join("data", "jobs.csv")
OUTPUT_PATH = os.path.join("data", "jobs_clean.csv")

def clean_data():
    df = pd.read_csv(INPUT_PATH)

    df.dropna(subset=["title", "company"], inplace=True)
    df["company"] = df["company"].str.strip()
    df["title"] = df["title"].str.strip()
    df["location"] = df["location"].fillna("Chicago, IL")
    df.drop_duplicates(subset=["title", "company"], inplace=True)

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Cleaned data saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    clean_data()
