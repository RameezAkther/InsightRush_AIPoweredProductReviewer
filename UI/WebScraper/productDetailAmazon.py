import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from .maxFile import get_max_numbered_jpg

prodDetail = {}

def getTitle(soup):
    try:
        t = soup.select_one('#productTitle')
        prodDetail['Title'] = t.text
    except:
        prodDetail['Title'] = " "

def getCurrentPrice(soup):
    try:
        symbol = soup.select_one('#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-symbol').text
        t = soup.select_one('#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole')
        prodDetail['Current Price'] = symbol + t.text
    except:
        prodDetail['Current Price'] = " "
    
def getInfo(soup):
    try:
        list_items = soup.select_one('#feature-bullets > ul')
        list_items_text = [item.get_text(strip=True) for item in list_items]
        filtered_list = [item for item in list_items_text if item]
        prodDetail['About'] = filtered_list
    except:
        prodDetail['About'] = " "

def amazonAI(soup):
    try:
        t = soup.select_one('#product-summary > p.a-spacing-small > span')
        prodDetail['Amazon AI'] = t.text
    except:
        prodDetail['Amazon AI'] = " "
    
def getImage(soup):
    try:
        image_tag = soup.select_one('#landingImage')
        image_url = image_tag['src']
        dir = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Image"
        img_name = int(get_max_numbered_jpg(dir).replace(".jpg", ""))
        img_name += 1
        img_name = str(img_name)
        response = requests.get(image_url)
        path = f"C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Image\\{img_name}.jpg"
        with open(path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        dir = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Image"
        print(f"Error getting image: {e}")
        img_name = int(get_max_numbered_jpg(dir).replace(".jpg", ""))
        img_name += 1
        img_name = str(img_name)
        path = f"C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Image\\{img_name}.jpg"
        with open(path, 'wb') as f:
            f.write(b'Dummy content')

def get_html(productUrl, driver):
    try:
        driver.get(productUrl)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*')))
        html_content = driver.page_source
        driver.quit()
        return html_content
    except:
        driver.quit()
        return None
    
def get_data(productUrl,driver):
    try:
        html = get_html(productUrl,driver)
        soup = BeautifulSoup(html, 'html.parser')
        getTitle(soup)
        getCurrentPrice(soup)
        getInfo(soup)
        amazonAI(soup)
        getImage(soup)
    except:
        raise RuntimeError("Unable to get data")

def ext(prod):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--silent")
        chrome_options.add_argument('--log-level=3')
        driver = webdriver.Chrome(options=chrome_options)
        get_data(prod,driver)
        return prodDetail
    except:
        raise RuntimeError("Unable to get product info (Amazon)")

# test run
#ext("https://www.amazon.in/Xiaomi-inches-Vision-Google-L50M8-A2IN/dp/B0CH31C1BR/ref=sr_1_1_sspa?dib=eyJ2IjoiMSJ9.wJOzhbBKpQgolxe4lGBuoCUrXbxzpMOAxzXJIgwJvEUuXumWdDpTdCD0nXp6FxNolHVI8fbPwH8KlijHTFHE1sV9EAZl27_KskBpE3Llyk8DCp1Bb9_cysi1laJ_x50HmhIIq8N7-UUHb9RPxs-DAL4IySSXaQgfHmlmRLLIuFNCoC2sl-9O0zvUiQ3Z_S-X09n8a2XkzChMKj57FbanKXBVdc2xO7Oy0Q6LqUhpbr8.zwyZfZxZONuaFCZ27DCqxzunhBJS2thPW08dmTcEkTg&dib_tag=se&keywords=tv&qid=1712837408&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1")


"""
prodDetail['Title'] = soup.select_one('#productTitle').text
symbol = soup.select_one('#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-symbol').text
prodDetail['Price'] = symbol + soup.select_one('#corePriceDisplay_desktop_feature_div > div.a-section.a-spacing-none.aok-align-center.aok-relative > span.a-price.aok-align-center.reinventPricePriceToPayMargin.priceToPay > span:nth-child(2) > span.a-price-whole').text
list_items = soup.select_one('#feature-bullets > ul')
list_items_text = [item.get_text(strip=True) for item in list_items]
filtered_list = [item for item in list_items_text if item]
prodDetail['About'] = filtered_list
list_items = soup.select_one('#feature-bullets > ul')
list_items_text = [item.get_text(strip=True) for item in list_items]
filtered_list = [item for item in list_items_text if item]
prodDetail['About'] = filtered_list

prodDetail['Amazon AI'] = soup.select_one('#product-summary > p.a-spacing-small > span').text
image_tag = soup.select_one('#landingImage')
image_url = image_tag['src']
dir = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Image"
img_name = int(get_max_numbered_jpg(dir).replace(".jpg",""))
img_name = img_name + 1
response = requests.get(image_url)
path = ".\\Image\\"+str(img_name)+".jpg"
with open(path, 'wb') as f:
    f.write(response.content)
"""