from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

prodDetail = {}

def getSauce(prodLink):
    try:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("--silent")
        chrome_options.add_argument('--log-level=3')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://pricehistory.app")
        search_bar = driver.find_element("id","search")
        product_url = prodLink
        search_bar.send_keys(product_url)
        search_bar.send_keys(Keys.RETURN)
        time.sleep(7)
        html_content = driver.page_source
        driver.quit()
        return html_content
    except:
        driver.quit()
        raise Exception('Unable to get info in pricehistory.com')
    finally:
        driver.quit()

def getTitle(soup):
    try:
        t = soup.select_one('body > div > div:nth-child(6) > div.col-md-12.col-lg-7.col-xl-8 > div > div.col-lg-9.col-md-9.col-sm-8.col-8.ph-title.my-0.pl-2.p-1 > h1')
        prodDetail['Title'] = t.text
    except:
        prodDetail['Title'] = " "

def getHighPrice(soup):
    try:
        t = soup.select_one('body > div > div:nth-child(6) > div.col-12.px-0.py-2.all-time-price-overview.small > div > div.col.bg-danger.text-light > span.amount')
        prodDetail['Highest Price'] = t.text
    except:
        prodDetail['Highest Price'] = " "

def getHighPriceDate(soup):
    try:
        t = soup.select_one('body > div > div:nth-child(6) > div:nth-child(9) > table > tbody > tr:nth-child(2) > td')
        prodDetail['Date of highest price'] = t.text.strip()
    except:
        prodDetail['Date of highest price'] = " "
    
def getAvgPrice(soup):
    try:
        t = soup.select_one('body > div > div:nth-child(6) > div.col-12.px-0.py-2.all-time-price-overview.small > div > div.col.bg-warning.text-dark > span.amount')
        prodDetail['Average Price'] = t.text.strip()
    except:
        prodDetail['Average Price'] = " "
    
def getAvgPriceDate(soup):
    try:
        t = soup.select_one('body > div > div:nth-child(6) > div:nth-child(9) > table > tbody > tr:nth-child(4) > td')
        prodDetail['Average Price as of'] = t.text.strip()
    except:
        prodDetail['Average Price as of'] = " "
    
def getLowPrice(soup):
    try:
        t = soup.select_one('body > div > div:nth-child(6) > div.col-12.px-0.py-2.all-time-price-overview.small > div > div.col.bg-info.text-light > span.amount')
        prodDetail['Lowest Price'] = t.text.strip()
    except:
        prodDetail['Lowest Price'] = " "

def getLowPriceDate(soup):
    try:
        t = soup.select_one('body > div > div:nth-child(6) > div.col-12.px-0.py-2.all-time-price-overview.small > div > div.col.bg-info.text-light > span.amount')
        prodDetail['Date of lowest price'] = t.text
    except:
        prodDetail['Date of lowest price'] = " "

def getCurrentPrice(soup):
    try:
        t = soup.select_one('body > div > div:nth-child(6) > div.col-md-12.col-lg-5.col-xl-4.ph-pricing.mt-2.mb-2.border.shadow-sm.p-2.bg-light > div.ph-pricing-pricing')
        prodDetail['Current Price'] = t.text
    except:
        prodDetail['Current Price'] = " "

def getLabelPrice(soup):
    try:
        t = soup.select_one('body > div > div:nth-child(6) > div.col-md-12.col-lg-5.col-xl-4.ph-pricing.mt-2.mb-2.border.shadow-sm.p-2.bg-light > div.ph-pricing-mrp')
        prodDetail['Label Price'] = t.text
    except:
        prodDetail['Label Price'] = " "

def getDiscount(soup):
    try:
        t = soup.select_one('body > div > div:nth-child(6) > div.col-md-12.col-lg-5.col-xl-4.ph-pricing.mt-2.mb-2.border.shadow-sm.p-2.bg-light > div.ph-pricing-discount')
        prodDetail['Discount'] = t.text.strip()
    except:
        prodDetail['Discount'] = " "

def getSuggestion(soup):
    try:
        t = soup.select_one('#pricing-assessment > div > div > div.col-12.col-sm-12.col-md-6.m-0 > p')
        prodDetail['Suggestion'] = t.text.strip()
    except:
        prodDetail['Suggestion'] = " "

def getStatus(soup):
    try:
        t = soup.select_one('#fix-bottom > div > div > div > div.col-3.p-0.rounded.text-light > a')
        prodDetail['Status'] = t.text 
    except:
        prodDetail['Status'] = " "

def ext(prodUrl):
    try:
        html = getSauce(prodUrl)
        if html == 0:
            print("Unable to retrieve info")
            return 0
        else:
            soup = BeautifulSoup(html, 'html.parser')
            getTitle(soup)
            getLowPrice(soup)
            getLowPriceDate(soup)
            getHighPrice(soup)
            getHighPriceDate(soup)
            getAvgPrice(soup)
            getAvgPriceDate(soup)
            getCurrentPrice(soup)
            getLabelPrice(soup)
            getDiscount(soup)
            getStatus(soup)
            getSuggestion(soup)
            if prodDetail['Current Price'] != " " and prodDetail['Label Price'] != " ":
                t1 = prodDetail['Current Price'].replace("₹","")
                t1 = t1.replace(",","")
                t2 = prodDetail['Label Price'].replace("₹","")
                t2 = t2.replace(",","")
                prodDetail['Savings'] = int(t2) - int(t1)
                prodDetail['Savings'] = "₹" + str(prodDetail['Savings'])
            else:
                prodDetail['Savings'] = " "
            return prodDetail
    except:
        raise RuntimeError('Unable to get info (General)')
    
