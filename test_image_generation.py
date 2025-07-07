#!/usr/bin/env python3
"""
測試圖像生成功能的腳本
"""

import os
import logging
from datetime import datetime
from orchestrator import create_production_orchestrator, create_demo_orchestrator

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_image_generation():
    """測試圖像生成功能"""
    logger.info("🧪 開始測試圖像生成功能...")
    
    # 測試範例課程資料
    test_lesson = {
        'id': 'test_lesson',
        'subject': '自然',
        'title': '【4-4】 生態系的類型',
        'content': '【4-4】 生態系的類型',
        'source_url': 'https://www.learnmode.net/course/638520/content'
    }
    
    # 檢查是否有 GitHub Token
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        logger.info("✅ 找到 GITHUB_TOKEN，將使用真實圖像生成")
        orchestrator = create_production_orchestrator()
    else:
        logger.info("⚠️ 未找到 GITHUB_TOKEN，將使用模擬圖像生成")
        orchestrator = create_demo_orchestrator()
    
    # 測試圖像生成
    try:
        enhanced_lesson = orchestrator._enhance_lesson_with_image(test_lesson)
        
        logger.info("📊 測試結果:")
        logger.info(f"  科目: {enhanced_lesson['subject']}")
        logger.info(f"  標題: {enhanced_lesson['title']}")
        logger.info(f"  圖像URL: {enhanced_lesson.get('image_url', 'None')}")
        logger.info(f"  生成時間: {enhanced_lesson.get('image_generated_at', 'None')}")
        
        if enhanced_lesson.get('image_error'):
            logger.error(f"  錯誤: {enhanced_lesson['image_error']}")
        
        # 測試 HTML 渲染
        html_content = orchestrator.html_renderer.render(enhanced_lesson, datetime.now().strftime('%Y-%m-%d'))
        
        # 檢查 HTML 中是否包含圖像相關內容
        if 'class="lesson-image"' in html_content:
            logger.info("✅ HTML 包含圖像標籤")
        elif 'image-placeholder' in html_content:
            logger.info("ℹ️ HTML 包含佔位符")
        else:
            logger.warning("❌ HTML 中未找到圖像相關內容")
            
    except Exception as e:
        logger.error(f"❌ 測試失敗: {str(e)}")
        raise

if __name__ == "__main__":
    test_image_generation()
