from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# 設定 Chrome options
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# 直接由 selenium-manager 取得 ChromeDriver
driver = webdriver.Chrome(options=options)

try:
    url = 'https://www.learnmode.net/course/638520/content'
    driver.get(url)
    time.sleep(5)  # 等待 JS 載入

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 依實際網頁結構調整 selector
    titles = soup.select('h3.chapter-name')

    for title in titles:
        print(title.get_text(strip=True))
finally:
    driver.quit()
