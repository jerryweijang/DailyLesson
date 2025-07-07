"""
Unit tests for image_service module
"""
import pytest
from unittest.mock import Mock, patch
from image_service import MockImageGenerator, EducationalImageService, PromptGenerator


class TestMockImageGenerator:
    """Test MockImageGenerator implementation"""
    
    def test_mock_image_generator_initialization(self):
        """Test MockImageGenerator can be initialized"""
        generator = MockImageGenerator()
        assert generator is not None
    
    def test_mock_image_generator_generates_consistent_urls(self):
        """Test that MockImageGenerator generates consistent mock URLs"""
        generator = MockImageGenerator()
        
        # Same inputs should produce same output
        url1 = generator.generate_image("自然", "測試課程", "測試內容")
        url2 = generator.generate_image("自然", "測試課程", "測試內容")
        
        assert url1 == url2
        assert url1.startswith("https://example.com/mock-images/")
        assert "自然" in url1
        assert url1.endswith(".jpg")
    
    def test_mock_image_generator_different_inputs_different_urls(self):
        """Test that different inputs produce different URLs"""
        generator = MockImageGenerator()
        
        url1 = generator.generate_image("自然", "課程A", "內容A")
        url2 = generator.generate_image("國文", "課程B", "內容B")
        
        assert url1 != url2
        assert "自然" in url1
        assert "國文" in url2
    
    def test_mock_image_generator_handles_empty_inputs(self):
        """Test MockImageGenerator handles empty inputs gracefully"""
        generator = MockImageGenerator()
        
        url = generator.generate_image("", "", "")
        assert url is not None
        assert url.startswith("https://example.com/mock-images/")


class TestPromptGenerator:
    """Test PromptGenerator class"""
    
    def test_prompt_generator_initialization(self):
        """Test PromptGenerator can be initialized"""
        generator = PromptGenerator()
        assert generator is not None
        assert hasattr(generator, 'subject_styles')
        assert isinstance(generator.subject_styles, dict)
    
    def test_prompt_generator_has_all_subjects(self):
        """Test that PromptGenerator has styles for all subjects"""
        generator = PromptGenerator()
        expected_subjects = ["自然", "國文", "歷史", "地理", "公民"]
        
        for subject in expected_subjects:
            assert subject in generator.subject_styles
            assert isinstance(generator.subject_styles[subject], str)
            assert len(generator.subject_styles[subject]) > 0
    
    def test_create_educational_prompt_basic(self):
        """Test basic prompt creation"""
        generator = PromptGenerator()
        
        prompt = generator.create_educational_prompt("自然", "測試課程", "測試內容")
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        assert "自然" in prompt or "scientific" in prompt
    
    def test_create_educational_prompt_unknown_subject(self):
        """Test prompt creation with unknown subject"""
        generator = PromptGenerator()
        
        prompt = generator.create_educational_prompt("未知科目", "測試課程", "測試內容")
        
        assert isinstance(prompt, str)
        assert len(prompt) > 0


class TestEducationalImageService:
    """Test EducationalImageService class"""
    
    def test_educational_image_service_initialization(self):
        """Test EducationalImageService can be initialized with a generator"""
        mock_generator = Mock()
        service = EducationalImageService(mock_generator)
        
        assert service.image_generator is mock_generator
    
    def test_generate_lesson_image_calls_generator(self):
        """Test that generate_lesson_image calls the underlying generator"""
        mock_generator = Mock()
        mock_generator.generate_image.return_value = "http://example.com/image.jpg"
        
        service = EducationalImageService(mock_generator)
        result = service.generate_lesson_image("自然", "測試課程", "測試內容")
        
        mock_generator.generate_image.assert_called_once_with("自然", "測試課程", "測試內容")
        assert result == "http://example.com/image.jpg"
    
    def test_generate_lesson_image_handles_none_return(self):
        """Test that generate_lesson_image handles None return from generator"""
        mock_generator = Mock()
        mock_generator.generate_image.return_value = None
        
        service = EducationalImageService(mock_generator)
        result = service.generate_lesson_image("自然", "測試課程", "測試內容")
        
        assert result is None
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    @patch('asyncio.sleep')
    async def test_generate_batch_images_basic(self, mock_sleep):
        """Test basic batch image generation"""
        mock_generator = Mock()
        mock_generator.generate_image.return_value = "http://example.com/image.jpg"
        
        service = EducationalImageService(mock_generator)
        
        lessons = [
            {"id": "1", "subject": "自然", "title": "課程1", "content": "內容1"},
            {"id": "2", "subject": "國文", "title": "課程2", "content": "內容2"}
        ]
        
        results = await service.generate_batch_images(lessons)
        
        assert len(results) == 2
        assert "1" in results
        assert "2" in results
        assert results["1"] == "http://example.com/image.jpg"
        assert results["2"] == "http://example.com/image.jpg"
        
        # Verify sleep was called for rate limiting
        assert mock_sleep.call_count == 2
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    @patch('asyncio.sleep')
    async def test_generate_batch_images_with_failures(self, mock_sleep):
        """Test batch image generation with some failures"""
        mock_generator = Mock()
        mock_generator.generate_image.side_effect = [
            "http://example.com/image1.jpg",
            Exception("API Error"),
            "http://example.com/image2.jpg"
        ]
        
        service = EducationalImageService(mock_generator)
        
        lessons = [
            {"id": "1", "subject": "自然", "title": "課程1", "content": "內容1"},
            {"id": "2", "subject": "國文", "title": "課程2", "content": "內容2"},
            {"id": "3", "subject": "歷史", "title": "課程3", "content": "內容3"}
        ]
        
        results = await service.generate_batch_images(lessons)
        
        # Should only have results for successful generations
        assert len(results) == 2
        assert "1" in results
        assert "2" not in results  # Failed due to exception
        assert "3" in results
    
    @pytest.mark.asyncio
    @pytest.mark.slow
    @patch('asyncio.sleep')
    async def test_generate_batch_images_empty_list(self, mock_sleep):
        """Test batch image generation with empty lesson list"""
        mock_generator = Mock()
        service = EducationalImageService(mock_generator)
        
        results = await service.generate_batch_images([])
        
        assert results == {}
        mock_sleep.assert_not_called()
        mock_generator.generate_image.assert_not_called()


class TestImageServiceIntegration:
    """Integration tests for image service components"""
    
    def test_educational_image_service_with_mock_generator(self):
        """Test EducationalImageService integration with MockImageGenerator"""
        generator = MockImageGenerator()
        service = EducationalImageService(generator)
        
        result = service.generate_lesson_image("自然", "測試課程", "測試內容")
        
        assert result is not None
        assert result.startswith("https://example.com/mock-images/")
        assert result.endswith(".jpg")
    
    def test_educational_image_service_with_different_subjects(self):
        """Test service with different subjects"""
        generator = MockImageGenerator()
        service = EducationalImageService(generator)
        
        subjects = ["自然", "國文", "歷史", "地理", "公民"]
        results = []
        
        for subject in subjects:
            result = service.generate_lesson_image(subject, f"{subject}課程", f"{subject}內容")
            results.append(result)
        
        # All should be successful
        assert all(result is not None for result in results)
        
        # All should be different URLs
        assert len(set(results)) == len(results)