#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import time
import re
import argparse

from bs4 import BeautifulSoup
from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, ElementClickInterceptedException


# In[ ]:


parser = argparse.ArgumentParser() 
  
# Adding optional argument 
parser.add_argument("-m", "--mode", help = "Specifying the mode, search or shop") 
parser.add_argument("-u", "--url", help = "URL that you will crawl") 
parser.add_argument("-t", "--total_page", help = "The total page that you will crawl (only work if you on search mode)") 
parser.add_argument("-o", "--output", help = "Output filename") 
  
# Read arguments from command line 
args = parser.parse_args() 
  
if args.mode == None:
    print('You must specify the mode')
    exit()
    
if args.url == None:
    print('You must specify the url')
    exit()
    
if args.mode == "search":
    if args.total_page == None:
        print('You must specify the total_page')
        exit()
    
if args.output == None:
    print('You must specify the output filename')
    exit()


# In[ ]:


mode = args.mode
url = args.url
total_page = 1 if(mode == "shop") else int(args.total_page)


# In[ ]:


chrome_options = webdriver.ChromeOptions()  
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36")
chrome_options.add_argument("--start-maximized");
chrome_options.add_argument("window-size=1366x768");
chrome_options.add_argument("user-data-dir={}".format("open-maps-user-dir"))
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu"), 
chrome_options.add_argument('disable-infobars')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")


# In[ ]:


driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
driver.maximize_window()
wait = WebDriverWait(driver, 2)


# In[ ]:


wait = WebDriverWait(driver, 60)


# In[ ]:


url_per_lapak = []


# In[ ]:


def scroll_down(driver):
    # scroll to down (looping until nothing loaded anymore)
    SCROLL_PAUSE_TIME = 0.5
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# In[ ]:


print("Visiting {}".format(url))
print("Please wait...")

for i in range(0, total_page):
    if mode == "search":
        driver.get(url + "&page={}".format(i))
    else:
        driver.get(url + "?perpage=9999")
    
    scroll_down(driver)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    container_info = soup.find_all(attrs={"class": "css-89jnbj"})
    
    if len(container_info) == 0:
        print("Crawling error")
        exit()
    
    for i in container_info:
        url_per_lapak.append(i["href"])

print("Gathering the lists of product...")


# In[ ]:


print("Prepare to crawl the products...")

clean_data = []

for i in url_per_lapak:
    try:
        driver.get(i)
    
        scroll_down(driver)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        title = soup.find(attrs={"data-testid": "lblPDPDetailProductName"}).text
        price = soup.find(attrs={"data-testid": "lblPDPDetailProductPrice"}).text.replace("Rp", "").replace(".", "")
        
        rating = soup.find(attrs={"data-testid": "lblPDPDetailProductRatingNumber"})
        rating = None if(rating == None) else rating.text
        
        total_reviewer = soup.find(attrs={"data-testid": "lblPDPDetailProductRatingCounter"})
        total_reviewer = None if(total_reviewer == None) else total_reviewer.text.replace(")", "").replace("(", "")
        
        total_sold = soup.find(attrs={"data-testid": "lblPDPDetailProductSuccessRate"})
        total_sold = None if(total_sold == None) else total_sold.text.split(" ")[1]
        
        seen_counter = soup.find(attrs={"data-testid": "lblPDPDetailProductSeenCounter"}).find("b").text.replace("x", "")
        weight = re.split('(\d+)', soup.find(attrs={"data-testid": "PDPDetailWeightValue"}).text)[1]
        weight_unit = re.split('(\d+)', soup.find(attrs={"data-testid": "PDPDetailWeightValue"}).text)[2]
        shop_name = soup.find(attrs={"data-testid": "llbPDPFooterShopName"}).text
        shop_region = soup.find(attrs={"data-testid": "lblPDPFooterLastOnline"}).text.split("•")[0]
        
        shop_badge = soup.find(attrs={"data-testid": "imgPDPDetailShopBadge"})
        is_power_merchant = False
        if shop_badge != None:
            if shop_badge.text == "Power Merchant":
                is_power_merchant = True

        clean_data.append({
            "title": title,
            "rating": rating,
            "price": price,
            "total_reviewer": total_reviewer,
            "total_sold": total_sold,
            "seen_counter": seen_counter,
            "weight": weight,
            "weight_unit": weight_unit,
            "shop_name": shop_name,
            "shop_region": shop_region,
            "is_power_merchant": is_power_merchant,
        })
        
        print("[{} of {}] {}".format(len(clean_data), len(url_per_lapak), title), end="\n")
        
    except TimeoutException as e:
        print("Error: " + str(e))
        pass


# In[ ]:


df = pd.DataFrame(clean_data)


# In[ ]:


df.to_csv("{}.csv".format(args.output), index=False)
print("Data have been successfully exported to {}.csv".format(args.output))

