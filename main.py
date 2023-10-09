import json
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --크롬창을 숨기고 실행-- driver에 options를 추가해주면된다
# options = webdriver.ChromeOptions()
# options.add_argument('headless')

url = 'https://map.kakao.com/'
driver = webdriver.Chrome('./chromedriver')  # 드라이버 경로
# driver = webdriver.Chrome('./chromedriver',chrome_options=options) # 크롬창 숨기기

driver.get(url)
key_word = '스터디 카페'

def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, "Can't find CSS tag.")
        driver.quit()
    return wait

def place_list_print():
    time.sleep(0.2)
    
    place_list = driver.find_elements(By.CSS_SELECTOR, "#info\.search\.place\.list > li")
    names = driver.find_elements(By.CSS_SELECTOR, '#info\.search\.place\.list > li > div.head_item.clickArea > strong > a.link_name')
    addresses = driver.find_elements(By.CSS_SELECTOR, '#info\.search\.place\.list > li > div.info_item > div.addr > p:nth-child(1)')
    other_addresses = driver.find_elements(By.CSS_SELECTOR, '#info\.search\.place\.list > li > div.info_item > div.addr > p:nth-child(2)')
    
    for index in range(len(place_list)):
        print("인덱스 :", index)
        
        # 장소 이름
        place_name = names[index].text
        #names[index] => A Selenium WebElement Class. It has text attribute that makes data to text type.
        print(place_name)
        
        # 장소 도로명 주소
        place_address = addresses[index].text
        print(place_address)
        
        # 장소 지번 주소
        place_other_adress = other_addresses[index].text
        print(place_other_adress)

time_wait(10, '#search\.keyword\.query')

search = driver.find_element(By.CSS_SELECTOR, '#search\.keyword\.query')
search.send_keys(key_word)
search.send_keys(Keys.ENTER)

sleep(1)

place_tab = driver.find_element(By.CSS_SELECTOR, '#info\.main\.options > li.option1 > a')
place_tab.send_keys(Keys.ENTER)

sleep(1)

place_list_print()

driver.quit()