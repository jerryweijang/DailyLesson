"""
Integration tests for the entire Daily Lesson system
"""
import pytest
import tempfile
import os
import json
from unittest.mock import patch, Mock
from orchestrator import create_demo_orchestrator
from datetime import datetime


class TestSystemIntegration:
    """Test entire system integration with real components"""
    
    def test_demo_system_end_to_end(self):
        """Test the complete demo system from start to finish"""
        # Create demo orchestrator (uses mock image generator)
        orchestrator = create_demo_orchestrator()
        
        # Mock the lesson fetcher to return predictable data
        mock_lessons = [
            {
                "subject": "自然",
                "title": "【1-1】植物的營養",
                "content": "植物營養的基本概念，包含光合作用與呼吸作用。"
            },
            {
                "subject": "國文", 
                "title": "【第一課】聲音鐘",
                "content": "透過聲音的節奏感受時間的流逝。"
            },
            {
                "subject": "歷史",
                "title": "【2-3】秦漢統一",
                "content": "秦始皇統一天下與漢朝的建立。"
            }
        ]
        
        # Mock fetch_lessons to return our test data
        original_fetch_lessons = orchestrator.lesson_fetcher.fetch_lessons
        orchestrator.lesson_fetcher.fetch_lessons = Mock(side_effect=[
            [mock_lessons[0]],  # 自然
            [mock_lessons[1]],  # 國文
            [mock_lessons[2]],  # 歷史
            [],  # 地理 (empty)
            []   # 公民 (empty)
        ])
        
        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            old_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Execute the complete system
                orchestrator.execute_daily_lesson_generation()
                
                # Verify output files were created
                assert os.path.exists("docs")
                
                today = datetime.now().strftime('%Y-%m-%d')
                html_file = f"docs/{today}.html"
                json_file = f"docs/{today}.json"
                
                assert os.path.exists(html_file)
                assert os.path.exists(json_file)
                
                # Verify HTML content
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Should contain one of our test lessons
                lesson_titles = [lesson["title"] for lesson in mock_lessons]
                assert any(title in html_content for title in lesson_titles)
                
                # Should contain proper HTML structure
                assert "<!DOCTYPE html>" in html_content
                assert "perplexity.ai" in html_content
                assert "lesson-image" in html_content or "image-placeholder" in html_content
                
                # Verify JSON content
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_content = f.read()
                
                json_data = json.loads(json_content)
                
                # Verify JSON structure
                assert "date" in json_data
                assert "lessons" in json_data
                assert "generated_at" in json_data
                assert json_data["date"] == today
                assert len(json_data["lessons"]) == 1
                
                # Verify the selected lesson
                selected_lesson = json_data["lessons"][0]
                assert "subject" in selected_lesson
                assert "title" in selected_lesson
                assert selected_lesson["title"] in lesson_titles
                
                # Should have mock image URL
                assert "image_url" in selected_lesson
                assert selected_lesson["image_url"].startswith("https://example.com/mock-images/")
                
            finally:
                os.chdir(old_cwd)
    
    @patch('lesson_service.webdriver.Chrome')
    @patch('lesson_service.BeautifulSoup')
    def test_lesson_fetching_integration(self, mock_soup, mock_chrome):
        """Test lesson fetching integration with mocked Selenium"""
        # Create orchestrator
        orchestrator = create_demo_orchestrator()
        
        # Mock webdriver and BeautifulSoup
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        # Mock beautiful soup to return test data
        mock_element = Mock()
        mock_element.get_text.return_value = "【1-1】測試課程標題"
        mock_soup.return_value.select.return_value = [mock_element]
        
        # Test fetching lessons
        subject_config = {
            'name': '自然',
            'url': 'https://www.learnmode.net/course/638520/content',
            'selector': 'h3.chapter-name'
        }
        
        lessons = orchestrator.lesson_fetcher.fetch_lessons(subject_config)
        
        # Verify selenium was called
        mock_chrome.assert_called_once()
        mock_driver.get.assert_called_once_with(subject_config['url'])
        mock_driver.quit.assert_called_once()
        
        # Verify lesson data
        assert isinstance(lessons, list)
        assert len(lessons) == 1
        assert lessons[0]['subject'] == '自然'
        assert lessons[0]['title'] == "【1-1】測試課程標題"
    
    def test_lesson_selection_algorithm(self):
        """Test that lesson selection algorithm works consistently"""
        orchestrator = create_demo_orchestrator()
        
        # Create test lessons
        lessons = [
            {"id": "1", "subject": "自然", "title": "課程1"},
            {"id": "2", "subject": "國文", "title": "課程2"},
            {"id": "3", "subject": "歷史", "title": "課程3"},
            {"id": "4", "subject": "地理", "title": "課程4"},
            {"id": "5", "subject": "公民", "title": "課程5"}
        ]
        
        # Multiple selections should be consistent
        selected1 = orchestrator.lesson_selector.select_daily_lesson(lessons)
        selected2 = orchestrator.lesson_selector.select_daily_lesson(lessons)
        selected3 = orchestrator.lesson_selector.select_daily_lesson(lessons)
        
        assert selected1 == selected2 == selected3
        assert selected1 in lessons
    
    def test_image_generation_integration(self):
        """Test image generation integration"""
        orchestrator = create_demo_orchestrator()
        
        lesson_data = {
            "subject": "自然",
            "title": "【1-1】植物的營養",
            "content": "植物營養的基本概念"
        }
        
        # Test image generation
        enhanced_lesson = orchestrator._enhance_lesson_with_image(lesson_data)
        
        # Should add image URL (mock generator)
        assert "image_url" in enhanced_lesson
        assert enhanced_lesson["image_url"].startswith("https://example.com/mock-images/")
        assert "image_generated_at" in enhanced_lesson
        
        # Original data should be preserved
        assert enhanced_lesson["subject"] == "自然"
        assert enhanced_lesson["title"] == "【1-1】植物的營養"
        assert enhanced_lesson["content"] == "植物營養的基本概念"
    
    def test_content_rendering_integration(self):
        """Test content rendering integration"""
        orchestrator = create_demo_orchestrator()
        
        lesson_data = {
            "subject": "國文",
            "title": "【第一課】聲音鐘",
            "image_url": "https://example.com/test-image.jpg"
        }
        
        date_str = "2024-01-01"
        
        # Test HTML rendering
        html_content = orchestrator.html_renderer.render(lesson_data, date_str)
        assert isinstance(html_content, str)
        assert "【第一課】聲音鐘" in html_content
        assert "國文" in html_content
        assert "https://example.com/test-image.jpg" in html_content
        
        # Test JSON rendering
        json_content = orchestrator.json_renderer.render(lesson_data, date_str)
        assert isinstance(json_content, str)
        
        json_data = json.loads(json_content)
        assert json_data["date"] == date_str
        assert json_data["lessons"][0]["title"] == "【第一課】聲音鐘"
    
    def test_error_recovery(self):
        """Test system error recovery"""
        orchestrator = create_demo_orchestrator()
        
        # Test with empty lesson list
        empty_lessons = []
        selected = orchestrator.lesson_selector.select_daily_lesson(empty_lessons)
        assert selected == {}
        
        # Test image generation with None result
        orchestrator.image_service.image_generator.generate_image = Mock(return_value=None)
        
        lesson_data = {"subject": "test", "title": "test", "content": "test"}
        enhanced = orchestrator._enhance_lesson_with_image(lesson_data)
        
        # Should not have image_url but should not fail
        assert "image_url" not in enhanced
        assert enhanced["subject"] == "test"
        assert enhanced["title"] == "test"
    
    def test_subject_filter_integration(self):
        """Test subject filter integration with real filter functions"""
        from lesson_service import SubjectFilter
        
        # Test real filter functions with various inputs
        test_cases = [
            ("自然", "【1-1】植物的營養", True),
            ("自然", "植物的營養", False),
            ("國文", "【第一課】聲音鐘", True),
            ("國文", "聲音鐘", False),
            ("歷史", "【2-3】秦漢統一", True),
            ("歷史", "秦漢統一", False),
            ("地理", "【3-5】氣候變化", True),
            ("地理", "氣候變化", False),
            ("公民", "【1-2】個人與社會", True),
            ("公民", "個人與社會", False),
        ]
        
        filter_map = {
            "自然": SubjectFilter.filter_nature,
            "國文": SubjectFilter.filter_chinese,
            "歷史": SubjectFilter.filter_history,
            "地理": SubjectFilter.filter_geography,
            "公民": SubjectFilter.filter_civics
        }
        
        for subject, title, expected in test_cases:
            filter_func = filter_map[subject]
            result = filter_func(title)
            assert result == expected, f"Failed for {subject}: {title}, expected {expected}, got {result}"


