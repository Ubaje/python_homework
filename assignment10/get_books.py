# Task 3
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(
    service=ChromeService(ChromeDriverManager().install()),
    options=options
)

url = "https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart"

try:
    driver.get(url)
    sleep(3)
    results = []
    li_elements = driver.find_elements(
        By.CSS_SELECTOR,
        'li.cp-search-result-item'
    )

    for li in li_elements:
        try:
            title_el = li.find_element(By.CSS_SELECTOR, 'span.title-content')
            title = title_el.text.strip()
        except Exception:
            title = ""
        try:
            author_els = li.find_elements(By.CSS_SELECTOR, 'a.author-link')
            authors = " ; ".join(a.text.strip() for a in author_els if a.text.strip())
        except Exception:
            authors = ""
        try:
            format_div = li.find_element(By.CSS_SELECTOR, 'div.cp-format-info')
            format_span = format_div.find_element(By.CSS_SELECTOR, 'span.display-info-primary')
            format_year = format_span.text.strip()
        except Exception:
            format_year = ""

        record = {
            "Title":       title,
            "Author":      authors,
            "Format-Year": format_year,
        }
        results.append(record)

    df = pd.DataFrame(results)
    print(df)

    # Task 4
    df.to_csv("get_books.csv", index=False)
    print("Saved get_books.csv")

    with open("get_books.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Saved get_books.json")

except Exception as e:
    print(f"Error: {type(e).__name__} – {e}")

finally:
    driver.quit()
