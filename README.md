# mask-detector
쿠팡 마스크 알리미
## 사용방법  
`pip install selenium` selenium 설치  
`pip install bs4` beautifulSoup 설치  

`driver = webdriver.Chrome('')` 빈 부분에 크롬 웹 드라이버가 있는 위치를 지정해야한다.  
예를들어 `driver = webdriver.Chrome('/Users/happy/Downloads/chromedriver')`

```python
driver.find_element_by_name('email').send_keys('')
driver.find_element_by_name('password').send_keys('')
```
위의 빈 부분에는 쿠팡 아이디를, 아래에는 비밀번호를 넣어야한다.  
코드 수정 후 파이썬 파일을 실행시키면 프로그램이 작동한다.  

## 동작과정  
이 프로그램은 쿠팡에서 품절되지 않은 마스크가 있는지 파악하여  
구매 가능한 마스크가 있다면 해당 제품의 구매 페이지로 넘어가고  
전부 품절이라면 품절되지 않은 제품이 발견될 때까지 새로고침을 하며 찾는다.  

<img width=600 src="https://user-images.githubusercontent.com/52627952/86006459-f5127900-ba50-11ea-8fdc-7fa4d5f36e3d.gif">