class TestSystemPerformance:
    """Test system performance and scalability"""
    
    def test_large_lesson_list_performance(self):
        """Test system performance with large lesson lists"""
        orchestrator = create_demo_orchestrator()
        
        # Create a large list of lessons
        large_lesson_list = [
            {"id": str(i), "subject": f"科目{i % 5}", "title": f"課程{i}"}
            for i in range(1000)
        ]
        
        # Test lesson selection performance
        import time
        start_time = time.time()
        
        selected = orchestrator.lesson_selector.select_daily_lesson(large_lesson_list)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete quickly (less than 1 second)
        assert execution_time < 1.0
        assert selected in large_lesson_list
    
    @pytest.mark.slow
    def test_batch_processing_performance(self):
        """Test batch processing performance"""
        orchestrator = create_demo_orchestrator()
        
        # Create multiple lessons for batch processing
        lessons = [
            {"id": str(i), "subject": "自然", "title": f"課程{i}", "content": f"內容{i}"}
            for i in range(10)
        ]
        
        # Test batch image generation
        import asyncio
        
        async def test_batch():
            start_time = time.time()
            results = await orchestrator.image_service.generate_batch_images(lessons)
            end_time = time.time()
            
            # Should complete reasonably quickly (with rate limiting)
            execution_time = end_time - start_time
            assert execution_time < 30.0  # With sleep(1) per item
            
            # Should process all lessons
            assert len(results) == len(lessons)
            
            return results
        
        import time
        results = asyncio.run(test_batch())
        
        # Verify all results
        for lesson in lessons:
            assert lesson["id"] in results
            assert results[lesson["id"]].startswith("https://example.com/mock-images/")


