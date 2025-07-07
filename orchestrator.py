"""
Main orchestration service following SOLID principles
"""

import os
import time
import logging
from datetime import datetime
from typing import List, Dict
from interfaces import LessonFetcher, LessonSelector, ImageGenerator, ContentRenderer
from lesson_service import SeleniumLessonFetcher, DayBasedLessonSelector
from image_service import EducationalImageService, GitHubModelsImageGenerator, MockImageGenerator
from content_renderer import EnhancedHtmlRenderer, JsonRenderer


class DailyLessonOrchestrator:
    """
    Main orchestrator that coordinates all services
    Follows Dependency Inversion Principle by depending on abstractions
    """
    
    def __init__(self, 
                 lesson_fetcher: LessonFetcher,
                 lesson_selector: LessonSelector,
                 image_generator: ImageGenerator,
                 html_renderer: ContentRenderer,
                 json_renderer: ContentRenderer):
        self.lesson_fetcher = lesson_fetcher
        self.lesson_selector = lesson_selector
        self.image_service = EducationalImageService(image_generator)
        self.html_renderer = html_renderer
        self.json_renderer = json_renderer
        self.logger = logging.getLogger(__name__)
        
        # Subject configurations
        self.subjects = [
            {
                'name': '自然',
                'url': 'https://www.learnmode.net/course/638520/content',
                'selector': 'h3.chapter-name'
            },
            {
                'name': '國文',
                'url': 'https://www.learnmode.net/course/638508/content',
                'selector': 'h3.chapter-name'
            },
            {
                'name': '歷史',
                'url': 'https://www.learnmode.net/course/638740/content',
                'selector': 'h3.chapter-name'
            },
            {
                'name': '地理',
                'url': 'https://www.learnmode.net/course/638739/content',
                'selector': 'h3.chapter-name'
            },
            {
                'name': '公民',
                'url': 'https://www.learnmode.net/course/638741/content',
                'selector': 'h3.chapter-name'
            }
        ]
    
    def execute_daily_lesson_generation(self) -> None:
        """Execute the complete daily lesson generation process"""
        self.logger.info("開始執行課程抓取和圖像生成...")
        
        # Step 1: Fetch all lessons
        all_lessons = self._fetch_all_lessons()
        
        if not all_lessons:
            self.logger.warning("沒有找到任何課程")
            return
        
        # Step 2: Select daily lesson
        daily_lesson = self.lesson_selector.select_daily_lesson(all_lessons)
        self.logger.info(f"今日課程: {daily_lesson['subject']} - {daily_lesson['title']}")
        
        # Step 3: Generate image for lesson
        enhanced_lesson = self._enhance_lesson_with_image(daily_lesson)
        
        # Step 4: Render and save content
        date_str = datetime.now().strftime('%Y-%m-%d')
        self._save_lesson_content(enhanced_lesson, date_str)
        
        self.logger.info("課程處理完成")
    
    def _fetch_all_lessons(self) -> List[Dict]:
        """Fetch lessons from all subjects"""
        all_lessons = []
        
        for subject in self.subjects:
            self.logger.info(f"正在抓取科目: {subject['name']}")
            lessons = self.lesson_fetcher.fetch_lessons(subject)
            all_lessons.extend(lessons)
            
            # Avoid excessive requests
            time.sleep(2)
        
        self.logger.info(f"總共抓取到 {len(all_lessons)} 個課程")
        return all_lessons
    
    def _enhance_lesson_with_image(self, lesson_data: Dict) -> Dict:
        """Add image to lesson data"""
        self.logger.info(f"開始為課程生成圖像: {lesson_data['subject']} - {lesson_data['title']}")
        
        image_url = self.image_service.generate_lesson_image(
            lesson_data['subject'],
            lesson_data['title'],
            lesson_data.get('content', '')
        )
        
        if image_url:
            lesson_data['image_url'] = image_url
            lesson_data['image_generated_at'] = datetime.now().isoformat()
            self.logger.info(f"圖像生成成功: {image_url}")
        else:
            self.logger.warning(f"圖像生成失敗: {lesson_data['subject']} - {lesson_data['title']}")
            lesson_data['image_url'] = None
            lesson_data['image_error'] = "圖像生成失敗"
        
        return lesson_data
    
    def _save_lesson_content(self, lesson_data: Dict, date_str: str) -> None:
        """Save lesson content in both HTML and JSON formats"""
        # Ensure docs directory exists
        os.makedirs('docs', exist_ok=True)
        
        # Save HTML with image display
        html_content = self.html_renderer.render(lesson_data, date_str)
        html_file = f"docs/{date_str}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        self.logger.info(f"已生成 HTML 檔案: {html_file}")
        
        # Save JSON data
        json_content = self.json_renderer.render(lesson_data, date_str)
        json_file = f"docs/{date_str}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            f.write(json_content)
        self.logger.info(f"已生成 JSON 檔案: {json_file}")


def create_production_orchestrator() -> DailyLessonOrchestrator:
    """Factory function to create production-ready orchestrator"""
    lesson_fetcher = SeleniumLessonFetcher()
    lesson_selector = DayBasedLessonSelector()
    
    # Use real image generator if GitHub token is available, otherwise use mock
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        image_generator = GitHubModelsImageGenerator(github_token)
        logging.info("使用真實的圖像生成器 (GitHub Models API)")
    else:
        image_generator = MockImageGenerator()
        logging.warning("未找到 GITHUB_TOKEN，使用模擬圖像生成器")
        logging.info("若要使用真實圖像生成，請設定 GITHUB_TOKEN 環境變數")
    
    html_renderer = EnhancedHtmlRenderer()
    json_renderer = JsonRenderer()
    
    return DailyLessonOrchestrator(
        lesson_fetcher=lesson_fetcher,
        lesson_selector=lesson_selector,
        image_generator=image_generator,
        html_renderer=html_renderer,
        json_renderer=json_renderer
    )


def create_demo_orchestrator() -> DailyLessonOrchestrator:
    """Factory function to create demo orchestrator with mock services"""
    lesson_fetcher = SeleniumLessonFetcher()
    lesson_selector = DayBasedLessonSelector()
    image_generator = MockImageGenerator()
    html_renderer = EnhancedHtmlRenderer()
    json_renderer = JsonRenderer()
    
    return DailyLessonOrchestrator(
        lesson_fetcher=lesson_fetcher,
        lesson_selector=lesson_selector,
        image_generator=image_generator,
        html_renderer=html_renderer,
        json_renderer=json_renderer
    )