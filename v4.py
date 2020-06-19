from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
import time
import multiprocessing

options = webdriver.ChromeOptions()  # 크롬 옵션 객체 생성
# 속도 향상을 위한 옵션 해제
prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2, 'geolocation': 2, 
'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 'ppapi_broker': 2, 'automatic_downloads': 2, 
'midi_sysex': 2, 'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 'protected_media_identifier': 2, 
'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}} 
options.add_experimental_option('prefs', prefs) 
options.add_argument("start-maximized") 
options.add_argument("disable-infobars") 
options.add_argument("--disable-extensions")

urls=[
    'https://www.coupang.com/np/search?q=%EB%A7%88%EC%8A%A4%ED%81%AC+kf94&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket%2C&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=auto&backgroundColor=&component=&rating=0&sorter=latestAsc&listSize=72',
    'https://www.coupang.com/np/search?q=%EB%A7%88%EC%8A%A4%ED%81%AC+kf94&brand=&offerCondition=&filter=&availableDeliveryFilter=&filterType=rocket%2C&isPriceRange=false&priceRange=&minPrice=&maxPrice=&page=1&trcid=&traid=&filterSetByUser=true&channel=auto&backgroundColor=&component=&rating=0&sorter=scoreDesc&listSize=72',
    # 'https://www.coupang.com/np/categories/310894?listSize=120&brand=&offerCondition=&filterType=rocket%2Ccoupang_global&isPriceRange=false&minPrice=&maxPrice=&page=3&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=latestAsc&filter=&component=310794&rating=0&rocketAll=true',
]


print(''' __   __  _______  _______  ___   _                                      
|  |_|  ||   _   ||       ||   | | |                                     
|       ||  |_|  ||  _____||   |_| |                                     
|       ||       || |_____ |      _|                                     
|       ||       ||_____  ||     |_                                      
| ||_|| ||   _   | _____| ||    _  |                                     
|_|   |_||__| |__||_______||___| |_|                                     
 ______   _______  _______  _______  _______  _______  _______  ______   
|      | |       ||       ||       ||       ||       ||       ||    _ |  
|  _    ||    ___||_     _||    ___||       ||_     _||   _   ||   | ||  
| | |   ||   |___   |   |  |   |___ |       |  |   |  |  | |  ||   |_||_ 
| |_|   ||    ___|  |   |  |    ___||      _|  |   |  |  |_|  ||    __  |
|       ||   |___   |   |  |   |___ |     |_   |   |  |       ||   |  | |
|______| |_______|  |___|  |_______||_______|  |___|  |_______||___|  |_|''')

print('='*10)
print('Detecting...')


def get_driver():
    driver = webdriver.Chrome('/Users/happy/Downloads/chromedriver')
    driver.get('https://login.coupang.com/login/login.pang')

    driver.find_element_by_name('email').send_keys('') # 쿠팡 아이디 입력
    driver.find_element_by_name('password').send_keys('') # 쿠팡 비밀번호 입력
    driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[5]/button').click()

    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#logout"))
    )
    
    return driver

def check_loop(url):
    driver = get_driver()
    driver.get(url)
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        items = soup.select('#productList .search-product a.search-product-link')

        have = [item for item in items if not "일시품절" in item.dd.text]


        if have:
            print("Detected!")
            driver.get('https://www.coupang.com{}'.format(have[0]['href']))
            # driver.maximize_window()
            # toaster = ToastNotifier()
            # toaster.show_toast("마스크 떴냐?","마스크 떴다!")
            # print(have)

            try:
                element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".prod-buy-btn"))
                )
                driver.find_element_by_xpath('//*[@id="contents"]/div[1]/div/div[3]/div[13]/div[2]/div[2]/button[2]').click()
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#pay-price-section"))
                )
                driver.find_element_by_xpath('//*[@id="paymentBtn"]').click()
            except:
                while True:
                    time.sleep(100)
            else:
                while True:
                    time.sleep(100)
        else:
            driver.refresh()
        time.sleep(1)


def main():
    p = [multiprocessing.Process(target=check_loop, args=(url, )) for url in urls]
    for i in p:
        i.start()
    for i in p:
        i.join()


if __name__ ==  '__main__':
    main()