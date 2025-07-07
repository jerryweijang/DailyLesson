#!/usr/bin/env python3
"""
Test script to reproduce the full flow and identify the issue
"""

import logging
import json
from datetime import datetime
from image_service import MockImageGenerator, EducationalImageService
from content_renderer import EnhancedHtmlRenderer, JsonRenderer

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_full_flow():
    """Test the complete flow from lesson data to rendered output"""
    logger.info("Testing complete flow...")
    
    # Sample lesson data (same as in existing JSON)
    lesson_data = {
        "id": "自然_20",
        "subject": "自然",
        "title": "【4-4】 生態系的類型",
        "content": "【4-4】 生態系的類型",
        "source_url": "https://www.learnmode.net/course/638520/content"
    }
    
    logger.info(f"Original lesson data: {lesson_data}")
    
    # Step 1: Generate image
    mock_generator = MockImageGenerator()
    service = EducationalImageService(mock_generator)
    
    image_url = service.generate_lesson_image(
        lesson_data['subject'],
        lesson_data['title'],
        lesson_data.get('content', '')
    )
    
    logger.info(f"Generated image URL: {image_url}")
    
    # Step 2: Enhance lesson data
    if image_url:
        lesson_data['image_url'] = image_url
        lesson_data['image_generated_at'] = datetime.now().isoformat()
        
    logger.info(f"Enhanced lesson data: {lesson_data}")
    
    # Step 3: Render HTML
    html_renderer = EnhancedHtmlRenderer()
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    html_content = html_renderer.render(lesson_data, date_str)
    
    logger.info("HTML content generated successfully")
    logger.info(f"HTML contains image_url: {'image_url' in str(html_content)}")
    
    # Step 4: Render JSON
    json_renderer = JsonRenderer()
    json_content = json_renderer.render(lesson_data, date_str)
    
    logger.info("JSON content generated successfully")
    logger.info(f"JSON content: {json_content}")
    
    # Step 5: Save test files
    with open('/tmp/test_output.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    with open('/tmp/test_output.json', 'w', encoding='utf-8') as f:
        f.write(json_content)
        
    logger.info("Test files saved to /tmp/test_output.html and /tmp/test_output.json")
    
    return lesson_data, html_content, json_content

def analyze_existing_files():
    """Analyze the existing files to understand the issue"""
    logger.info("Analyzing existing files...")
    
    # Read existing JSON
    with open('docs/2025-07-07.json', 'r', encoding='utf-8') as f:
        existing_json = json.load(f)
    
    logger.info(f"Existing JSON: {existing_json}")
    
    # Check if image_url is present
    lesson = existing_json['lessons'][0]
    has_image_url = 'image_url' in lesson
    
    logger.info(f"Existing lesson has image_url: {has_image_url}")
    
    if not has_image_url:
        logger.error("❌ The existing lesson data does NOT contain image_url field!")
        logger.error("This explains why the HTML shows the placeholder.")
    
    return existing_json

if __name__ == "__main__":
    logger.info("🔍 Starting full flow test...")
    
    try:
        # Test 1: Analyze existing files
        existing_data = analyze_existing_files()
        
        # Test 2: Test full flow
        enhanced_data, html_content, json_content = test_full_flow()
        
        logger.info("✅ All tests completed successfully!")
        logger.info("Check /tmp/test_output.* files to see the correct output")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        raise