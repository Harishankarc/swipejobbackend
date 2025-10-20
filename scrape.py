from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/120.0.0.0 Safari/537.36")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
    "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/120.0.0.0 Safari/537.36"
})

base_url = "https://in.indeed.com/jobs?q=software+developer&l=Kerala"

all_jobs = []

for page in range(0, 10):
    start = page * 10
    url = f"{base_url}&start={start}"
    print(f"\n🔍 Scraping page {page + 1}: {url}")

    driver.get(url)
    time.sleep(6)

    for i in range(2):
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_cards = soup.find_all("div", class_="job_seen_beacon")

    if not job_cards:
        print("⚠️ No more job cards found — stopping early.")
        break

    for job_card in job_cards:
        title_tag = job_card.find("h2", {"class": lambda x: x and "jobTitle" in x})
        title = title_tag.get_text(strip=True) if title_tag else None

        company_tag = job_card.find(attrs={"data-testid": "company-name"})
        company = company_tag.get_text(strip=True) if company_tag else None

        location_tag = job_card.find(attrs={"data-testid": "text-location"})
        location = location_tag.get_text(strip=True) if location_tag else None

        link_tag = job_card.find("a", href=True)
        job_link = "https://in.indeed.com" + link_tag["href"] if link_tag else None

        if any([title, company, location]):
            all_jobs.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Link": job_link
            })

    print(f"✅ Found {len(job_cards)} jobs on page {page + 1}")

driver.quit()

df = pd.DataFrame(all_jobs)
df.to_csv("indeed_jobs_list.csv", index=False, encoding="utf-8")

print(f"\n🎉 Scraped total {len(df)} jobs from {page + 1} pages.")
print("📁 Saved as indeed_jobs.csv")
