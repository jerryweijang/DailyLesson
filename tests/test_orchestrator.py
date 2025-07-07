"""
Unit tests for orchestrator module
"""
import pytest
import os
import tempfile
from unittest.mock import Mock, patch, MagicMock
from orchestrator import DailyLessonOrchestrator, create_production_orchestrator, create_demo_orchestrator
from datetime import datetime


class TestDailyLessonOrchestrator:
    """Test DailyLessonOrchestrator class"""
    
    def test_orchestrator_initialization(self):
        """Test DailyLessonOrchestrator can be initialized with all dependencies"""
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        assert orchestrator.lesson_fetcher is lesson_fetcher
        assert orchestrator.lesson_selector is lesson_selector
        assert orchestrator.html_renderer is html_renderer
        assert orchestrator.json_renderer is json_renderer
        assert orchestrator.image_service is not None
    
    def test_orchestrator_has_subject_configurations(self):
        """Test that orchestrator has proper subject configurations"""
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        assert hasattr(orchestrator, 'subjects')
        assert isinstance(orchestrator.subjects, list)
        assert len(orchestrator.subjects) == 5  # 五個科目
        
        expected_subjects = ['自然', '國文', '歷史', '地理', '公民']
        actual_subjects = [s['name'] for s in orchestrator.subjects]
        
        for expected in expected_subjects:
            assert expected in actual_subjects
    
    def test_orchestrator_subject_configurations_structure(self):
        """Test that subject configurations have proper structure"""
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        for subject in orchestrator.subjects:
            assert 'name' in subject
            assert 'url' in subject
            assert 'selector' in subject
            assert isinstance(subject['name'], str)
            assert isinstance(subject['url'], str)
            assert isinstance(subject['selector'], str)
            assert subject['url'].startswith('https://www.learnmode.net')
    
    @patch('orchestrator.time.sleep')
    def test_fetch_all_lessons(self, mock_sleep):
        """Test _fetch_all_lessons method"""
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        # Mock lesson fetcher to return lessons
        lesson_fetcher.fetch_lessons.side_effect = [
            [{"subject": "自然", "title": "【1-1】植物"}],
            [{"subject": "國文", "title": "【第一課】聲音鐘"}],
            [{"subject": "歷史", "title": "【2-3】秦漢"}],
            [{"subject": "地理", "title": "【3-5】氣候"}],
            [{"subject": "公民", "title": "【1-2】個人"}]
        ]
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        lessons = orchestrator._fetch_all_lessons()
        
        # Should call fetch_lessons for each subject
        assert lesson_fetcher.fetch_lessons.call_count == 5
        
        # Should return all lessons
        assert len(lessons) == 5
        assert any(lesson['subject'] == '自然' for lesson in lessons)
        assert any(lesson['subject'] == '國文' for lesson in lessons)
        assert any(lesson['subject'] == '歷史' for lesson in lessons)
        assert any(lesson['subject'] == '地理' for lesson in lessons)
        assert any(lesson['subject'] == '公民' for lesson in lessons)
        
        # Should sleep between requests
        assert mock_sleep.call_count == 5
    
    def test_enhance_lesson_with_image(self):
        """Test _enhance_lesson_with_image method"""
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        # Mock image generator
        image_generator.generate_image.return_value = "https://example.com/image.jpg"
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        lesson_data = {
            "subject": "自然",
            "title": "【1-1】植物的營養",
            "content": "課程內容"
        }
        
        enhanced_lesson = orchestrator._enhance_lesson_with_image(lesson_data)
        
        # Should call image generator
        image_generator.generate_image.assert_called_once_with(
            "自然", "【1-1】植物的營養", "課程內容"
        )
        
        # Should add image_url to lesson data
        assert "image_url" in enhanced_lesson
        assert enhanced_lesson["image_url"] == "https://example.com/image.jpg"
        assert "image_generated_at" in enhanced_lesson
    
    def test_enhance_lesson_with_image_failure(self):
        """Test _enhance_lesson_with_image when image generation fails"""
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        # Mock image generator to return None
        image_generator.generate_image.return_value = None
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        lesson_data = {
            "subject": "自然",
            "title": "【1-1】植物的營養",
            "content": "課程內容"
        }
        
        enhanced_lesson = orchestrator._enhance_lesson_with_image(lesson_data)
        
        # Should not add image_url if generation fails
        assert "image_url" not in enhanced_lesson
        assert "image_generated_at" not in enhanced_lesson
    
    @patch('orchestrator.os.makedirs')
    @patch('builtins.open', new_callable=MagicMock)
    def test_save_lesson_content(self, mock_open, mock_makedirs):
        """Test _save_lesson_content method"""
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        # Mock renderers
        html_renderer.render.return_value = "<html>test</html>"
        json_renderer.render.return_value = '{"test": "data"}'
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        lesson_data = {
            "subject": "自然",
            "title": "【1-1】植物的營養",
            "image_url": "https://example.com/image.jpg"
        }
        
        orchestrator._save_lesson_content(lesson_data, "2024-01-01")
        
        # Should create docs directory
        mock_makedirs.assert_called_once_with('docs', exist_ok=True)
        
        # Should call both renderers
        html_renderer.render.assert_called_once_with(lesson_data, "2024-01-01")
        json_renderer.render.assert_called_once_with(lesson_data, "2024-01-01")
        
        # Should open and write both files
        assert mock_open.call_count == 2
        mock_open.assert_any_call("docs/2024-01-01.html", 'w', encoding='utf-8')
        mock_open.assert_any_call("docs/2024-01-01.json", 'w', encoding='utf-8')
    
    @patch('orchestrator.os.makedirs')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('orchestrator.time.sleep')
    def test_execute_daily_lesson_generation_full_flow(self, mock_sleep, mock_open, mock_makedirs):
        """Test complete execute_daily_lesson_generation flow"""
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        # Mock all dependencies
        lesson_fetcher.fetch_lessons.return_value = [
            {"subject": "自然", "title": "【1-1】植物的營養"}
        ]
        lesson_selector.select_daily_lesson.return_value = {
            "subject": "自然", "title": "【1-1】植物的營養"
        }
        image_generator.generate_image.return_value = "https://example.com/image.jpg"
        html_renderer.render.return_value = "<html>test</html>"
        json_renderer.render.return_value = '{"test": "data"}'
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        # Execute the full flow
        orchestrator.execute_daily_lesson_generation()
        
        # Should fetch lessons from all subjects
        assert lesson_fetcher.fetch_lessons.call_count == 5
        
        # Should select a daily lesson
        lesson_selector.select_daily_lesson.assert_called_once()
        
        # Should generate image
        image_generator.generate_image.assert_called_once()
        
        # Should render content
        html_renderer.render.assert_called_once()
        json_renderer.render.assert_called_once()
        
        # Should save files
        mock_makedirs.assert_called_once()
        assert mock_open.call_count == 2
    
    @patch('orchestrator.time.sleep')
    def test_execute_daily_lesson_generation_no_lessons(self, mock_sleep):
        """Test execute_daily_lesson_generation when no lessons are found"""
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        # Mock to return no lessons
        lesson_fetcher.fetch_lessons.return_value = []
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        # Should not raise error, just return early
        orchestrator.execute_daily_lesson_generation()
        
        # Should not call lesson selector if no lessons
        lesson_selector.select_daily_lesson.assert_not_called()
        
        # Should not call image generator
        image_generator.generate_image.assert_not_called()
        
        # Should not call renderers
        html_renderer.render.assert_not_called()
        json_renderer.render.assert_not_called()


