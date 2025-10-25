import pytest
import pandas as pd
import os
from playwright.sync_api import sync_playwright
from src.scraper import scrape_jobs, LinkedInScraper, GrepJobScraper, NewGradJobsScraper

OUTPUT_PATH = os.path.join("data", "jobs.csv")

@pytest.fixture(scope="module")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        yield browser
        browser.close()

# Unit test: test parsing logic with sample HTML (mocked)
# This would normally use a library like responses or pytest-playwright for mocking
# Here we just test the parse_jobs method with a minimal example

def test_linkedin_parse_jobs_with_no_jobs():
    scraper = LinkedInScraper("software engineer", "Chicago, IL")
    class DummyPage:
        def query_selector_all(self, selector):
            return []  # no jobs
    df = scraper.parse_jobs(DummyPage())
    assert df.empty

# Integration test: test full scrape flow for LinkedIn

def test_scrape_linkedin(browser):
    site_name = "linkedin"
    job_type = "software engineer"
    location = "Chicago, IL"
    df = scrape_jobs(site_name, job_type, location, browser)
    assert not df.empty
    assert set(["title", "company", "location", "date_posted", "link"]).issubset(df.columns)

# Regression test: compare output to saved snapshot
# For simplicity, we just check columns and row count here

def test_regression_output_file_exists():
    assert os.path.exists(OUTPUT_PATH)

def test_regression_output_row_count():
    df = pd.read_csv(OUTPUT_PATH)
    # Expect at least 1 job listing
    assert len(df) > 0

# Error handling test: simulate empty page

def test_parse_jobs_empty_page():
    scraper = GrepJobScraper("software engineer", "Chicago, IL")
    class DummyPage:
        def query_selector_all(self, selector):
            return []
    df = scraper.parse_jobs(DummyPage())
    assert df.empty

# Data validation test: check columns and non-empty values

def test_data_validation():
    df = pd.read_csv(OUTPUT_PATH)
    expected_cols = ["title", "company", "location", "date_posted", "link"]
    for col in expected_cols:
        assert col in df.columns
        assert df[col].dropna().apply(lambda x: isinstance(x, str) and len(x) > 0).all()

# End-to-end test: run scraper and check output file

def test_end_to_end(browser):
    site_name = "linkedin"
    job_type = "software engineer"
    location = "Chicago, IL"
    df = scrape_jobs(site_name, job_type, location, browser)
    os.makedirs("data", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    assert os.path.exists(OUTPUT_PATH)

# Performance test: measure scraping time (basic)
import time as time_module

def test_performance_scrape_linkedin(browser):
    site_name = "linkedin"
    job_type = "software engineer"
    location = "Chicago, IL"
    start = time_module.time()
    df = scrape_jobs(site_name, job_type, location, browser)
    duration = time_module.time() - start
    assert duration < 30  # expect scrape to complete within 30 seconds

# Mocking external dependencies would require more setup and libraries,
# so here we just demonstrate the idea with a dummy test

def test_mocking_example():
    class DummyBrowser:
        def new_page(self):
            class DummyPage:
                def goto(self, url):
                    pass
                def query_selector_all(self, selector):
                    return []
            return DummyPage()
    dummy_browser = DummyBrowser()
    scraper = LinkedInScraper("software engineer", "Chicago, IL")
    df = scraper.scrape_jobs(dummy_browser)
    assert df.empty
