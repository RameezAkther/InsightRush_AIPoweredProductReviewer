import requests
import pandas as pd
from bs4 import BeautifulSoup
from .maxFile import get_max_numbered_csv

review_data = []

def extractReviews(reviewUrl):
    try:
        resp = requests.get(reviewUrl)
        soup = BeautifulSoup(resp.text, 'html.parser')
        review_divs = soup.find_all('div', {"class":"col EPCmJX Ma1fCG"})
        for div in review_divs:
            rating = None
            title = None
            review_description = None
            
            rating_elem = div.find('div', {"class":"XQDdHH Ga3i8K"})
            if rating_elem:
                rating = rating_elem.text.strip()

            title_elem = div.find('p', {"class":"z9E0IG"})
            if title_elem:
                title = title_elem.text.strip()

            review_desc_elem = div.find('div', {"class":"ZmyHeo"})
            if review_desc_elem:
                review_description = review_desc_elem.text.strip()

            if rating and title and review_description:
                review_data.append({
                    'Rating': rating,
                    'Review Title': title,
                    'Review Body': review_description[:-9]
                })
    except Exception as e:
        raise RuntimeError("Unable to scrape reviews")

def get_review(prod, totalPg):
    try:
        productUrl = prod
        reviewUrl = productUrl.replace("/p/", "/product-reviews/")
    
        #print("Number of reviews found ",totalRev)
        #print("Number of review pages : ",totalPg)

        totalPg = int(totalPg)
        #temp = int(input("Enter the number of review pages you want to scrape (1 page has 10 reviews) : "))
        for i in range(totalPg):
            try: 
                reviewUrl = reviewUrl + "&page=" + str(i+1)
                extractReviews(reviewUrl)
            except Exception as e:
                print("Error occured: ",e)
    except Exception as e:
        raise RuntimeError("Internal Error. ",e)

    try:
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
#get_review("https://www.flipkart.com/motorola-envisionx-165-cm-65-inch-qled-ultra-hd-4k-smart-google-tv-dolby-vision-atmos/product-reviews/itm767828569c629?pid=TVSGRTDDGYA4HPWU&lid=LSTTVSGRTDDGYA4HPWUZVEWYT&marketplace=FLIPKART",2)