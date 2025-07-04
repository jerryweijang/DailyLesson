import os
import asyncio
import logging
from typing import Optional, List, Dict
from openai import OpenAI
import json
from datetime import datetime
from interfaces import ImageGenerator


class PromptGenerator:
    """Single Responsibility: Generate prompts for educational content"""
    
    def __init__(self):
        self.subject_styles = {
            "自然": "scientific illustration, educational diagram, nature",
            "國文": "traditional Chinese calligraphy, literature, classical art",
            "歷史": "historical illustration, ancient artifacts, timeline",
            "地理": "geographical map, landscape, cultural landmarks",
            "公民": "civic education, society, democratic concepts"
        }
    
    def create_educational_prompt(self, subject: str, lesson_title: str, content: str) -> str:
        """建立教育內容相關的圖像提示詞"""
        style = self.subject_styles.get(subject, "educational illustration")
        
        # 限制內容長度，避免提示詞過長
        content_summary = content[:200] if len(content) > 200 else content
        
        prompt = f"""Create an educational illustration for {subject} lesson titled '{lesson_title}'. 
        Content focus: {content_summary}
        Style: {style}
        Requirements: suitable for 7th grade students, clear and informative, culturally appropriate for Taiwan education"""
        
        return prompt


class GitHubModelsImageGenerator(ImageGenerator):
    """Concrete implementation of ImageGenerator using GitHub Models API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=api_key or os.environ.get("GITHUB_TOKEN")
        )
        self.logger = logging.getLogger(__name__)
        self.prompt_generator = PromptGenerator()
        
    def generate_image(self, subject: str, title: str, content: str) -> Optional[str]:
        """Generate image for lesson content"""
        try:
            prompt = self.prompt_generator.create_educational_prompt(subject, title, content)
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                style="natural"
            )
            
            image_url = response.data[0].url
            self.logger.info(f"成功產生圖像: {subject} - {title}")
            return image_url
            
        except Exception as e:
            self.logger.error(f"圖像產生失敗: {subject} - {title}, 錯誤: {str(e)}")
            return None


class MockImageGenerator(ImageGenerator):
    """Mock implementation for testing - Open/Closed Principle"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def generate_image(self, subject: str, title: str, content: str) -> Optional[str]:
        """Generate mock image URL for testing"""
        self.logger.info(f"生成模擬圖像: {subject} - {title}")
        return f"https://example.com/mock-images/{subject}_{hash(title) % 10000}.jpg"


class EducationalImageService:
    """Service class that uses dependency injection - Dependency Inversion Principle"""
    
    def __init__(self, image_generator: ImageGenerator):
        self.image_generator = image_generator
        self.logger = logging.getLogger(__name__)
        
    def generate_lesson_image(self, subject: str, lesson_title: str, content: str) -> Optional[str]:
        """為課程內容產生相關圖像"""
        return self.image_generator.generate_image(subject, lesson_title, content)
    
    async def generate_batch_images(self, lessons: List[Dict]) -> Dict[str, str]:
        """批量產生課程圖像"""
        results = {}
        
        for lesson in lessons:
            try:
                image_url = self.generate_lesson_image(
                    lesson['subject'],
                    lesson['title'],
                    lesson['content']
                )
                if image_url:
                    results[lesson['id']] = image_url
                    
                # 避免 API 速率限制
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"批量處理失敗: {lesson['id']}, 錯誤: {str(e)}")
                
        return results