class TestOrchestratorFactoryFunctions:
    """Test orchestrator factory functions"""
    
    @patch('orchestrator.os.environ.get')
    def test_create_production_orchestrator_with_token(self, mock_get):
        """Test create_production_orchestrator with GitHub token"""
        mock_get.return_value = "test-token"
        
        orchestrator = create_production_orchestrator()
        
        assert orchestrator is not None
        assert hasattr(orchestrator, 'lesson_fetcher')
        assert hasattr(orchestrator, 'lesson_selector')
        assert hasattr(orchestrator, 'image_service')
        assert hasattr(orchestrator, 'html_renderer')
        assert hasattr(orchestrator, 'json_renderer')
    
    @patch('orchestrator.os.environ.get')
    @patch('orchestrator.logging.warning')
    def test_create_production_orchestrator_without_token(self, mock_warning, mock_get):
        """Test create_production_orchestrator without GitHub token"""
        mock_get.return_value = None
        
        orchestrator = create_production_orchestrator()
        
        assert orchestrator is not None
        
        # Should log warning about using mock generator
        mock_warning.assert_called_once_with(
            "No GITHUB_TOKEN found, using mock image generator"
        )
    
    def test_create_demo_orchestrator(self):
        """Test create_demo_orchestrator"""
        orchestrator = create_demo_orchestrator()
        
        assert orchestrator is not None
        assert hasattr(orchestrator, 'lesson_fetcher')
        assert hasattr(orchestrator, 'lesson_selector')
        assert hasattr(orchestrator, 'image_service')
        assert hasattr(orchestrator, 'html_renderer')
        assert hasattr(orchestrator, 'json_renderer')
    
    def test_factory_functions_return_different_instances(self):
        """Test that factory functions return different instances"""
        demo1 = create_demo_orchestrator()
        demo2 = create_demo_orchestrator()
        
        assert demo1 is not demo2
        assert demo1.lesson_fetcher is not demo2.lesson_fetcher
    
    @patch('orchestrator.os.environ.get')
    def test_factory_functions_use_correct_components(self, mock_get):
        """Test that factory functions use the correct components"""
        mock_get.return_value = "test-token"
        
        production = create_production_orchestrator()
        demo = create_demo_orchestrator()
        
        # Both should have the same types of components
        assert type(production.lesson_fetcher).__name__ == 'SeleniumLessonFetcher'
        assert type(demo.lesson_fetcher).__name__ == 'SeleniumLessonFetcher'
        
        assert type(production.lesson_selector).__name__ == 'DayBasedLessonSelector'
        assert type(demo.lesson_selector).__name__ == 'DayBasedLessonSelector'
        
        assert type(production.html_renderer).__name__ == 'EnhancedHtmlRenderer'
        assert type(demo.html_renderer).__name__ == 'EnhancedHtmlRenderer'
        
        assert type(production.json_renderer).__name__ == 'JsonRenderer'
        assert type(demo.json_renderer).__name__ == 'JsonRenderer'


