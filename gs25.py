from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import time
from mysql import Product

driver = webdriver.Chrome('/Users/kimseong-eun/webCrawling/chromedriver')
url = 'http://gs25.gsretail.com/gscvs/ko/products/event-goods#;'

print("getting url site")
driver.get(url)

driver.find_element(By.XPATH, '//*[@id="TOTAL"]').click()
time.sleep(1)

num = 1
page = 1
while True:
    prod = []
    try: 
        prod.append(wait(driver, 15).until(EC.presence_of_element_located((By.XPATH,
         f'//*[@id="contents"]/div[2]/div[3]/div/div/div[4]/ul/li[{num}]/div/div/p/span'))).text)    # event
        prod.append(wait(driver, 15).until(EC.presence_of_element_located((By.XPATH,
         f'//*[@id="contents"]/div[2]/div[3]/div/div/div[4]/ul/li[{num}]/div/p[2]'))).text)          # name
        prod.append(wait(driver, 15).until(EC.presence_of_element_located((By.XPATH,
         f'//*[@id="contents"]/div[2]/div[3]/div/div/div[4]/ul/li[{num}]/div/p[3]/span'))).text)      # price
        try:
            prod.append(driver.find_element(By.XPATH, f'//*[@id="contents"]/div[2]/div[3]/div/div/div[4]/ul/li[{num}]/div/p[1]/img').get_attribute('src')) 
        except NoSuchElementException:
            print('NoSuchElementException')
            prod.append('NO_IMG')
            pass

        Product(event=prod[0], name=prod[1], price=prod[2], img=prod[3]).save()
        
        num += 1 
        if num == 9:
            num = 1
            driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH,'//*[@id="contents"]/div[2]/div[3]/div/div/div[1]/div/a[3]'))
            page += 1 
            time.sleep(2)

        if page > 151:
                break
    except TimeoutException:
        print('Parse END')
        break
    except StaleElementReferenceException:
        time.sleep(1) 