class TestSystemCompatibility:
    """Test system compatibility and backwards compatibility"""
    
    def test_output_format_compatibility(self):
        """Test that output formats are compatible with existing systems"""
        orchestrator = create_demo_orchestrator()
        
        lesson_data = {
            "subject": "自然",
            "title": "【1-1】植物的營養",
            "image_url": "https://example.com/image.jpg"
        }
        
        # Test HTML output format
        html_content = orchestrator.html_renderer.render(lesson_data, "2024-01-01")
        
        # Should be valid HTML
        assert html_content.startswith("<!DOCTYPE html>")
        assert html_content.endswith("</html>")
        assert "<html lang=\"zh-Hant\">" in html_content
        
        # Should contain expected elements for GitHub Pages
        assert "perplexity.ai" in html_content
        assert "countdown" in html_content
        
        # Test JSON output format
        json_content = orchestrator.json_renderer.render(lesson_data, "2024-01-01")
        
        # Should be valid JSON
        json_data = json.loads(json_content)
        assert isinstance(json_data, dict)
        
        # Should have expected structure
        assert "date" in json_data
        assert "lessons" in json_data
        assert "generated_at" in json_data
    
    def test_legacy_system_integration(self):
        """Test integration with legacy systems"""
        from content_renderer import LegacyHtmlRenderer
        
        legacy_renderer = LegacyHtmlRenderer()
        
        lesson_data = {
            "subject": "自然",
            "title": "【1-1】植物的營養"
        }
        
        legacy_html = legacy_renderer.render(lesson_data, "2024-01-01")
        
        # Should maintain legacy format
        assert "meta http-equiv=\"refresh\"" in legacy_html
        assert "content=\"0;url=" in legacy_html
        assert "如果沒有自動跳轉" in legacy_html
        
        # Should still work with Perplexity AI
        assert "perplexity.ai" in legacy_html