from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
import time
import asyncio

urls=[
    'https://www.coupang.com/np/categories/310894?listSize=120&brand=&offerCondition=&filterType=rocket%2Ccoupang_global&isPriceRange=false&minPrice=&maxPrice=&page=1&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=latestAsc&filter=&component=310794&rating=0&rocketAll=true',
    'https://www.coupang.com/np/categories/310894?listSize=120&brand=&offerCondition=&filterType=rocket%2Ccoupang_global&isPriceRange=false&minPrice=&maxPrice=&page=2&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=latestAsc&filter=&component=310794&rating=0&rocketAll=true',
    'https://www.coupang.com/np/categories/310894?listSize=120&brand=&offerCondition=&filterType=rocket%2Ccoupang_global&isPriceRange=false&minPrice=&maxPrice=&page=3&channel=user&fromComponent=N&selectedPlpKeepFilter=&sorter=latestAsc&filter=&component=310794&rating=0&rocketAll=true',
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


async def get_driver():
    driver = webdriver.Chrome('/Users/happy/Downloads/chromedriver')
    driver.get('https://login.coupang.com/login/login.pang')

    driver.find_element_by_name('email').send_keys('') # 쿠팡 아이디 입력
    driver.find_element_by_name('password').send_keys('') # 쿠팡 비밀번호 입력
    driver.find_element_by_xpath('/html/body/div[1]/div/div/form/div[5]/button').click()

    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#logout"))
        )
    
    return driver

async def check_loop(url):
    driver = await get_driver()
    await asyncio.sleep(0.1)
    driver.get(url)
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        items = soup.select('#productList .baby-product a.baby-product-link')

        have = [item for item in items if not "일시품절" in item.dd.text]


        if have:
            print("Detected!")
            driver.get('https://www.coupang.com{}'.format(have[0]['href']))
            driver.maximize_window()
            toaster = ToastNotifier()
            toaster.show_toast("마스크 떴냐?","마스크 떴다!")
            while True:
                await asyncio.sleep(100)
        else:
            driver.refresh()
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(*[check_loop(url) for url in urls])

if __name__ ==  '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())