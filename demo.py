#!/usr/bin/env python3
"""
Demonstration script for the ImageService implementation
Shows how the system works with mock data (no actual API calls)
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List

# Add current directory to path
sys.path.append('.')

from image_service import EducationalImageService, enhance_lesson_with_image, save_enhanced_lesson_data

def mock_image_service():
    """Create a mock image service for demonstration"""
    class MockEducationalImageService(EducationalImageService):
        def __init__(self):
            # Don't call super().__init__ to avoid OpenAI client initialization
            import logging
            self.logger = logging.getLogger(__name__)
            
        def generate_lesson_image(self, subject: str, lesson_title: str, content: str):
            """Mock image generation - returns a mock URL"""
            prompt = self._create_educational_prompt(subject, lesson_title, content)
            
            # Generate a mock image URL based on the content
            mock_image_id = abs(hash(f"{subject}_{lesson_title}")) % 1000000
            mock_url = f"https://example.com/generated-images/{subject.lower()}_{mock_image_id}.jpg"
            
            self.logger.info(f"✓ 模擬圖像生成: {subject} - {lesson_title}")
            self.logger.info(f"  提示詞: {prompt[:80]}...")
            self.logger.info(f"  圖像URL: {mock_url}")
            
            return mock_url
    
    return MockEducationalImageService()

def create_sample_lessons() -> List[Dict]:
    """Create sample lesson data for demonstration"""
    return [
        {
            'id': 'nature_1',
            'subject': '自然',
            'title': '【1-1】生物的特徵',
            'content': '生物具有生長、繁殖、代謝等基本特徵，與非生物有明顯區別',
            'source_url': 'https://www.learnmode.net/course/638520/content'
        },
        {
            'id': 'chinese_1',
            'subject': '國文',
            'title': '【第一課】聲音鐘',
            'content': '探討聲音在生活中的重要性，以及如何用心聆聽周遭的聲音',
            'source_url': 'https://www.learnmode.net/course/638508/content'
        },
        {
            'id': 'history_1',
            'subject': '歷史',
            'title': '【1-1】史前台灣與原住民文化',
            'content': '台灣的史前文化發展與原住民族群的分布特色',
            'source_url': 'https://www.learnmode.net/course/638740/content'
        },
        {
            'id': 'geography_1',
            'subject': '地理',
            'title': '【1-1】台灣的位置與範圍',
            'content': '台灣位於亞洲東部，地理位置優越，具有重要的戰略地位',
            'source_url': 'https://www.learnmode.net/course/638739/content'
        },
        {
            'id': 'civics_1',
            'subject': '公民',
            'title': '【1-1】個人與社會',
            'content': '探討個人在社會中的角色與責任，以及人際關係的重要性',
            'source_url': 'https://www.learnmode.net/course/638741/content'
        }
    ]

def demonstrate_daily_selection(lessons: List[Dict]) -> Dict:
    """Demonstrate the daily lesson selection algorithm"""
    print("📅 每日課程選擇演示")
    print("-" * 50)
    
    # Simulate the daily selection algorithm from the existing system
    day_of_year = datetime.now().timetuple().tm_yday
    daily_lesson_idx = (day_of_year - 1) % len(lessons)
    selected_lesson = lessons[daily_lesson_idx]
    
    print(f"年度第 {day_of_year} 天")
    print(f"課程總數: {len(lessons)}")
    print(f"選中索引: {daily_lesson_idx}")
    print(f"今日課程: {selected_lesson['subject']} - {selected_lesson['title']}")
    print()
    
    return selected_lesson

def demonstrate_image_generation(lesson_data: Dict):
    """Demonstrate image generation for a lesson"""
    print("🎨 圖像生成演示")
    print("-" * 50)
    
    # Configure logging to show the process
    import logging
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    
    # Create mock image service
    image_service = mock_image_service()
    
    # Generate image for the lesson
    enhanced_lesson = enhance_lesson_with_image(lesson_data, image_service)
    
    print(f"✓ 圖像生成完成")
    print(f"  原始課程: {lesson_data['title']}")
    print(f"  增強後包含圖像: {'image_url' in enhanced_lesson}")
    print(f"  圖像URL: {enhanced_lesson.get('image_url', 'None')}")
    print()
    
    return enhanced_lesson

def demonstrate_json_output(enhanced_lesson: Dict):
    """Demonstrate JSON output format"""
    print("📄 JSON 輸出格式演示")
    print("-" * 50)
    
    # Create output directory if it doesn't exist
    os.makedirs('docs', exist_ok=True)
    
    # Save to JSON file
    date_str = datetime.now().strftime('%Y-%m-%d')
    save_enhanced_lesson_data(date_str, [enhanced_lesson])
    
    # Display the saved JSON
    json_file = f"docs/{date_str}.json"
    print(f"✓ JSON 文件已保存: {json_file}")
    
    with open(json_file, 'r', encoding='utf-8') as f:
        json_content = json.load(f)
    
    print("JSON 結構:")
    print(json.dumps(json_content, ensure_ascii=False, indent=2))
    print()
    
    return json_file

def demonstrate_html_compatibility(enhanced_lesson: Dict):
    """Demonstrate HTML redirect compatibility"""
    print("🔗 HTML 重定向兼容性演示")
    print("-" * 50)
    
    import urllib.parse
    
    title = enhanced_lesson['title']
    prompt = f"請根據附檔的課文教學重點格式，提供一篇詳細的課文學習教材，內容盡可能的詳細，題目如下: {title}"
    url_encoded = urllib.parse.quote(prompt)
    perplexity_link = f"https://www.perplexity.ai/search?q={url_encoded}"
    
    # Create HTML redirect file
    date_str = datetime.now().strftime('%Y-%m-%d')
    html_file = f"docs/{date_str}.html"
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0;url={perplexity_link}">
<title>跳轉中...</title>
</head>
<body>
如果沒有自動跳轉，請點擊 <a href="{perplexity_link}">{title}</a>
</body>
</html>'''
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ HTML 重定向文件已保存: {html_file}")
    print(f"✓ 重定向到: {perplexity_link[:80]}...")
    print()
    
    return html_file

def main():
    """Main demonstration function"""
    print("🚀 ImageService 實作演示")
    print("=" * 60)
    print()
    
    # Create sample lessons
    lessons = create_sample_lessons()
    print(f"📚 準備了 {len(lessons)} 個範例課程")
    for lesson in lessons:
        print(f"  - {lesson['subject']}: {lesson['title']}")
    print()
    
    # Demonstrate daily selection
    selected_lesson = demonstrate_daily_selection(lessons)
    
    # Demonstrate image generation
    enhanced_lesson = demonstrate_image_generation(selected_lesson)
    
    # Demonstrate JSON output
    json_file = demonstrate_json_output(enhanced_lesson)
    
    # Demonstrate HTML compatibility
    html_file = demonstrate_html_compatibility(enhanced_lesson)
    
    print("✅ 演示完成！")
    print("=" * 60)
    print(f"📁 生成的文件:")
    print(f"  - JSON: {json_file}")
    print(f"  - HTML: {html_file}")
    print()
    print("🔧 實際部署說明:")
    print("1. 在 GitHub Repository Settings > Secrets 中設定 GITHUB_TOKEN")
    print("2. 啟用 GitHub Actions workflow: daily-lesson-with-images.yml")
    print("3. 系統將每日自動執行，生成包含圖像的課程內容")
    print("4. 輸出同時包含 JSON 和 HTML 格式，保持向後兼容性")

if __name__ == "__main__":
    main()