#di = ext("https://www.amazon.in/Godrej-Convertible-Split-AC-12TINV3R32-GWA/dp/B0BN37ZCF7/ref=sr_1_1_sspa?_encoding=UTF8&content-id=amzn1.sym.58c90a12-100b-4a2f-8e15-7c06f1abe2be&dib=eyJ2IjoiMSJ9.LpujZ4uISPUK8sa_6yNGVaJ6gZ1SvJMqMGwoZI950ZumxSLryiO68ly2lNtjsEb1U80Wn8Xhe33o4hK4pCTyyBhL8ne8M9UXIluv2LUxkGvqAbW9MgYkVpvDw4vooMxRTYsy_KXPAaEkmt5u8sZF0yQFscrCJ0ejsc1wzwQB1ZyAASrLLxJDK1kDPpDdtI7_lFn_SFV2kiAtumeiOuk9Tc0zlGEzOaQJOPcMJCt0vTwrHq72MToJ1uU4FZFkqhdY9gXMU-I9l8d4qIFFJNjJTEwgsBhzO4o4ghxLWujsEmg.fHCIcJ7Ojj7HZNzWq2_RzGgOFqKo4jRkxQlGJnRyCu4&dib_tag=se&pd_rd_r=7090cfc8-3768-4ef4-a5a9-1ea7bb92d35b&pd_rd_w=1WmFB&pd_rd_wg=xPWBn&pf_rd_p=58c90a12-100b-4a2f-8e15-7c06f1abe2be&pf_rd_r=KFZ13V5H5K4JFJ0RG5Z6&qid=1712186662&refinements=p_85%3A10440599031&rps=1&s=kitchen&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGZfYnJvd3Nl&th=1")
#di = ext("https://www.amazon.in/Neemans-Casual-Trainers-Comfortable-Lightweight/dp/B0BY6GCZVS/ref=lp_1983518031_1_1_sspa?keywords=Men%27s+Shoes&pf_rd_p=9e034799-55e2-4ab2-b0d0-eb42f95b2d05&pf_rd_r=8K2BSATTTRS47BM0B8EB&sp_csd=d2lkZ2V0TmFtZT1zcF9hcGJfZGVza3RvcF9icm93c2VfaW5saW5lX2F0Zg&psc=1")
#print(di)

"""
prodDetail['Title'] = soup.select_one('body > div > div:nth-child(6) > div.col-md-12.col-lg-7.col-xl-8 > div > div.col-lg-9.col-md-9.col-sm-8.col-8.ph-title.my-0.pl-2.p-1 > h1').text
            prodDetail['Highest Price'] = soup.select_one('body > div.container.main-container.pt-2 > div:nth-child(6) > div.col-12.px-0.py-2.all-time-price-overview.small > div > div.col.bg-danger.text-light > span.amount').text.strip()
            prodDetail['Date of highest price'] = soup.select_one('body > div.container.main-container.pt-2 > div:nth-child(6) > div:nth-child(9) > table > tbody > tr:nth-child(6) > td').text
            prodDetail['Average Price'] = soup.select_one('body > div.container.main-container.pt-2 > div:nth-child(6) > div.col-12.px-0.py-2.all-time-price-overview.small > div > div.col.bg-warning.text-dark > span.amount').text.strip()
            prodDetail['Average Price as of'] = soup.select_one('body > div.container.main-container.pt-2 > div:nth-child(6) > div:nth-child(9) > table > tbody > tr:nth-child(4) > td').text
            prodDetail['Lowest Price'] = soup.select_one('body > div.container.main-container.pt-2 > div:nth-child(6) > div.col-12.px-0.py-2.all-time-price-overview.small > div > div.col.bg-info.text-light > span.amount').text.strip()
            prodDetail['Date of lowest price'] = soup.select_one('body > div.container.main-container.pt-2 > div:nth-child(6) > div:nth-child(9) > table > tbody > tr:nth-child(2) > td').text
            prodDetail['Current Price'] = soup.select_one('#price-table > div > table > tbody > tr:nth-child(1) > td').text.strip()
            prodDetail['Market Rate'] = soup.select_one('#price-table > div > table > tbody > tr:nth-child(2) > td').text.strip()
            prodDetail['Savings'] = soup.select_one('#price-table > div > table > tbody > tr:nth-child(3) > td').text.strip()
            prodDetail['Discount'] = soup.select_one("#price-table > div > table > tbody > tr:nth-child(4) > td").text
            prodDetail['Suggestion'] = soup.select_one('#pricing-assessment > div > div > div.col-12.col-sm-12.col-md-6.m-0 > p').text
            desc = soup.select_one("#product-details")
            ul_tag = desc.find('ul', class_='pl-4')
            # Initialize an empty list to store the text content of each <li> tag
            list_items = []
            # Loop through each <li> tag within the <ul> tag and extract the text content
            for li_tag in ul_tag.find_all('li'):
                list_items.append(li_tag.get_text(strip=True))
            prodDetail['Description'] = list_items
            detail = soup.select_one("#product-info")

            tbody_tag = detail.find('tbody')
            
            # Initialize an empty list to store the pairs of text content
            pairs = []

            # Loop through each <tr> tag within the <tbody> tag
            for tr_tag in tbody_tag.find_all('tr'):
                # Find the <th> and <td> tags within the <tr> tag
                th_tag = tr_tag.find('th')
                td_tag = tr_tag.find('td')
                
                # Extract the text content of <th> and <td> tags
                th_text = th_tag.get_text(strip=True) if th_tag else ''
                td_text = td_tag.get_text(strip=True) if td_tag else ''
                
                # Append the pair to the list
                pairs.append((th_text, td_text))

            prodDetail['Detail'] = pairs
            prodDetail['Status'] = soup.select_one('#fix-bottom > div > div > div > div.col-3.p-0.rounded.text-light > a').text
"""