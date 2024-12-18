from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from collections import OrderedDict
import time
import pandas as pd
import json
from SQL_data import conn

#이벤트
def Event(xpath, data):
    # 스크롤 맨위로
    driver.execute_script("document.body.scrollHeight")
    element = driver.find_element(By.XPATH, xpath)
    driver.execute_script("arguments[0].click();", element)
    
    # 덤증정 페이지 클래스 이름 통일 제한으로 인해 함수 2개로 분리
    if xpath == '//*[@id="section"]/div[3]/ul/li[4]/a':
        search_add()
    else:
        search()
    
    getdata(data)
    
# 덤증정 이벤트 더보기
def search_add():
    while(True):
        item = driver.find_elements(By.CSS_SELECTOR, "div.event_add_list > ul > li")
        
        driver.find_element(By.CLASS_NAME, 'pr_more').click()
        time.sleep(1)
        last_item =  driver.find_elements(By.CSS_SELECTOR, "div.event_add_list > ul > li")
        
        if item[-1].text == last_item[-1].text:
            break

# 더보기 클릭
def search():
    while(True):
        # 클릭 전 마지막 추출
        item = driver.find_elements(By.CSS_SELECTOR, "div.event_plus_list > ul > li")
        # 더보기 클릭
        driver.find_element(By.CLASS_NAME, 'pr_more').click()
        time.sleep(1)
        # 클릭 후 마지막 추출
        last_item =  driver.find_elements(By.CSS_SELECTOR, "div.event_plus_list > ul > li")
        
        # 마지막 요소 끼리 비교 후 종료
        if item[-1].text == last_item[-1].text:
            break

# DATAFrame으로 만들기
def getdata(data):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # dic 변환용 배열 
    event_list = OrderedDict()

    event_tab_list = []
    event_name_list = []
    event_price_list = []
    event_img_list = []
    
    # 요소 추출
    prod_tab_List = soup.select("div.event_plus_list > ul > li > a > span")
    prod_name_List = soup.select("div.event_plus_list > ul > li > a > img")
    prod_price_List = soup.select("div.event_plus_list > ul > li > a > p > strong")
    prod_img_List = soup.select("div.event_plus_list > ul > li > a > img")

    LENGTH = min(len(prod_img_List), len(prod_name_List), len(prod_price_List))

    # 배열에 추가 
    for i in range(LENGTH):
        event_tab_list.append(prod_tab_List[i].text)
        event_img_list.append(prod_img_List[i]['src'])
        event_name_list.append(prod_name_List[i]['alt'])
        event_price_list.append(prod_price_List[i].text)
        
    # Dic에 저장
    data["event"] = event_tab_list
    data["name"] = event_name_list
    data["price"] = event_price_list
    data["img"] = event_img_list
    
    # DataFrame 으로 변환
    df = pd.DataFrame(data)
    
    # 중복 제거
    df = df.drop_duplicates(['name'])
    
    # DB에 넣기
    input_DB(df)
    
# DB 삽입
def input_DB(df):
    # DB에 넣기
    for idx, row in df.iterrows(): 
        val = (row[0], row[1], row[2], row[3], row[4])
        cur.execute('INSERT INTO MINISTOP (brand, event, name, price, img) VALUES (%s, %s, %s, %s, %s)',val)
        conn.commit()
        
#실행 함수
def Ministop_event():
    #사이트 이동
    url='https://www.ministop.co.kr/MiniStopHomePage/page/event/plus1.do'
    driver.get(url)    
    time.sleep(2)

    # 이벤트 배열
    event = []
    # DataFrame 변환용 dic
    data = {
        "brand" : "MINISTOP"
    }
    xpath_tap = [
        '//*[@id="section"]/div[3]/ul/li[1]/a',
        '//*[@id="section"]/div[3]/ul/li[2]/a',
        '//*[@id="section"]/div[3]/ul/li[3]/a',
        '//*[@id="section"]/div[3]/ul/li[4]/a',
        '//*[@id="section"]/div[3]/ul/li[5]/a'
    ]
    
        
    Len = len(xpath_tap)
    
    # Tap 수만큼 함수 실행
    for i in range(Len):
        Event(xpath_tap[i],data)
        

        
s = Service('/Users/gimmingi/Desktop/web/chromedriver')
driver = webdriver.Chrome(service=s)


cur = conn.cursor()



Ministop_event()

cur.close()
driver.close()