def crawl_ViettelStore():
    import time
    import csv
    import pandas as pd

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.webdriver.common.by import By
    from datetime import date
    from pymongo import MongoClient


    options = Options()
    options.headless = True
    driver = webdriver.Chrome(executable_path='D:/workspace/drivers/chromedriver.exe', chrome_options=options)


    LOGIN_URL = 'https://viettelstore.vn/dien-thoai'
    # driver.get(LOGIN_URL)
    driver.get(LOGIN_URL)


    ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
    time.sleep(5)


    def show_more_product(driver):
        more_product_id = 'div_Danh_Sach_San_Pham_loadMore_btn'
        try:
            driver.find_element(By.ID, more_product_id).find_element(By.TAG_NAME, 'a').click()
        except:
            pass
        try:
            driver.find_element(By.ID, more_product_id).find_element(By.TAG_NAME, 'a').click()
        except:
            pass


    def get_product_link(driver):
        links = []
        link_CN ='item.ProductList3Col_item'
        number_product = len(driver.find_elements(By.CLASS_NAME,link_CN))
        for i in range(number_product):
            link = driver.find_elements(By.CLASS_NAME,link_CN)[i].find_element(By.TAG_NAME,'a').get_attribute('href')
            links.append(link)
        return links


    def get_detals(driver):
        name_xpath = '/html/body/div[3]/div[1]/div/div[1]/ul/li[2]/div/div/div[1]/div[1]/h1'
        new_price = '/html/body/div[3]/div[1]/div/div[1]/ul/li[2]/div/div/div[1]/div[1]/div[1]/span[1]'

        name = ''
        kich_thuoc_man_hinh = ''
        cong_nghe_man_hinh = ''
        camera_sau = ''
        camera_truoc = ''
        loai_sim = ''
        bo_nho_trong = ''
        pin = ''
        ram = ''
        chip_set = ''
        bluetooth = ''


        try:
            name = driver.find_element(By.XPATH, name_xpath).text
        except:
            pass
        try:
            new_price = driver.find_element(By.XPATH, new_price).text
        except:
            pass
        driver.execute_script("window.scrollTo(0, 3000)")
        table = driver.find_elements(By.CLASS_NAME, 'digital ')[0].find_element(By.TAG_NAME,'table')
        trs   = table.find_elements(By.TAG_NAME, 'tr')
        for tr in trs:
            th=''
            td=''

            try:
                th = tr.find_elements(By.TAG_NAME, 'td')[0].text
                td = tr.find_elements(By.TAG_NAME, 'td')[1].text
            except:
                x=0
            hdh =''
            if th == 'Hệ điều hành:':
                hdh = td
            if th == 'CPU:':
                chip_set = td
            if th == 'Màn hình:':
                cong_nghe_man_hinh = td
            if th =='Camera sau:':
                camera_sau=td
            if th =='Camera trước:':
                camera_truoc = td
            if th == 'Hỗ trợ đa sim:':
                loai_sim = td

            if th == 'Dung lượng pin':
                pin = td

            if th == 'RAM:':
                ram = td

            if th == 'Độ phân giải':
                do_phan_giai = td

            if th == 'Bộ nhớ trong:':
                bo_nho_trong = td

            if th == 'Pin:':
                pin = td
        with open('viettel_store.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([name, new_price, cong_nghe_man_hinh, camera_sau, camera_truoc, chip_set, ram, bo_nho_trong,
                             pin, loai_sim, hdh])

    for i in range(10):
        try:
            show_more_product(driver)
            time.sleep(2)
        except:
            pass

    links = get_product_link(driver)

    for link in links:
        try:
            driver.get(link)
        except:
            x=0
        try:
            get_detals(driver)
        except:
            pass

    driver.close()

    data = pd.read_csv("viettel_store.csv", header=None)
    data["date"] = [str(date.today())]*data.shape[0]
    data.reset_index(inplace=True)
    data_dict = data.to_dict('records')

    client = MongoClient("mongodb+srv://longgiang:longgiang2010@cluster0.npw0zsg.mongodb.net/")
    db = client["data-integration"]
    collec = db["thegioididong"]

    collec.insert_many(data_dict)
