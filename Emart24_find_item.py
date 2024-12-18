from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import pandas as pd
import json
from SQL_data import conn
import re

def getdata(event_lable_list, event_name_list, event_price_list, event_img_list, event):
    # 페이지 읽기
    html_page = driver.page_source
    soup_page = BeautifulSoup(html_page, 'html.parser')
    
    # 요소 읽기 
    prod_name_List = soup_page.select("p.productDiv")
    prod_price_List = soup_page.select("p.price") 
    prod_img_List = soup_page.select("div.box > p.productImg > img")

    LENGTH = min(len(prod_img_List), len(prod_name_List), len(prod_price_List))
    
    if event == "SALE":
        for i in range(LENGTH):
            event_lable_list.append(event)
            event_img_list.append(prod_img_List[i]['src'])
            event_name_list.append(prod_name_List[i].text)
            text = prod_price_List[i].text
            index = text.find("→")
            event_price_list.append(text[index + 2:])
    else: 
        for i in range(LENGTH):
            event_lable_list.append(event)
            event_img_list.append(prod_img_List[i]['src'])
            event_name_list.append(prod_name_List[i].text)
            event_price_list.append(prod_price_List[i].text)
 
# 다음 페이지 누르기
def next_page(event_lable_list, event_name_list, event_price_list, event_img_list, event, xpath):
    
    # tap 누르기
    driver.find_element(By.XPATH,xpath).click()
    
    # 페이지 요소 읽기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    # 현재 창에 나와있는 페이지들
    totalpage = soup.select(".paging > a") 

    # 마지막 페이지 찾기 
    lastpage = int(re.sub(r'[^0-9]', '',totalpage[-1]["href"]))
    
    
    # 마지막 페이지 수만큼 다음 클릭하면서 데이터 읽어오기
    for i in range(lastpage):
        getdata(event_lable_list, event_name_list, event_price_list, event_img_list, event)
        driver.find_element(By.CLASS_NAME, 'next.bgNone').click()
    #스크롤 맨위로
    driver.execute_script("window.scrollTo(0, 0)")
    
def input_DB(df):
    # DB에 넣기
    for idx, row in df.iterrows(): 
        val = (row[0], row[1], row[2], row[3], row[4])
        cur.execute('INSERT INTO EMART24 (brand, event, name, price, img) VALUES (%s, %s, %s, %s, %s)',val)
        conn.commit()
    
# 이마트 열기
def Emart24_event():
    
    # Emart24 창 열기
    url='https://emart24.co.kr/product/eventProduct.asp'
    driver.get(url)
    time.sleep(2)
    
    
    # 배열 생성
    event_lable_list = []
    event_name_list = []
    event_price_list = []
    event_img_list = []
    event = []
    
    # 데이터 프레임으로 전환할 딕션어리 생성
    data = {
        "brand" : "EMART24"
    }
    
    # tap 이름
    xpath = driver.find_element(By.CLASS_NAME,"tab01")
    xpaths = xpath.find_elements(By.CSS_SELECTOR, "a")
    for i in xpaths[1:]:
        TEXT = i.text
        event.append(TEXT.replace(" ",""))
    
    # tap 들
    xpath_tap = [
        '//*[@id="tabNew"]/ul/li[2]/h4/a',
        '//*[@id="tabNew"]/ul/li[3]/h4/a',
        '//*[@id="tabNew"]/ul/li[4]/h4/a',
        '//*[@id="tabNew"]/ul/li[5]/h4/a',
        '//*[@id="tabNew"]/ul/li[6]/h4/a',
        '//*[@id="tabNew"]/ul/li[7]/h4/a'
    ]
    
    LEN = min(len(event), len(xpath_tap))
    # tap 이동
    for i in range(LEN):
        next_page(event_lable_list,event_name_list, event_price_list, event_img_list, event[i], xpath_tap[i])
        
    
    # 딕션어리 추가
    data["event"] = event_lable_list
    data["name"] = event_name_list
    data["price"] = event_price_list
    data["img"] = event_img_list
    
    # 변환
    df = pd.DataFrame(data)
    
    #중복 제거
    df = df.drop_duplicates(['name'])
    
    input_DB(df)

# 크롬 드라이버 실행 
s = Service('/Users/gimmingi/Desktop/web/chromedriver')
driver = webdriver.Chrome(service=s)


cur = conn.cursor()
# 실행
Emart24_event()

cur.close()
driver.close()