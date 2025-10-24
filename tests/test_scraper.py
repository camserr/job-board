import pandas as pd
import os

def test_output_exists():
    assert os.path.exists("data/raw_jobs.csv")

def test_columns_present():
    df = pd.read_csv("data/raw_jobs.csv")
    expected = {"title", "company", "location", "date_posted", "link", "search_query"}
    assert expected.issubset(df.columns)
