from playwright.sync_api import sync_playwright
import pandas as pd
import time
import os

OUTPUT_PATH = os.path.join("data", "jobs.csv")

def scrape_jobs():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Example query (You can adjust later)
        page.goto("https://www.indeed.com/jobs?q=software+engineer&l=Chicago%2C+IL")
        time.sleep(3)

        titles, companies, locations, dates, links = [], [], [], [], []

        job_cards = page.query_selector_all('div.job_seen_beacon')

        for job in job_cards:
            title = job.query_selector('h2 span')
            company = job.query_selector('span.companyName')
            location = job.query_selector('div.companyLocation')
            date = job.query_selector('span.date')
            link = job.query_selector('a')

            titles.append(title.inner_text() if title else None)
            companies.append(company.inner_text() if company else None)
            locations.append(location.inner_text() if location else None)
            dates.append(date.inner_text() if date else None)
            links.append("https://indeed.com" + link.get_attribute("href") if link else None)

        df = pd.DataFrame({
            "title": titles,
            "company": companies,
            "location": locations,
            "date_posted": dates,
            "link": links
        })

        os.makedirs("data", exist_ok=True)
        df.to_csv(OUTPUT_PATH, index=False)
        browser.close()

if __name__ == "__main__":
    scrape_jobs()
