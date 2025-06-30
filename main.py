from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

class LinkedInJobScraper:
    def __init__(self, keyword, max_jobs):
        self.keyword = keyword
        self.max_jobs = max_jobs
        self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.jobs_list = []

    def open_search_page(self):
        query = self.keyword.replace(" ", "%20")
        url = f"https://www.linkedin.com/jobs/search/?keywords={query}"
        self.browser.get(url)
        time.sleep(5)

    def grab_jobs(self):
        cards = self.browser.find_elements(By.CLASS_NAME, "job-card-container")
        for card in cards[:self.max_jobs]:
            try:
                job_title = card.find_element(By.CLASS_NAME, "job-card-list__title").text
                company_name = card.find_element(By.CLASS_NAME, "job-card-container__company-name").text
                location = card.find_element(By.CLASS_NAME, "job-card-container__metadata-item").text
                job_link = card.find_element(By.CLASS_NAME, "job-card-list__title").get_attribute("href")

                self.jobs_list.append({
                    "Title": job_title,
                    "Company": company_name,
                    "Location": location,
                    "URL": job_link
                })
            except Exception as err:
                print("Error in extracting job info:", err)

    def export_csv(self):
        df = pd.DataFrame(self.jobs_list)
        df.to_csv("linkedin_jobs.csv", index=False)
        print("Jobs saved in linkedin_jobs.csv file.")

    def run_scraper(self):
        self.open_search_page()
        self.grab_jobs()
        self.export_csv()
        self.browser.quit()

if __name__ == "__main__":
    job = input("Enter job title: ")
    count = int(input("How many jobs to fetch? "))

    scraper = LinkedInJobScraper(job, count)
    scraper.run_scraper()