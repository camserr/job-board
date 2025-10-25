import time
import pandas as pd
from playwright.sync_api import sync_playwright
import os

OUTPUT_PATH = os.path.join("data", "jobs.csv")


class BaseScraper:
    def __init__(self, job_type, location):
        self.job_type = job_type
        self.location = location

    def fetch_page(self, page):
        raise NotImplementedError("fetch_page method must be implemented by subclass")

    def parse_jobs(self, page):
        raise NotImplementedError("parse_jobs method must be implemented by subclass")

    def scrape_jobs(self, browser):
        page = browser.new_page()
        self.fetch_page(page)
        time.sleep(3)  # wait for page to load
        return self.parse_jobs(page)


class LinkedInScraper(BaseScraper):
    def fetch_page(self, page):
        url = f"https://www.linkedin.com/jobs/search/?keywords={self.job_type.replace(' ', '%20')}&location={self.location.replace(' ', '%20')}"
        page.goto(url)

    def parse_jobs(self, page):
        titles, companies, locations, dates, links = [], [], [], [], []
        job_cards = page.query_selector_all('ul.jobs-search__results-list li')

        for job in job_cards:
            title = job.query_selector('h3.base-search-card__title')
            company = job.query_selector('h4.base-search-card__subtitle')
            location = job.query_selector('span.job-search-card__location')
            date = job.query_selector('time')
            link = job.query_selector('a.base-card__full-link')

            titles.append(title.inner_text().strip() if title else None)
            companies.append(company.inner_text().strip() if company else None)
            locations.append(location.inner_text().strip() if location else None)
            dates.append(date.get_attribute('datetime') if date else None)
            links.append(link.get_attribute('href') if link else None)

        df = pd.DataFrame({
            "title": titles,
            "company": companies,
            "location": locations,
            "date_posted": dates,
            "link": links
        })
        return df


class GrepJobScraper(BaseScraper):
    def fetch_page(self, page):
        url = f"https://grepjob.com/jobs?q={self.job_type.replace(' ', '+')}&l={self.location.replace(' ', '+')}"
        page.goto(url)

    def parse_jobs(self, page):
        titles, companies, locations, dates, links = [], [], [], [], []
        job_cards = page.query_selector_all('div.job-listing')

        for job in job_cards:
            title = job.query_selector('h2.job-title')
            company = job.query_selector('div.company-name')
            location = job.query_selector('div.job-location')
            date = job.query_selector('span.posted-date')
            link = job.query_selector('a.job-link')

            titles.append(title.inner_text().strip() if title else None)
            companies.append(company.inner_text().strip() if company else None)
            locations.append(location.inner_text().strip() if location else None)
            dates.append(date.inner_text().strip() if date else None)
            links.append(link.get_attribute('href') if link else None)

        df = pd.DataFrame({
            "title": titles,
            "company": companies,
            "location": locations,
            "date_posted": dates,
            "link": links
        })
        return df


class NewGradJobsScraper(BaseScraper):
    def fetch_page(self, page):
        url = f"https://www.newgrad-jobs.com/jobs?search={self.job_type.replace(' ', '+')}&location={self.location.replace(' ', '+')}"
        page.goto(url)

    def parse_jobs(self, page):
        titles, companies, locations, dates, links = [], [], [], [], []
        job_cards = page.query_selector_all('div.job-card')

        for job in job_cards:
            title = job.query_selector('h3.job-title')
            company = job.query_selector('div.company')
            location = job.query_selector('span.location')
            date = job.query_selector('span.date-posted')
            link = job.query_selector('a.job-link')

            titles.append(title.inner_text().strip() if title else None)
            companies.append(company.inner_text().strip() if company else None)
            locations.append(location.inner_text().strip() if location else None)
            dates.append(date.inner_text().strip() if date else None)
            links.append(link.get_attribute('href') if link else None)

        df = pd.DataFrame({
            "title": titles,
            "company": companies,
            "location": locations,
            "date_posted": dates,
            "link": links
        })
        return df


def get_scraper(site_name, job_type, location):
    scrapers = {
        "linkedin": LinkedInScraper,
        "grepjob": GrepJobScraper,
        "newgrad": NewGradJobsScraper
    }
    scraper_class = scrapers.get(site_name.lower())
    if not scraper_class:
        raise ValueError(f"Unsupported site: {site_name}")
    return scraper_class(job_type, location)


def scrape_jobs(site_name, job_type, location, browser):
    scraper = get_scraper(site_name, job_type, location)
    return scraper.scrape_jobs(browser)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        site_name = "linkedin"
        job_type = "software engineer"
        location = "Chicago, IL"
        df = scrape_jobs(site_name, job_type, location, browser)
        os.makedirs("data", exist_ok=True)
        df.to_csv(OUTPUT_PATH, index=False)
        browser.close()


if __name__ == "__main__":
    main()
