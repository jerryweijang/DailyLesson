#!/usr/bin/env python3
"""
Demonstration script for the ImageService implementation
Now using SOLID principles and proper orchestration
"""

import logging
from orchestrator import create_demo_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Execute demonstration of the daily lesson system"""
    logger.info("🎯 開始執行 ImageService 示範...")
    
    try:
        # Create orchestrator with demo dependencies (mock image generator)
        orchestrator = create_demo_orchestrator()
        
        # Execute the complete daily lesson generation process
        orchestrator.execute_daily_lesson_generation()
        
        logger.info("✅ 示範完成！")
        logger.info("📁 請檢查 docs/ 資料夾中的生成檔案")
        
    except Exception as e:
        logger.error(f"❌ 示範執行失敗: {str(e)}")
        raise


if __name__ == "__main__":
    main()