#!/usr/bin/env python3
"""
Test script to verify image generation functionality
Usage: python test_image_generation.py
"""

import os
import sys
import logging
from datetime import datetime

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from image_service import EducationalImageService, GitHubModelsImageGenerator, MockImageGenerator
from content_renderer import EnhancedHtmlRenderer, JsonRenderer

def test_image_generation():
    """Test image generation with fallback mechanism"""
    
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    logger.info("🧪 Testing image generation functionality...")
    
    # Test lesson data
    test_lesson = {
        "id": "test_lesson",
        "subject": "自然",
        "title": "測試課程",
        "content": "測試課程內容",
        "source_url": "https://example.com"
    }
    
    # Test with GitHub Models API (with fallback)
    github_token = os.environ.get("GITHUB_TOKEN")
    if github_token:
        logger.info("Testing with GitHub Models API...")
        image_generator = GitHubModelsImageGenerator(github_token)
    else:
        logger.info("No GitHub token found, testing with mock generator...")
        image_generator = MockImageGenerator()
    
    image_service = EducationalImageService(image_generator)
    
    # Generate image
    image_url = image_service.generate_lesson_image(
        test_lesson['subject'],
        test_lesson['title'],
        test_lesson.get('content', '')
    )
    
    if image_url:
        test_lesson['image_url'] = image_url
        test_lesson['image_generated_at'] = datetime.now().isoformat()
        logger.info(f"✅ Image generated successfully: {image_url}")
        
        # Test HTML rendering
        html_renderer = EnhancedHtmlRenderer()
        html_content = html_renderer.render(test_lesson, datetime.now().strftime('%Y-%m-%d'))
        
        # Check if HTML contains image
        if '<img src="' in html_content and 'lesson-image' in html_content:
            logger.info("✅ HTML rendering successful - image tag found")
            
            # Check that placeholder is not present
            if '課程圖像生成中' not in html_content:
                logger.info("✅ No placeholder text found in HTML")
                return True
            else:
                logger.error("❌ Placeholder text still present in HTML")
                return False
        else:
            logger.error("❌ HTML rendering failed - no image tag found")
            return False
    else:
        logger.error("❌ Image generation failed")
        return False

if __name__ == "__main__":
    success = test_image_generation()
    if success:
        print("🎉 Image generation test passed!")
        sys.exit(0)
    else:
        print("💥 Image generation test failed!")
        sys.exit(1)