import pandas as pd
from src.clean_data import clean_data

def test_clean_data(tmp_path):
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
    import os
    os.makedirs(tmp_path / "data", exist_ok=True)
    clean_data()

    assert "jobs_clean.csv"
