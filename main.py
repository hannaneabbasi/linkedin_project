from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import os

class JobScraper:
    def __init__(self, job_title, limit=10):
        self.job_title = job_title
        self.limit = limit
        self.driver = None
        self.results = []

    def setup_driver(self):
        path = os.path.join(os.getcwd(), "chromedriver.exe")
        service = Service(path)
        self.driver = webdriver.Chrome(service=service)

    def build_url(self):
        base = "https://www.linkedin.com/jobs/search/"
        keyword = self.job_title.replace(" ", "%20")
        return f"{base}?keywords={keyword}&location=Worldwide"

    def scrape(self):
        self.setup_driver()
        self.driver.get(self.build_url())
        time.sleep(3)

        jobs = self.driver.find_elements(By.CLASS_NAME, "base-search-card")[:self.limit]

        for job in jobs:
            try:
                title = job.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
                company = job.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
                location = job.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()
                link = job.find_element(By.TAG_NAME, "a").get_attribute("href")

                self.results.append({
                    "Job Title": title,
                    "Company": company,
                    "Location": location,
                    "Link": link
                })
            except Exception as e:
                print("Error:", e)
                continue

        self.driver.quit()

    def export_to_csv(self, filename="job_listings.csv"):
        df = pd.DataFrame(self.results)
        df.to_csv(filename, index=False)
        print(f"Saved to {filename}")

if __name__ == "__main__":
    scraper = JobScraper("data analyst", limit=10)
    scraper.scrape()
    scraper.export_to_csv()