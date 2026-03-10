# Task 6
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://owasp.org/Top10/2025/"

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver


def scrape_owasp_top10():
    driver = get_driver()
    vulnerabilities = []

    try:
        driver.get(URL)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(),'Top 10:2025 List')]/following-sibling::ol[1]"))
        )
        anchor_xpath = "//h3[contains(text(),'Top 10:2025 List')]/following-sibling::ol[1]/li/a"
        anchors = driver.find_elements(By.XPATH, anchor_xpath)

        for anchor in anchors:
            title = anchor.text.strip()
            href = anchor.get_attribute("href")
            vulnerabilities.append({"title": title, "href": href})

    finally:
        driver.quit()

    return vulnerabilities


def write_to_csv(data, filename="owasp_top_10.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["title", "href"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"\nData written to {filename}")


if __name__ == "__main__":
    print("Scraping OWASP Top 10:2025...\n")
    data = scrape_owasp_top10()

    print("Scraped vulnerabilities:")
    for item in data:
        print(item)

    write_to_csv(data)