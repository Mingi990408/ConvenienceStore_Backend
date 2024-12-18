from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from collections import OrderedDict
import time
import pandas as pd
from mysql import Product

# 웹 크롤링하는 함수 
# 예시) 1+1을 누르고 더보기가 뜨지 않을 때까지 더보기를 계속 누름
# 모든 상품이 페이지에 나타난 후 요소들을 prod_xxx에 저장 
# 요소에서 필요한 데이터를 리스트에 저장 
# 순서를 유지하기 위해 OrderedDict을 이용해 DataFrame을 생성 후 DB에 저장 
def crawling(brand, url, event_xpath, next_xpath, css_selector):

    driver = webdriver.Chrome('/Users/kimseong-eun/webCrawling/chromedriver')
    
    # 페이지 열기
    print("getting url site")
    driver.get(url)

    # 상품명, 가격, 이미지 src, 행사목록 리스트 
    name = []
    price= []
    img = []
    event = []

    print("parsing data")
    for i in range(len(event_xpath)):   # 행사목록의 개수만큼 반복문 실행 
        driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, event_xpath[i]))   # 행사목록 클릭 
        while True: 
            try: 
                time.sleep(2)
                driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, next_xpath))   # 더보기 클릭 
                time.sleep(1)               
            except NoSuchElementException:  # 더보기 요소를 찾을 수 없는 경우 무한루프 탈출 
                break 
        
        prod_img = driver.find_elements(By.CSS_SELECTOR, css_selector[0])        # 이미지 요소를 찾아 리스트 형태로 저장 
        prod_name = driver.find_elements(By.CSS_SELECTOR, css_selector[1])       # 상품명 요소를 찾아 리스트 형태로 저장 
        prod_price = driver.find_elements(By.CSS_SELECTOR, css_selector[2])      # 가격 요소를 찾아 리스트 형태로 저장 
        prod_event = driver.find_elements(By.CSS_SELECTOR, css_selector[3])      # 행사목록 요소를 찾아 리스트 형태로 저장 

        LENGTH = min(len(prod_img), len(prod_name), len(prod_price), len(prod_event))   # 요소의 최소 크기를 찾아 반복문 반복횟수 결정 
        
        for i in range(LENGTH):
            img.append(prod_img[i].get_attribute('src'))    # 요소에서 이미지 src를 가져와 추가
            name.append(prod_name[i].text)                  # 요소에서 텍스트(상품명)을 가져와 추가 
            price.append(prod_price[i].text)                # 요소에서 텍스트(가격)을 가져와 추가 
            event.append(prod_event[i].text)                # 요소에서 텍스트(행사목록)을 가져와 추가 
    
    print("processing data to DataFrame") 
    products = OrderedDict()    # 순서가 보장되는 Dict에 각 리스트를 삽입 
    products = {
            "brand" : brand,
            "event" : event,
            "name" : name,
            "price" : price, 
            "img" : img}
    
    prod_df = pd.DataFrame(products) # OrderedDict을 통해 DataFrame 생성 
    Product(df = prod_df).save()

def setting():
    brand = 'CU'
    url = 'http://cu.bgfretail.com/event/plus.do?category=event&depth2=1&sf=N'
    event_xpath = ['//*[@id="contents"]/div[1]/ul/li[2]/a',
             '//*[@id="contents"]/div[1]/ul/li[3]/a']
    next_xpath = '//*[@id="contents"]/div[2]/div/div/div[1]/a'
    css_selector = ['#contents > div.relCon > div > ul a > div.prod_wrap > div.prod_img > img',
                    '#contents > div.relCon > div > ul a > div.prod_wrap > div.prod_text > div.name',
                    '#contents > div.relCon > div > ul a > div.prod_wrap > div.prod_text > div.price > strong',
                    '#contents > div.relCon > div > ul a > div.badge > span']

    cu_df = crawling(brand, url, event_xpath, next_xpath, css_selector)

if __name__ == '__main__':
    setting()