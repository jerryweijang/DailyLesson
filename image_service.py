import os
import asyncio
import logging
from typing import Optional, List, Dict
from openai import OpenAI
import json
from datetime import datetime

class EducationalImageService:
    """教育內容圖像產生服務"""
    
    def __init__(self):
        self.client = OpenAI(
            base_url="https://models.inference.ai.azure.com",
            api_key=os.environ.get("GITHUB_TOKEN")
        )
        self.logger = logging.getLogger(__name__)
        
    def generate_lesson_image(self, subject: str, lesson_title: str, content: str) -> Optional[str]:
        """為課程內容產生相關圖像"""
        try:
            # 建立適合教育內容的提示詞
            prompt = self._create_educational_prompt(subject, lesson_title, content)
            
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                style="natural"
            )
            
            image_url = response.data[0].url
            self.logger.info(f"成功產生圖像: {subject} - {lesson_title}")
            return image_url
            
        except Exception as e:
            self.logger.error(f"圖像產生失敗: {subject} - {lesson_title}, 錯誤: {str(e)}")
            return None
    
    def _create_educational_prompt(self, subject: str, lesson_title: str, content: str) -> str:
        """建立教育內容相關的圖像提示詞"""
        # 根據科目調整提示詞風格
        subject_styles = {
            "自然": "scientific illustration, educational diagram, nature",
            "國文": "traditional Chinese calligraphy, literature, classical art",
            "歷史": "historical illustration, ancient artifacts, timeline",
            "地理": "geographical map, landscape, cultural landmarks",
            "公民": "civic education, society, democratic concepts"
        }
        
        style = subject_styles.get(subject, "educational illustration")
        
        # 限制內容長度，避免提示詞過長
        content_summary = content[:200] if len(content) > 200 else content
        
        prompt = f"""Create an educational illustration for {subject} lesson titled '{lesson_title}'. 
        Content focus: {content_summary}
        Style: {style}
        Requirements: suitable for 7th grade students, clear and informative, culturally appropriate for Taiwan education"""
        
        return prompt
    
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

def enhance_lesson_with_image(lesson_data: Dict, image_service: EducationalImageService) -> Dict:
    """為課程資料增加圖像"""
    image_url = image_service.generate_lesson_image(
        lesson_data['subject'],
        lesson_data['title'],
        lesson_data.get('content', '')
    )
    
    if image_url:
        lesson_data['image_url'] = image_url
        lesson_data['image_generated_at'] = datetime.now().isoformat()
    
    return lesson_data

def save_enhanced_lesson_data(date_str: str, lessons_with_images: List[Dict]):
    """儲存包含圖像的課程資料到 docs 資料夾"""
    output_path = f"docs/{date_str}.json"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "date": date_str,
            "lessons": lessons_with_images,
            "generated_at": datetime.now().isoformat()
        }, f, ensure_ascii=False, indent=2)