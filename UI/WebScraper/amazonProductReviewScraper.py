import pandas as pd
from bs4 import BeautifulSoup
from .maxFile import get_max_numbered_csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import keyboard


reviewlist = []

def extractReviews(driver, reviewUrl, pageNumber):
    try:
        driver.get(reviewUrl)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-hook="review"]')))
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        reviews = soup.findAll('div', {'data-hook': 'review'})
        for item in reviews:
            review = {
                'productTitle': soup.title.text.replace("Amazon.in:Customer reviews: ", "").strip(),
                'Rating': item.find('i', {'data-hook': 'review-star-rating'}).text.strip(),
                'Review Title': item.find('a', class_='review-title').get_text(strip=True).split('stars')[1],
                'Review Body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        raise RuntimeError("Unable to scrape reviews")

def get_review(prod, pg):
    productUrl = prod
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--silent")
    chrome_options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=chrome_options)
    pg = int(pg)
    try:
        reviewUrl = productUrl.replace("dp", "product-reviews") + "&pageNumber=" + str(1)
        #totalRev = totalReview(driver, reviewUrl)
        if pg == 0:
            #print("No customer reviewed the product!")
            driver.quit()
            return None
        else:
            #totalPg = totalRev // 10 + 1
            #print("\nTotal number of reviews available ",totalRev)
            #print("Total number of pages ",totalPg)
            #pg = int(input("Enter the number of pages you want to scrape (1 page will have 10 reviews) : "))
            for i in range(1, pg + 1):
                if keyboard.is_pressed('q'):
                    print("Stopping scraping...")
                    break
                try: 
                    reviewUrl = productUrl.replace("dp", "product-reviews") + "&pageNumber=" + str(i)
                    extractReviews(driver, reviewUrl, i)
                except Exception as e:
                    print(f"Error scraping page {i}: {e}")
    except Exception as e:
        driver.quit()
        raise RuntimeError("Internal Error. ",e)
    finally:
        driver.quit()
    try:
        if reviewlist == []:
            raise RuntimeError("No data is collected")
        else:
            df = pd.DataFrame(reviewlist)
            dir = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data"
            prodName = int(get_max_numbered_csv(dir).replace(".csv",""))
            prodName = prodName + 1
            file_path = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Scraped Data\\" + str(prodName) + ".csv"
            df.to_csv(file_path)
            print("Reviews are successfully collected and saved as ", prodName ,".csv")
    except:
        raise RuntimeError("Unable to create CSV")

#test
#get_review("https://www.amazon.in/HP-i5-12450H-15-6-inch-Response-fa0666TX/dp/B0C2HZYM87/ref=cm_cr_arp_d_pdt_img_top?ie=UTF8&th=1",5)