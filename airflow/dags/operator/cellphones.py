from bs4 import BeautifulSoup
import requests
import json, time
import pandas as pd

from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


def get_item_cellphones(r):
    with open('cellphones.json', 'a') as f:
        soup = BeautifulSoup(r, 'html.parser')
        product_tab = soup.find('div', class_ = 'block-products san-pham-cate').find('div', class_ = 'list-product')
        products = product_tab.find_all('div', class_ = 'item-product')

        for product in products:
            name = product.find('div', class_ = 'item-product__box-name').find('h3').text
            price = product.find('div', class_ = 'item-product__box-price').find('p', class_ = 'special-price').text
            image = product.find('div', class_ = 'item-product__box-img').find('img')['data-src']
            item = {
                'name' : name,
                'price' : price,
                'image' : image,
            }
            json.dump(item, f)
            f.write('\n')


def crawl_cellphones():
    driver_path = 'D:\workspace\drivers\chromedriver.exe'
    chromeOptions = Options()
    chromeOptions.add_argument("start-maximized")
    chromeOptions.headless = False

    driver = webdriver.Chrome(executable_path=driver_path,
                            chrome_options=chromeOptions)


    url = 'https://cellphones.com.vn/mobile.html'    
    driver.get(url)
    time.sleep(2)

    done = False
    while not done:
        try:
            element = driver.find_element(by=By.CSS_SELECTOR, value='a.btn-show-more.btn-load-more.cta-xem-san-pham')
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            r = driver.page_source
            get_item_cellphones(r)
            element.click()
            time.sleep(5)
        except:
            done = True

    r = driver.page_source
    driver.__exit__()
    get_item_cellphones(r)
    df = pd.read_json('cellphones.json', lines = True).drop_duplicates()
    df.to_csv('cellphones.csv')