from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
import time

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

print('='*73)
print('Detecting...')

driver = webdriver.Chrome('/Users/happy/Downloads/chromedriver')

driver.get('https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fwww.coupang.com%2Fnp%2Fpost%2Flogin%3Fr%3Dhttps%253A%252F%252Fwww.coupang.com%252F')

driver.find_element_by_name('email').send_keys('') #쿠팡 아이디 입력
driver.find_element_by_name('password').send_keys('') # 쿠팡 비밀번호 입력
driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[5]/button').click()

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#logout"))
    )

driver.get('https://www.coupang.com/np/categories/310894?listSize=120&brand=&offerCondition=&filterType=rocket%2Ccoupang_global&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=latestAsc&filter=&component=310794&rating=0&rocketAll=true')
# driver.get('https://www.coupang.com/np/categories/310886?listSize=60&brand=&offerCondition=&filterType=rocket%2Ccoupang_global&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=Y&selectedPlpKeepFilter=&sorter=latestAsc&filter=&component=310786&rating=0&rocketAll=true')



while True:

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    items = soup.select('#productList .baby-product a.baby-product-link')

    have = [item for item in items if not "일시품절" in item.dd.text]

    if have:
        print("Detected!")
        # print(have)
        driver.get('https://www.coupang.com{}'.format(have[0]['href']))
        # toaster = ToastNotifier()
        # toaster.show_toast("마스크 떴냐?","마스크 떴다!")
        
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
            break
        else:
            break
    else:
        driver.refresh()
    
    # time.sleep(0.5)
