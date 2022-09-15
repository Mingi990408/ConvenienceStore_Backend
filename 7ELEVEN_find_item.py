from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import pandas as pd
import json
from SQL_data import conn

#이벤트
def Event(url, event, data):
    data["event"] = event
    driver.execute_script("document.body.scrollHeight")
    element = driver.find_element(By.XPATH, url)
    driver.execute_script("arguments[0].click();", element)
    
    search()
    
    getdata(event, data)
    

# 더보기 클릭
def search():
    while(True):
        try:
            driver.find_element(By.CLASS_NAME, 'btn_more').click()
            time.sleep(2)
        except NoSuchElementException:
            break

# DATAFrame으로 만들기
def getdata(event, data):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    event_list = OrderedDict()

    event_name_list = []
    event_price_list = []
    event_img_list = []
    prod_name_List = soup.select(".name")
    prod_price_List = soup.select(".price > span")
    prod_img_List = soup.select("div.pic_product > img")

    LENGTH = min(len(prod_img_List), len(prod_name_List), len(prod_price_List))

    for i in range(LENGTH):
        event_img_list.append(prod_img_List[i]['src'])
        event_name_list.append(prod_name_List[i].text)
        event_price_list.append(prod_price_List[i].text)
        
    data["name"] = event_name_list
    data["price"] = event_price_list
    data["img"] = event_img_list
    df = pd.DataFrame(data)
    df = df.drop_duplicates(['name'])
    
    # DB에 넣기
    for idx, row in df.iterrows(): 
        val = (row[0], row[1], row[2], row[3], row[4])
        cur.execute('INSERT INTO SEVENELEVEN (brand, event, name, price, img) VALUES (%s, %s, %s, %s, %s)',val)
        conn.commit()
        
#실행 함수
def Eleven_event():
    url='https://www.7-eleven.co.kr/product/presentList.asp'
    driver.get(url)
    time.sleep(2)
    data = {
        "brand" : "7ELEVEN"
    }
    xpath = [
        '//*[@id="actFrm"]/div[3]/div[1]/ul/li[1]/a',
        '//*[@id="actFrm"]/div[3]/div[1]/ul/li[2]/a',
        '//*[@id="actFrm"]/div[3]/div[1]/ul/li[3]/a',
        '//*[@id="actFrm"]/div[3]/div[1]/ul/li[4]/a'
    ]
    event = [
        "1+1",
        "2+1",
        "증정행사",
        "할인행사"
    ]
    Len = len(event)
    for i in range(Len):
        Event(xpath[i] ,event[i], data)
        

        
s = Service('/Users/gimmingi/Desktop/web/chromedriver')
driver = webdriver.Chrome(service=s)

# SQL 
cur = conn.cursor()



Eleven_event()

cur.close()
driver.close()