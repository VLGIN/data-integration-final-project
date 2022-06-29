def crawl_mediaMart():
  import requests
  from bs4 import BeautifulSoup
  import json
  import pandas as pd
  import time
  import os

  def crawl_item(url_input):
    try:
      url = 'https://mediamart.vn' + url_input
      headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
        'X-Requested-With': 'XMLHttpRequest',
      }    
      r = requests.get(url, headers=headers)
      data = {}
      soup = BeautifulSoup(r.content.decode('utf-8', 'ignore'), 'html.parser')
      data["name"] = soup.find_all("div", class_="pdetail-name")[0].text.split('\n')[1]
      x=0
      key=''
      for tr in soup.find_all('td'):
        if(len(tr.get_text()) > 0):
          if(x%2)==0:
            key=tr.get_text()
          else:
            data[key]=tr.get_text()
          x=x+1
      data["price"] = soup.find("div", class_="pdetail-price-box").text
      time.sleep(10)
      return data
    except:
      pass
  data=[]
  # if os.path.exists('/opt/airflow/dags/mediamart.csv'):
  #   df = pd.read_csv('mediamart.csv') #duong dan file csv
  # else:
  #   df = None
  url = 'https://mediamart.vn/smartphones'
  headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'X-Requested-With': 'XMLHttpRequest',
  }    
  r = requests.get(url, headers=headers)
  soup = BeautifulSoup(r.content, 'html.parser')
  for div in soup.find_all("div", class_="col-6 col-md-3 col-lg-3"):
    data.append(crawl_item(div.find("a", href=True)['href']))
  # if df == None:
  #   df = pd.DataFrame(data)
  # else:
  #   df = pd.concat([pd.DataFrame(data), df], ignore_index=True)
  df = pd.DataFrame(data)
  df.to_csv('/opt/airflow/dags/mediamart.csv')
  print("Save to file")
