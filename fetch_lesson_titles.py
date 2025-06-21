from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

def fetch_titles(subject_name, url, title_selector, title_filter=None):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        titles = soup.select(title_selector)
        for title in titles:
            text = title.get_text(strip=True)
            if title_filter is None or title_filter(text):
                print(f'{subject_name}\t{text}')
    finally:
        driver.quit()

def filter_nature(text):
    # 自然: 【數字-數字】
    return re.match(r'【\d+-\d+】', text)

def filter_chinese(text):
    # 國文: 只抓含【】符號的項目，如【第一課】 聲音鐘
    return re.search(r'【[^】]+】', text)

def filter_history(text):
    # 歷史: 只抓「主題X」或「單元X」開頭
    return re.match(r'【\d+-\d+】', text)

def filter_geography(text):
    # 地理: 只抓「主題X」或「單元X」開頭
     return re.match(r'【\d+-\d+】', text)

def filter_civics(text):
    # 公民: 只抓「主題X」或「單元X」開頭
     return re.match(r'【\d+-\d+】', text)

subjects = [
    {
        'name': '自然',
        'url': 'https://www.learnmode.net/course/638520/content',
        'selector': 'h3.chapter-name',
        'filter': filter_nature
    },
    {
        'name': '國文',
        'url': 'https://www.learnmode.net/course/638508/content',
        'selector': 'h3.chapter-name',
        'filter': filter_chinese
    },
    {
        'name': '歷史',
        'url': 'https://www.learnmode.net/course/638740/content',
        'selector': 'h3.chapter-name',
        'filter': filter_history
    },
    {
        'name': '地理',
        'url': 'https://www.learnmode.net/course/638739/content',
        'selector': 'h3.chapter-name',
        'filter': filter_geography
    },
    {
        'name': '公民',
        'url': 'https://www.learnmode.net/course/638741/content',
        'selector': 'h3.chapter-name',
        'filter': filter_civics
    },
]

for subj in subjects:
    fetch_titles(subj['name'], subj['url'], subj['selector'], subj['filter'])
