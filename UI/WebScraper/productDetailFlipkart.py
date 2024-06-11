import requests
from bs4 import BeautifulSoup
from .maxFile import get_max_numbered_jpg

prodDetail = {}

def getTitle(soup):
    try:
        t = soup.find('span',{'class': 'VU-ZEz'})
        prodDetail['Title'] = t.text
    except:
        prodDetail['Title'] = " "

def getCurrentPrice(soup):
    try:
        t = soup.find('div',{'class': 'Nx9bqj CxhGGd'})
        prodDetail['Current Price'] = t.text
    except:
        prodDetail['Current Price'] = " "
    
def getInfo(soup):
    try:
        t = soup.find_all('li',{'class': '_7eSDEz'})
        t_ = []
        for i in t:
            t_.append(i.text)
        prodDetail['About'] = t_
    except:
        prodDetail['About'] = " "

def getImage(soup):
    try:
        image_tag = soup.find("div",{"class":"_4WELSP _6lpKCl"})
        image_tag = soup.find_all('img')
        image_url = image_tag[2]['src']
        dir = "C:\\Users\\ramee\\Desktop\\AI Lab\\Project\\Image"
        img_name = int(get_max_numbered_jpg(dir).replace(".jpg", ""))
        img_name += 1
        img_name = str(img_name)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': '*/*'
        }
        response = requests.get(image_url, headers=headers)
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

def get_html(productUrl):
    try:
        resp = requests.get(productUrl)
        html_content = resp.content
        return html_content
    except:
        return None
    
def get_data(productUrl):
    try:
        html = get_html(productUrl)
        soup = BeautifulSoup(html, 'html.parser')
        getTitle(soup)
        getCurrentPrice(soup)
        getInfo(soup)
        getImage(soup)
    except:
        raise RuntimeError("Unable to get data")

def ext(prod):
    try:
        get_data(prod)
        return prodDetail
    except:
        raise RuntimeError("Unable to get product info (Flipkart)")

# test run
#print(ext("https://www.flipkart.com/philips-gc1903-1300-w-steam-iron/p/itma2af216e592da?pid=IRND2UFFYBMGSPUN&lid=LSTIRND2UFFYBMGSPUNG4PV8Q&marketplace=FLIPKART&store=j9e%2Fabm%2Fa0u&srno=b_1_2&otracker=nmenu_sub_Appliances_0_Irons&fm=organic&iid=ffd3abce-9258-4262-926f-c8737df61ddc.IRND2UFFYBMGSPUN.SEARCH&ppt=browse&ppn=browse&ssid=afxrdhlakg0000001714546159013"))



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