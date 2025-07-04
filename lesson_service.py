"""
Lesson fetching service following SOLID principles
"""

import re
import time
import logging
from datetime import datetime
from typing import List, Dict, Callable, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from interfaces import LessonFetcher, LessonSelector


class SubjectFilter:
    """Single Responsibility: Handle filtering logic for different subjects"""
    
    @staticmethod
    def filter_nature(text: str) -> bool:
        """自然: 【數字-數字】"""
        return bool(re.match(r'【\d+-\d+】', text))

    @staticmethod
    def filter_chinese(text: str) -> bool:
        """國文: 只抓含【】符號的項目，如【第一課】 聲音鐘"""
        return bool(re.search(r'【[^】]+】', text))

    @staticmethod
    def filter_history(text: str) -> bool:
        """歷史: 只抓「主題X」或「單元X」開頭"""
        return bool(re.match(r'【\d+-\d+】', text))

    @staticmethod
    def filter_geography(text: str) -> bool:
        """地理: 只抓「主題X」或「單元X」開頭"""
        return bool(re.match(r'【\d+-\d+】', text))

    @staticmethod
    def filter_civics(text: str) -> bool:
        """公民: 只抓「主題X」或「單元X」開頭"""
        return bool(re.match(r'【\d+-\d+】', text))


class SeleniumLessonFetcher(LessonFetcher):
    """Concrete implementation of LessonFetcher using Selenium"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.filter_map = {
            '自然': SubjectFilter.filter_nature,
            '國文': SubjectFilter.filter_chinese,
            '歷史': SubjectFilter.filter_history,
            '地理': SubjectFilter.filter_geography,
            '公民': SubjectFilter.filter_civics
        }
    
    def fetch_lessons(self, subject_config: Dict) -> List[Dict]:
        """Fetch lessons for a given subject configuration"""
        name = subject_config['name']
        url = subject_config['url']
        selector = subject_config['selector']
        filter_func = self.filter_map.get(name)
        
        return self._fetch_titles_structured(name, url, selector, filter_func)
    
    def _fetch_titles_structured(self, subject_name: str, url: str, title_selector: str, title_filter: Optional[Callable] = None) -> List[Dict]:
        """Fetch lesson titles and return structured data"""
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
                    self.logger.info(f"找到課程: {subject_name} - {text}")
                    
        except Exception as e:
            self.logger.error(f"抓取課程失敗: {subject_name}, 錯誤: {str(e)}")
        finally:
            driver.quit()
        
        return lessons


class DayBasedLessonSelector(LessonSelector):
    """Concrete implementation of LessonSelector using day-of-year algorithm"""
    
    def select_daily_lesson(self, lessons: List[Dict]) -> Dict:
        """Select the lesson for today from the available lessons"""
        if not lessons:
            raise ValueError("No lessons available for selection")
        
        day_of_year = datetime.now().timetuple().tm_yday
        daily_lesson_idx = (day_of_year - 1) % len(lessons)
        return lessons[daily_lesson_idx]