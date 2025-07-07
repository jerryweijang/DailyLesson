#!/usr/bin/env python3
"""
診斷目前系統狀態的腳本
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def diagnose_system():
    """診斷系統狀態"""
    logger.info("🔍 開始診斷系統狀態...")
    
    # 1. 檢查環境變數
    logger.info("📋 檢查環境變數:")
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        logger.info(f"  ✅ GITHUB_TOKEN: 存在 (長度: {len(github_token)})")
    else:
        logger.warning("  ⚠️ GITHUB_TOKEN: 不存在")
    
    # 2. 檢查 docs 目錄
    docs_path = Path("docs")
    if docs_path.exists():
        logger.info(f"📁 docs 目錄存在，包含 {len(list(docs_path.glob('*')))} 個檔案")
        
        # 檢查最新的 JSON 檔案
        json_files = list(docs_path.glob("*.json"))
        if json_files:
            latest_json = max(json_files, key=lambda f: f.stat().st_mtime)
            logger.info(f"📄 最新 JSON 檔案: {latest_json.name}")
            
            try:
                with open(latest_json, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                lessons = data.get('lessons', [])
                if lessons:
                    lesson = lessons[0]
                    logger.info(f"📚 課程資訊:")
                    logger.info(f"  科目: {lesson.get('subject', 'N/A')}")
                    logger.info(f"  標題: {lesson.get('title', 'N/A')}")
                    logger.info(f"  圖像URL: {lesson.get('image_url', 'None')}")
                    logger.info(f"  生成時間: {lesson.get('image_generated_at', 'None')}")
                    
                    if lesson.get('image_error'):
                        logger.error(f"  錯誤: {lesson['image_error']}")
                    
                    # 診斷圖像問題
                    image_url = lesson.get('image_url')
                    if image_url is None:
                        logger.warning("🚨 診斷: 圖像URL為空，表示圖像生成失敗")
                        logger.info("💡 可能原因:")
                        logger.info("  1. GITHUB_TOKEN 未設定或無效")
                        logger.info("  2. GitHub Models API 呼叫失敗")
                        logger.info("  3. 網路連線問題")
                    elif image_url.startswith('https://example.com/mock-images/'):
                        logger.info("🎭 診斷: 使用模擬圖像生成器")
                        logger.info("💡 這是預期行為，因為沒有有效的 GITHUB_TOKEN")
                    else:
                        logger.info("🖼️ 診斷: 使用真實圖像URL")
                        
            except Exception as e:
                logger.error(f"❌ 讀取 JSON 檔案失敗: {str(e)}")
    else:
        logger.warning("📁 docs 目錄不存在")
    
    # 3. 檢查 HTML 檔案
    html_files = list(docs_path.glob("*.html")) if docs_path.exists() else []
    if html_files:
        latest_html = max(html_files, key=lambda f: f.stat().st_mtime)
        logger.info(f"🌐 最新 HTML 檔案: {latest_html.name}")
        
        try:
            with open(latest_html, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            if 'class="lesson-image"' in html_content:
                logger.info("✅ HTML 包含圖像標籤")
            elif 'image-placeholder' in html_content:
                logger.info("ℹ️ HTML 包含佔位符")
                if '課程圖像生成中' in html_content:
                    logger.warning("🚨 診斷: HTML 顯示 '課程圖像生成中'，確認圖像生成失敗")
            else:
                logger.warning("❌ HTML 中未找到圖像相關內容")
                
        except Exception as e:
            logger.error(f"❌ 讀取 HTML 檔案失敗: {str(e)}")
    
    # 4. 提供解決建議
    logger.info("💡 解決建議:")
    if not github_token:
        logger.info("  1. 設定 GITHUB_TOKEN 環境變數以啟用真實圖像生成")
        logger.info("  2. 或者接受使用模擬圖像生成器的結果")
    logger.info("  3. 檢查網路連線是否正常")
    logger.info("  4. 查看系統日誌以獲取更多錯誤資訊")

if __name__ == "__main__":
    diagnose_system()
