#!/usr/bin/env python3
"""
Main script for generating daily lessons with images
Now using SOLID principles and proper orchestration
"""

import logging
from orchestrator import create_production_orchestrator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main execution function"""
    try:
        # Create orchestrator with production dependencies
        orchestrator = create_production_orchestrator()
        
        # Execute the complete daily lesson generation process
        orchestrator.execute_daily_lesson_generation()
        
    except Exception as e:
        logger.error(f"執行失敗: {str(e)}")
        raise


if __name__ == "__main__":
    main()