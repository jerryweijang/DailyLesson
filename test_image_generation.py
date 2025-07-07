#!/usr/bin/env python3
"""
Test script to debug image generation issues
"""

import logging
from image_service import MockImageGenerator, EducationalImageService

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_mock_image_generation():
    """Test if mock image generator works"""
    logger.info("Testing mock image generator...")
    
    # Create mock generator
    mock_generator = MockImageGenerator()
    
    # Test direct generation
    image_url = mock_generator.generate_image(
        subject="自然",
        title="【4-4】 生態系的類型",
        content="【4-4】 生態系的類型"
    )
    
    logger.info(f"Mock generator returned: {image_url}")
    
    # Test through service
    service = EducationalImageService(mock_generator)
    
    service_url = service.generate_lesson_image(
        subject="自然",
        lesson_title="【4-4】 生態系的類型",
        content="【4-4】 生態系的類型"
    )
    
    logger.info(f"Service returned: {service_url}")
    
    return service_url

def test_lesson_data_enhancement():
    """Test the lesson data enhancement process"""
    logger.info("Testing lesson data enhancement...")
    
    # Create sample lesson data
    lesson_data = {
        "id": "自然_20",
        "subject": "自然",
        "title": "【4-4】 生態系的類型",
        "content": "【4-4】 生態系的類型",
        "source_url": "https://www.learnmode.net/course/638520/content"
    }
    
    logger.info(f"Original lesson data: {lesson_data}")
    
    # Create service
    mock_generator = MockImageGenerator()
    service = EducationalImageService(mock_generator)
    
    # Generate image
    image_url = service.generate_lesson_image(
        lesson_data['subject'],
        lesson_data['title'],
        lesson_data.get('content', '')
    )
    
    logger.info(f"Generated image URL: {image_url}")
    
    if image_url:
        lesson_data['image_url'] = image_url
        
    logger.info(f"Enhanced lesson data: {lesson_data}")
    
    return lesson_data

if __name__ == "__main__":
    logger.info("🔍 Starting image generation debugging...")
    
    try:
        # Test 1: Mock generator
        mock_url = test_mock_image_generation()
        
        # Test 2: Data enhancement
        enhanced_data = test_lesson_data_enhancement()
        
        logger.info("✅ All tests completed successfully!")
        logger.info(f"Final enhanced data: {enhanced_data}")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        raise