class TestOrchestratorIntegration:
    """Integration tests for orchestrator components"""
    
    def test_orchestrator_integration_with_mocks(self):
        """Test orchestrator integration with all mocked components"""
        # Create a complete orchestrator with mocks
        orchestrator = create_demo_orchestrator()
        
        # Mock the lesson fetcher to return actual data
        orchestrator.lesson_fetcher.fetch_lessons = Mock(return_value=[
            {"subject": "自然", "title": "【1-1】植物的營養", "content": "植物營養的基本概念"}
        ])
        
        # Mock the lesson selector
        orchestrator.lesson_selector.select_daily_lesson = Mock(return_value={
            "subject": "自然", "title": "【1-1】植物的營養", "content": "植物營養的基本概念"
        })
        
        # Create a temporary directory for output
        with tempfile.TemporaryDirectory() as temp_dir:
            # Change to temp directory
            old_cwd = os.getcwd()
            os.chdir(temp_dir)
            
            try:
                # Execute the orchestrator
                orchestrator.execute_daily_lesson_generation()
                
                # Check that files were created
                assert os.path.exists("docs")
                
                # Check that HTML and JSON files exist
                today = datetime.now().strftime('%Y-%m-%d')
                html_file = f"docs/{today}.html"
                json_file = f"docs/{today}.json"
                
                assert os.path.exists(html_file)
                assert os.path.exists(json_file)
                
                # Check file contents
                with open(html_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                    assert "【1-1】植物的營養" in html_content
                    assert "自然" in html_content
                
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_content = f.read()
                    assert "【1-1】植物的營養" in json_content
                    assert "自然" in json_content
                    
            finally:
                os.chdir(old_cwd)
    
    def test_orchestrator_error_handling(self):
        """Test orchestrator error handling"""
        # Create orchestrator with failing components
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        # Make lesson fetcher fail
        lesson_fetcher.fetch_lessons.side_effect = Exception("Network error")
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        # Should raise exception
        with pytest.raises(Exception):
            orchestrator.execute_daily_lesson_generation()
    
    def test_orchestrator_partial_failures(self):
        """Test orchestrator with partial failures"""
        lesson_fetcher = Mock()
        lesson_selector = Mock()
        image_generator = Mock()
        html_renderer = Mock()
        json_renderer = Mock()
        
        # Some subjects fail, some succeed
        lesson_fetcher.fetch_lessons.side_effect = [
            [{"subject": "自然", "title": "【1-1】植物"}],  # Success
            Exception("Network error"),  # Fail
            [{"subject": "歷史", "title": "【2-3】秦漢"}],  # Success
            Exception("Network error"),  # Fail
            [{"subject": "公民", "title": "【1-2】個人"}]   # Success
        ]
        
        lesson_selector.select_daily_lesson.return_value = {
            "subject": "自然", "title": "【1-1】植物"
        }
        
        image_generator.generate_image.return_value = "https://example.com/image.jpg"
        html_renderer.render.return_value = "<html>test</html>"
        json_renderer.render.return_value = '{"test": "data"}'
        
        orchestrator = DailyLessonOrchestrator(
            lesson_fetcher=lesson_fetcher,
            lesson_selector=lesson_selector,
            image_generator=image_generator,
            html_renderer=html_renderer,
            json_renderer=json_renderer
        )
        
        # Should handle partial failures gracefully
        # This will depend on the actual implementation
        # For now, we expect it to fail on the first exception
        with pytest.raises(Exception):
            orchestrator.execute_daily_lesson_generation()