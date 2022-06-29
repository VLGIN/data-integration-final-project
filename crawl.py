from typing import Text
import requests
from bs4 import BeautifulSoup
import lxml
import json
import csv
import pandas as pd

def crawl():
  data_phones = []

  Devices=["apple-iphone","samsung","oppo","xiaomi","vivo","realme","nokia","itel","masstel"]
  ID=1
  for i in range(len(Devices)):
    URL = 'https://www.thegioididong.com/dtdd-'+Devices[i]
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    webpage = requests.get(URL,headers=headers).text
    A=[]
    soup = BeautifulSoup(webpage, 'html.parser')
    data = soup.find('ul', {"class":"listproduct"})
    for a in data.find_all('a',href=True):
      try:
        new_str=a['href']
        new_str=new_str.replace("javascript:void(0)","")
        new_str=new_str.replace("#","")
        if new_str=="":
          continue
        if new_str=="/dtdd/poco-c40?src=osp":   #Mẫu điện thoại đang quảng cáo
          continue
        URL = "https://www.thegioididong.com" + new_str
        headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
        webpage = requests.get(URL,headers=headers).text

        soup = BeautifulSoup(webpage, 'html.parser')
        data = json.loads(soup.find('script', id="productld").get_text()).get("additionalProperty")
        name = json.loads(soup.find('script', id="productld").get_text()).get('name')

        data1=json.loads(soup.find('script', id="productld").text).get("offers").get('price')
        data2=json.loads(soup.find('script', id="productld").text).get("offers").get('priceValidUntil')
        print('ID = ',ID)
        print(name)
        ID=ID+1
        print('Price :',data1)
        print('priceValidUntil :',data2)
        
        item = {}
        item['Name'] = name
        item['Price'] = data1
        item['priceValidUntil']=data2

        for entry in data:
            print(entry['name'],':',entry['value'])   
            item[entry['name']] = entry['value']

        data_phones.append(item)
      except:
        pass
  df = pd.DataFrame.from_dict(data_phones)
  df.to_csv("data_phones.csv", encoding="utf-8") 

    