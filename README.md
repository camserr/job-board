# Chicago Job Market Dashboard

A small project to analyze the Chicago job market using Python, Docker, and Tableau.

## Features
- Scrapes Chicago job listings (title, company, location, posted date, link)
- Cleans and stores data into a CSV
- Deployable pipeline with GitHub Actions + Docker
- Tableau dashboard showing trends

## Tech Stack
- Python (pandas, playwright)
- Docker
- GitHub Actions (CI/CD)
- Tableau (for visualization)

## Setup

```bash
git clone https://github.com/camserr/chicago-job-dashboard.git
cd chicago-job-dashboard
pip install -r requirements.txt
python src/scraper.py
python src/clean_data.py
