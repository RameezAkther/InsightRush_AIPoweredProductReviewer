from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def totalReview(productUrl):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--silent")
        chrome_options.add_argument('--log-level=3')
        driver = webdriver.Chrome(options=chrome_options)
        productUrl = productUrl.replace("dp", "product-reviews") + "&pageNumber=" + str(1)
        driver.get(productUrl)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-hook="cr-filter-info-review-rating-count"]')))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        reviews = soup.find('div', {'data-hook': 'cr-filter-info-review-rating-count'})
        total_reviews_text = reviews.text.strip().split(', ')[1].split(" ")[0]
        return int(total_reviews_text.replace(",",""))
    except:
        raise RuntimeError("Unable to scrape review count")