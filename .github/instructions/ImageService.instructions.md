# 圖像服務開發指令

---
applyTo: '**'
---

## 概述
此指令檔案提供 GitHub Copilot 關於建立 Python 圖像服務的程式碼標準、領域知識和偏好設定。本專案專注於教育內容的自動化處理和圖像產生，將在 GitHub Actions workflow 中自動執行。

## GitHub Models API 設定

### 環境變數設定
使用 GitHub Personal Access Token (PAT) 和環境變數進行 Azure OpenAI 模型的身份驗證：

```python
import os
from openai import OpenAI

# GitHub Models API 設定
# 需要在 GitHub Actions secrets 中設定 GITHUB_TOKEN
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ.get("GITHUB_TOKEN")
)

# 用於圖像產生的範例
def generate_image(prompt: str) -> str:
    """使用 DALL-E 產生圖像"""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    return response.data[0].url
```

## Python 圖像服務程式碼標準

### 1. 類別結構
- 使用 `ImageService` 類別封裝圖像產生邏輯
- 實作適當的錯誤處理和重試機制
- 支援多種圖像格式和尺寸

### 2. 設定管理
- 使用環境變數儲存敏感資訊
- 支援本地開發和 GitHub Actions 環境
- 實作設定驗證

### 3. 錯誤處理
- 使用 Python logging 模組
- 實作重試機制處理 API 限制
- 提供詳細的錯誤訊息

### 4. 非同步處理
- 使用 `asyncio` 處理並發請求
- 支援批量圖像產生
- 實作適當的速率限制

## 教育內容圖像服務實作

### 主要圖像服務類別
```python
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
```

### 與現有專案整合
```python
# 擴展現有的 fetch_lesson_titles.py
import json
from datetime import datetime

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
```

## GitHub Actions Workflow 整合

### requirements.txt
```txt
openai>=1.12.0
selenium>=4.15.0
beautifulsoup4>=4.12.0
asyncio
```

### 環境變數設定
在 GitHub Repository Settings > Secrets and variables > Actions 中設定：
- `GITHUB_TOKEN`: GitHub Personal Access Token (具備 GitHub Models 存取權限)

### Workflow 範例
```yaml
# .github/workflows/daily-lesson-with-images.yml
name: Daily Lesson with Images

on:
  schedule:
    - cron: '0 22 * * *'  # 每日 06:00 台北時間 (UTC+8)
  workflow_dispatch:

jobs:
  generate-lessons:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Install Chrome
      run: |
        sudo apt-get update
        sudo apt-get install -y google-chrome-stable
    
    - name: Generate lessons with images
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: |
        python main_with_images.py
    
    - name: Commit and push
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add docs/
        git commit -m "Daily lesson update with images: $(date +'%Y-%m-%d')" || exit 0
        git push
```

## 最佳實務

### 1. 安全性
- 使用環境變數儲存 API 金鑰
- 絕不在程式碼中硬編碼敏感資訊
- 驗證輸入參數防止注入攻擊

### 2. 效能最佳化
- 實作圖像快取機制
- 使用非同步處理提升效率
- 控制 API 呼叫頻率避免限制

### 3. 錯誤處理
- 實作重試機制處理暫時性錯誤
- 記錄詳細的錯誤資訊
- 優雅處理 API 限制和超時

### 4. 監控
- 記錄 API 使用量
- 監控圖像產生成功率
- 追蹤處理時間和效能指標

## 圖像提示詞最佳實務

### 教育內容適用的提示詞模板
```python
SUBJECT_PROMPTS = {
    "自然": "scientific educational illustration showing {topic}, clear diagram style, suitable for middle school students",
    "國文": "traditional Chinese literature illustration depicting {topic}, classical art style, cultural elements",
    "歷史": "historical educational illustration of {topic}, accurate historical context, timeline visualization",
    "地理": "geographical educational map or landscape showing {topic}, clear labels, educational style",
    "公民": "civic education illustration explaining {topic}, modern design, democratic concepts"
}
```

### 避免的內容
- 暴力或不適當的圖像
- 版權受保護的角色或品牌
- 過於複雜的細節
- 文化不敏感的內容

## 注意事項
- 確保遵循 GitHub Models API 的使用條款
- 監控 API 使用量避免超出限制
- 定期更新套件以獲得最新功能
- 實作適當的快取機制以降低成本
- 考慮圖像檔案大小和載入效能