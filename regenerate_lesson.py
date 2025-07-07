#!/usr/bin/env python3
"""
重新生成今天的課程，包含圖像處理改進
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def regenerate_todays_lesson():
    """重新生成今天的課程"""
    logger.info("🔄 開始重新生成今天的課程...")
    
    try:
        # 使用現有的 orchestrator
        from orchestrator import create_production_orchestrator
        
        orchestrator = create_production_orchestrator()
        
        # 執行完整的課程生成流程
        orchestrator.execute_daily_lesson_generation()
        
        logger.info("✅ 課程重新生成完成")
        
        # 檢查結果
        date_str = datetime.now().strftime('%Y-%m-%d')
        json_file = Path(f"docs/{date_str}.json")
        html_file = Path(f"docs/{date_str}.html")
        
        if json_file.exists():
            logger.info(f"📄 JSON 檔案已生成: {json_file}")
            
            # 讀取並顯示結果
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            lessons = data.get('lessons', [])
            if lessons:
                lesson = lessons[0]
                logger.info(f"📚 課程資訊:")
                logger.info(f"  科目: {lesson.get('subject', 'N/A')}")
                logger.info(f"  標題: {lesson.get('title', 'N/A')}")
                logger.info(f"  圖像URL: {lesson.get('image_url', 'None')}")
                
                if lesson.get('image_url'):
                    logger.info("🖼️ 圖像生成成功")
                else:
                    logger.warning("⚠️ 圖像生成失敗")
        else:
            logger.error(f"❌ JSON 檔案未生成: {json_file}")
        
        if html_file.exists():
            logger.info(f"🌐 HTML 檔案已生成: {html_file}")
        else:
            logger.error(f"❌ HTML 檔案未生成: {html_file}")
            
    except Exception as e:
        logger.error(f"❌ 重新生成失敗: {str(e)}")
        raise

if __name__ == "__main__":
    regenerate_todays_lesson()
