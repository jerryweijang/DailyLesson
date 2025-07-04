#!/usr/bin/env python3
"""
Main script for generating daily lessons with images
Integrates fetch_lesson_titles.py with EducationalImageService
"""

import os
import re
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from image_service import EducationalImageService, enhance_lesson_with_image, save_enhanced_lesson_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_titles_structured(subject_name, url, title_selector, title_filter=None):
    """
    Fetch lesson titles and return structured data
    Modified from fetch_lesson_titles.py to return structured data instead of printing
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    
    lessons = []
    try:
        driver.get(url)
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        titles = soup.select(title_selector)
        
        for i, title in enumerate(titles):
            text = title.get_text(strip=True)
            if title_filter is None or title_filter(text):
                lessons.append({
                    'id': f"{subject_name}_{i}",
                    'subject': subject_name,
                    'title': text,
                    'content': text,  # For now, use title as content
                    'source_url': url
                })
                logger.info(f"找到課程: {subject_name} - {text}")
                
    except Exception as e:
        logger.error(f"抓取課程失敗: {subject_name}, 錯誤: {str(e)}")
    finally:
        driver.quit()
    
    return lessons

def filter_nature(text):
    """自然: 【數字-數字】"""
    return re.match(r'【\d+-\d+】', text)

def filter_chinese(text):
    """國文: 只抓含【】符號的項目，如【第一課】 聲音鐘"""
    return re.search(r'【[^】]+】', text)

def filter_history(text):
    """歷史: 只抓「主題X」或「單元X」開頭"""
    return re.match(r'【\d+-\d+】', text)

def filter_geography(text):
    """地理: 只抓「主題X」或「單元X」開頭"""
    return re.match(r'【\d+-\d+】', text)

def filter_civics(text):
    """公民: 只抓「主題X」或「單元X」開頭"""
    return re.match(r'【\d+-\d+】', text)

def main():
    """主要執行函數"""
    logger.info("開始執行課程抓取和圖像生成...")
    
    # 定義科目配置
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
    
    # 抓取所有課程標題
    all_lessons = []
    for subject in subjects:
        logger.info(f"正在抓取科目: {subject['name']}")
        lessons = fetch_titles_structured(
            subject['name'],
            subject['url'],
            subject['selector'],
            subject['filter']
        )
        all_lessons.extend(lessons)
        
        # 避免過度請求
        time.sleep(2)
    
    logger.info(f"總共抓取到 {len(all_lessons)} 個課程")
    
    # 選擇今日課程（模擬現有的日選算法）
    if all_lessons:
        import datetime
        day_of_year = datetime.datetime.now().timetuple().tm_yday
        daily_lesson_idx = (day_of_year - 1) % len(all_lessons)
        daily_lesson = all_lessons[daily_lesson_idx]
        
        logger.info(f"今日課程: {daily_lesson['subject']} - {daily_lesson['title']}")
        
        # 初始化圖像服務
        image_service = EducationalImageService()
        
        # 為今日課程產生圖像
        enhanced_lesson = enhance_lesson_with_image(daily_lesson, image_service)
        
        # 儲存增強後的課程資料
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
        save_enhanced_lesson_data(date_str, [enhanced_lesson])
        
        # 同時產生與現有系統兼容的 HTML 重定向檔案
        generate_html_redirect(enhanced_lesson, date_str)
        
        logger.info("課程處理完成")
    else:
        logger.warning("沒有找到任何課程")

def generate_html_redirect(lesson_data, date_str):
    """產生 HTML 重定向檔案（維持與現有系統的兼容性）"""
    import urllib.parse
    
    title = lesson_data['title']
    prompt = f"請根據附檔的課文教學重點格式，提供一篇詳細的課文學習教材，內容盡可能的詳細，題目如下: {title}"
    url_encoded = urllib.parse.quote(prompt)
    link = f"https://www.perplexity.ai/search?q={url_encoded}"
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0;url={link}">
<title>跳轉中...</title>
</head>
<body>
如果沒有自動跳轉，請點擊 <a href="{link}">{title}</a>
</body>
</html>'''
    
    html_file = f"docs/{date_str}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"已生成 HTML 重定向檔案: {html_file}")

if __name__ == "__main__":
    main()