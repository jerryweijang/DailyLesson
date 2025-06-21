from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

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
    # 抓出所有章節名稱 <h3 class="chapter-name">
    titles = soup.select('h3.chapter-name')

    # 只保留符合【數字-數字】格式的章節名稱
    for title in titles:
        text = title.get_text(strip=True)
        if re.match(r'【\d+-\d+】', text):
            print(text)
finally:
    driver.quit()
