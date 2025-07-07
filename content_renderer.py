"""
Content rendering service following SOLID principles
"""

import json
import urllib.parse
from typing import Dict
from datetime import datetime
from interfaces import ContentRenderer


class EnhancedHtmlRenderer(ContentRenderer):
    """Renders lesson content as HTML with image display and redirect"""
    
    def render(self, lesson_data: Dict, date_str: str) -> str:
        """Render lesson data into HTML format with image display"""
        title = lesson_data['title']
        subject = lesson_data['subject']
        image_url = lesson_data.get('image_url')
        
        # Create prompt for Perplexity AI
        prompt = f"請根據附檔的課文教學重點格式，提供一篇詳細的課文學習教材，內容盡可能的詳細，題目如下: {title}"
        url_encoded = urllib.parse.quote(prompt)
        perplexity_link = f"https://www.perplexity.ai/search?q={url_encoded}"
        
        # Generate HTML with image display and delayed redirect
        html_content = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - {subject}</title>
    <style>
        body {{
            font-family: "Microsoft JhengHei", sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            margin-bottom: 10px;
        }}
        .subject {{
            color: #7f8c8d;
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 30px;
        }}
        .lesson-image {{
            width: 100%;
            max-width: 600px;
            height: auto;
            display: block;
            margin: 20px auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .redirect-info {{
            text-align: center;
            padding: 20px;
            background-color: #e8f5e8;
            border-radius: 5px;
            margin-top: 20px;
        }}
        .manual-link {{
            display: inline-block;
            margin-top: 15px;
            padding: 15px 30px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-size: 1.2em;
            font-weight: bold;
            transition: background-color 0.3s;
        }}
        .manual-link:hover {{
            background-color: #2980b9;
        }}
        .image-placeholder {{
            width: 100%;
            height: 300px;
            background-color: #ecf0f1;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #7f8c8d;
            font-size: 1.1em;
            border-radius: 10px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{title}</h1>
        <div class="subject">{subject}</div>
        
        {self._generate_image_html(image_url)}
        
        <div class="redirect-info">
            <p>點擊下方按鈕開始學習：</p>
            <a href="{perplexity_link}" class="manual-link">開始學習</a>
        </div>
    </div>
</body>
</html>'''
        
        return html_content
    
    def _generate_image_html(self, image_url: str) -> str:
        """Generate HTML for displaying the lesson image"""
        if image_url:
            # 檢查是否為模擬URL
            if image_url.startswith('https://example.com/mock-images/'):
                return f'''<div class="image-placeholder">
                    <p>🎨 圖像生成功能正在開發中</p>
                    <p>模擬圖像 URL: <code>{image_url}</code></p>
                </div>'''
            else:
                return f'<img src="{image_url}" alt="課程圖像" class="lesson-image" onerror="this.parentElement.innerHTML=\'<div class=&quot;image-placeholder&quot;>圖像載入失敗</div>\'">'
        else:
            return '<div class="image-placeholder">課程圖像生成中...</div>'


class JsonRenderer(ContentRenderer):
    """Renders lesson content as JSON format"""
    
    def render(self, lesson_data: Dict, date_str: str) -> str:
        """Render lesson data into JSON format"""
        output_data = {
            "date": date_str,
            "lessons": [lesson_data],
            "generated_at": datetime.now().isoformat()
        }
        return json.dumps(output_data, ensure_ascii=False, indent=2)


class LegacyHtmlRenderer(ContentRenderer):
    """Renders lesson content as legacy HTML redirect format"""
    
    def render(self, lesson_data: Dict, date_str: str) -> str:
        """Render lesson data into legacy HTML redirect format"""
        title = lesson_data['title']
        prompt = f"請根據附檔的課文教學重點格式，提供一篇詳細的課文學習教材，內容盡可能的詳細，題目如下: {title}"
        url_encoded = urllib.parse.quote(prompt)
        link = f"https://www.perplexity.ai/search?q={url_encoded}"
        
        return f'''<!DOCTYPE html>
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