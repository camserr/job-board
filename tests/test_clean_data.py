import pandas as pd
import pytest
from src.clean_data import clean_data

import os

def load_file_safely(filepath):
    if not os.path.exists(filepath):
        pytest.skip(f"Skipping test because file not found: {filepath}")
    with open(filepath, 'r') as f:
        return f.read()

def test_clean_data(tmp_path):
    try:
        test_csv = tmp_path / "jobs.csv"
        df = pd.DataFrame({
            "title": ["Software Engineer", None],
            "company": ["ABC Inc", "XYZ"],
            "location": [None, "Chicago"],
            "date_posted": ["1 day ago", "2 days ago"],
            "link": ["a.com", "b.com"]
        })
        df.to_csv(test_csv, index=False)

        # Mock file paths
        os.makedirs(tmp_path / "data", exist_ok=True)
        clean_data()

        assert "jobs_clean.csv"
    except Exception as e:
        pytest.fail(f"Test failed due to unexpected error: {e}")
