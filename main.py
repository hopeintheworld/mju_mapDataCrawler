import json
import time
from time import sleep
import csv

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


def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, "Can't find CSS tag.")
        driver.quit()
    return wait

def search_keyword(key_word):
    time_wait(10, '#search\.keyword\.query')

    search = driver.find_element(By.CSS_SELECTOR, '#search\.keyword\.query')
    search.send_keys(key_word)
    search.send_keys(Keys.ENTER)

    sleep(1)

    place_tab = driver.find_element(By.CSS_SELECTOR, '#info\.main\.options > li.option1 > a')
    place_tab.send_keys(Keys.ENTER)
    
    
    sleep(1)

def kakao_place_list_crawl(current_page):
    time.sleep(2)
    
    place_dict_list = []
    
    place_list = driver.find_elements(By.CSS_SELECTOR, "#info\.search\.place\.list > li")
    names = driver.find_elements(By.CSS_SELECTOR, '#info\.search\.place\.list > li > div.head_item.clickArea > strong > a.link_name')
    addresses = driver.find_elements(By.CSS_SELECTOR, '#info\.search\.place\.list > li > div.info_item > div.addr > p:nth-child(1)')
    other_addresses = driver.find_elements(By.CSS_SELECTOR, '#info\.search\.place\.list > li > div.info_item > div.addr > p:nth-child(2)')
    phone_nums = driver.find_elements(By.CSS_SELECTOR, '#info\.search\.place\.list > li > div.info_item > div.contact.clickArea > span.phone')
    
    for index in range(len(place_list)):
        place_dict = {"_id":index + (current_page-1)*15, "name": "", "street_name_address": "", "street_number_address":"", "phone_num": ""}
        
        # 장소 이름
        place_dict["name"] = names[index].text
        #names[index] => A Selenium WebElement Class. It has text attribute that makes data to text type.
        
        # 장소 도로명 주소
        place_dict["street_name_address"] = addresses[index].text
        
        # 장소 지번 주소
        place_dict["street_number_address"] = other_addresses[index].text
        
        # 연락처
        place_dict["phone_num"] = phone_nums[index].text if phone_nums[index].text!="" else "null"
        
        # Dictionary data를 array에 추가.
        place_dict_list.append(place_dict)
        
    print(place_dict_list)
    return place_dict_list

def kakao_change_page():
    kakao_place = []
    current_page = 1
    page_index = 1
    error_cnt = 0    
    
    while 1:
        # 페이지 넘어가며 출력
        try:
            # 페이지 크롤링
            print("현재 페이지 크롤링 : ", current_page)
            print("페이지 인덱스 : ", page_index)
            crawl_result = kakao_place_list_crawl(current_page)
            
            kakao_place += crawl_result
            sleep(1)
            
            # 한 페이지에 장소 개수가 15개 미만이라면 해당 페이지는 마지막 페이지
            if len(crawl_result) < 15:
                print("마지막 페이지")
                break
            
            # (8) 다섯번째 페이지까지 왔다면 다음 버튼을 누르고 page2 = 0으로 초기화
            if page_index == 5:
                driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').send_keys(Keys.ENTER)
                page_index = 1
                
                sleep(1)
            elif page_index < 5:
                # (7) 페이지 번호 클릭
                page_index += 1
                driver.find_element(By.XPATH, f'//*[@id="info.search.page.no{page_index}"]').send_keys(Keys.ENTER)
                
                sleep(1)
            elif not driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]').is_enabled():
                # 다음 버튼을 누를 수 없다면 마지막 페이지
                break

            current_page += 1

        except Exception as e:
            error_cnt += 1
            
            if error_cnt > 3:
                break
            
    return kakao_place

#START
driver.get(url)

# 카카오맵 "스터디 카페" 키워드 검색.
key_word = '스터디 카페'
search_keyword(key_word)
result = kakao_change_page()

# CSV 파일로 변환
labels = ["_id", "name", "street_name_address", "street_number_address", "phone_num"]

with open("study_cafe.csv", "w") as file:
    writer = csv.DictWriter(file, fieldnames=labels)
    writer.writeheader()
    writer.writerows(result)

driver.quit()