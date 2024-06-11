from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from .maxFile import get_max_numbered_csv
from bs4 import BeautifulSoup
import re
import requests
import pandas as pd

review_data = []

def totalReviews(productUrl):
    try:
        resp = requests.get(productUrl)
        soup = BeautifulSoup(resp.text, 'html.parser')
        reviews_span = soup.select_one('#container > div > div._2tsNFb > div > div._1YokD2._2GoDe3.col-12-12 > div._1YokD2._3Mn1Gg.col-9-12 > div:nth-child(2) > div > div.col-4-12._17ETNY > div > div:nth-child(3) > div > span')
        if reviews_span:
            text = reviews_span.get_text(strip=True)
            numbers = re.findall(r'\d+', text.replace(',', ''))
            if numbers:
                return int(numbers[0])
        return 0
    except:
        raise RuntimeError("Unable to get the review count")

def extractReviews(driver, review_url):
    try:
        driver.get(review_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._1AtVbE.col-12-12')))
        read_more_links = driver.find_elements(By.XPATH, "//span[contains(@class, '_1BWGvX') and contains(., 'READ MORE')]")
        for link in read_more_links:
            try:
                link.click()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div._1AtVbE.col-12-12')))
            except Exception as e:
                print("Failed to click on link:", e)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        review_divs = soup.find_all('div', class_='_1AtVbE col-12-12')
        for div in review_divs:
            rating = None
            title = None
            review_description = None
            rating_elem = div.find('div', class_='_3LWZlK _1BLPMq')
            if rating_elem:
                rating = rating_elem.text.strip()
            title_elem = div.find('p', class_='_2-N8zT')
            if title_elem:
                title = title_elem.text.strip()
            review_desc_elem = div.find('div', class_='')
            if review_desc_elem:
                review_description = review_desc_elem.text.strip()
            if rating and title and review_description:
                review_data.append({
                    'Rating': rating,
                    'Review Title': title,
                    'Review Body': review_description[:-9]
                })
    except:
        raise RuntimeError("Unable to scrape reviews.")

def get_review(prod):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--silent")
        chrome_options.add_argument('--log-level=3')
        driver = webdriver.Chrome(options=chrome_options)
        productUrl = prod
        reviewUrl = productUrl.replace("/p/", "/product-reviews/")
        totalRev = totalReviews(reviewUrl)
        if totalRev >= 300:
            totalPg = 30
        elif totalRev == 0:
            print("No reviews present!")
            return None
        else:
            totalPg = totalRev // 10 + 1
        print("\nTotal number of review pages: ",totalPg)
        temp = int(input("Enter the number of pages you want to scrape (1 page have 10 reviews): "))
        if temp <= 0 or temp > totalPg:
            print("Invalid Input!")
            driver.quit()
            return None
        else:
            totalPg = temp
        for i in range(totalPg):
            try: 
                reviewUrl = reviewUrl + "&page=" + str(i+1)
                extractReviews(driver, reviewUrl)
            except Exception as e:
                print(e)
    except Exception as e:
        driver.quit()
        raise ("Internal Error. ",e)
    finally:
        driver.quit()
    try:
        if review_data == []:
            raise RuntimeError("No data is collected")
        else:
            df = pd.DataFrame(review_data)
            dir = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data"
            prodName = int(get_max_numbered_csv(dir).replace(".csv",""))
            prodName = prodName + 1
            file_path = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data\\" + str(prodName) + ".csv"
            df.to_csv(file_path)
            print("Reviews are successfully collected and saved as ", str(prodName) ,".csv")
    except:
        raise RuntimeError("Unable to create CSV")
    
# test run
#get_review("https://www.flipkart.com/poco-m6-pro-5g-power-black-128-gb/p/itmef8fa46f89738?pid=MOBGRNZ3ER4N3K4F&lid=LSTMOBGRNZ3ER4N3K4FIYYGCU&marketplace=FLIPKART&store=tyy%2F4io&spotlightTagId=BestsellerId_tyy%2F4io&srno=b_1_1&otracker=browse&fm=organic&iid=a96206e1-4f7c-485d-afcb-4c1c375aefff.MOBGRNZ3ER4N3K4F.SEARCH&ppt=browse&ppn=browse&ssid=cnrb9gfj4g0000001712828975745")