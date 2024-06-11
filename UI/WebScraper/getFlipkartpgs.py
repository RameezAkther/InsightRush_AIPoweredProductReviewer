import requests
from bs4 import BeautifulSoup
import re

def totalReviews(productUrl):
    try:
        productUrl = productUrl.replace("/p/", "/product-reviews/")
        resp = requests.get(productUrl)
        soup = BeautifulSoup(resp.text, 'html.parser')
        reviews_span = soup.find('span',{'class': 'Wphh3N'})
        if reviews_span:
            no = reviews_span.text
            no = no.replace(",","")
            numbers = re.search(r'(\d+)\s+Reviews', no).group(1)
            if numbers:
                if int(numbers) >= 300:
                    return 300
                else:
                    return int(numbers)
        return 0
    except:
        raise RuntimeError("Unable to get review count")
    
#print(totalReviews("https://www.flipkart.com/hisense-e7k-126-cm-50-inch-qled-ultra-hd-4k-smart-vidaa-tv-dolby-vision-atmos/p/itm62fd1e22110c2?pid=TVSGSZGZY6QMR5JH&lid=LSTTVSGSZGZY6QMR5JH1AIHVY&marketplace=FLIPKART&store=ckf%2Fczl&srno=b_1_1&otracker=browse&fm=organic&iid=en_YqA2-K3dy-kt1A1AkUEXy3XC2wgOX4KCXXCuvYsRRy4CsphHTMT0hzWNPP8aqMncKhOVm2IPio8jXkH2OqIqOPUFjCTyOHoHZs-Z5_PS_w0%3D&ppt=pp&ppn=pp&ssid=3kppifnzr40000001714544768493"))