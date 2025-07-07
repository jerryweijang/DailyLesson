"""
Unit tests for interfaces module
"""
import pytest
from interfaces import LessonFetcher, ImageGenerator, ContentRenderer, LessonSelector


class TestLessonFetcher:
    """Test abstract LessonFetcher interface"""
    
    def test_lesson_fetcher_is_abstract(self):
        """Test that LessonFetcher cannot be instantiated directly"""
        with pytest.raises(TypeError):
            LessonFetcher()
    
    def test_lesson_fetcher_requires_fetch_lessons_method(self):
        """Test that concrete implementations must implement fetch_lessons"""
        class IncompleteLessonFetcher(LessonFetcher):
            pass
        
        with pytest.raises(TypeError):
            IncompleteLessonFetcher()


class TestImageGenerator:
    """Test abstract ImageGenerator interface"""
    
    def test_image_generator_is_abstract(self):
        """Test that ImageGenerator cannot be instantiated directly"""
        with pytest.raises(TypeError):
            ImageGenerator()
    
    def test_image_generator_requires_generate_image_method(self):
        """Test that concrete implementations must implement generate_image"""
        class IncompleteImageGenerator(ImageGenerator):
            pass
        
        with pytest.raises(TypeError):
            IncompleteImageGenerator()


class TestContentRenderer:
    """Test abstract ContentRenderer interface"""
    
    def test_content_renderer_is_abstract(self):
        """Test that ContentRenderer cannot be instantiated directly"""
        with pytest.raises(TypeError):
            ContentRenderer()
    
    def test_content_renderer_requires_render_method(self):
        """Test that concrete implementations must implement render"""
        class IncompleteContentRenderer(ContentRenderer):
            pass
        
        with pytest.raises(TypeError):
            IncompleteContentRenderer()


class TestLessonSelector:
    """Test abstract LessonSelector interface"""
    
    def test_lesson_selector_is_abstract(self):
        """Test that LessonSelector cannot be instantiated directly"""
        with pytest.raises(TypeError):
            LessonSelector()
    
    def test_lesson_selector_requires_select_daily_lesson_method(self):
        """Test that concrete implementations must implement select_daily_lesson"""
        class IncompleteLessonSelector(LessonSelector):
            pass
        
        with pytest.raises(TypeError):
            IncompleteLessonSelector()


class TestInterfaceImplementations:
    """Test that interfaces can be properly implemented"""
    
    def test_concrete_lesson_fetcher_implementation(self):
        """Test that LessonFetcher can be properly implemented"""
        class ConcreteLessonFetcher(LessonFetcher):
            def fetch_lessons(self, subject_config):
                return []
        
        # Should not raise an error
        fetcher = ConcreteLessonFetcher()
        assert fetcher.fetch_lessons({}) == []
    
    def test_concrete_image_generator_implementation(self):
        """Test that ImageGenerator can be properly implemented"""
        class ConcreteImageGenerator(ImageGenerator):
            def generate_image(self, subject, title, content):
                return "http://example.com/image.jpg"
        
        # Should not raise an error
        generator = ConcreteImageGenerator()
        assert generator.generate_image("test", "title", "content") == "http://example.com/image.jpg"
    
    def test_concrete_content_renderer_implementation(self):
        """Test that ContentRenderer can be properly implemented"""
        class ConcreteContentRenderer(ContentRenderer):
            def render(self, lesson_data, date_str):
                return "rendered content"
        
        # Should not raise an error
        renderer = ConcreteContentRenderer()
        assert renderer.render({}, "2024-01-01") == "rendered content"
    
    def test_concrete_lesson_selector_implementation(self):
        """Test that LessonSelector can be properly implemented"""
        class ConcreteLessonSelector(LessonSelector):
            def select_daily_lesson(self, lessons):
                return lessons[0] if lessons else {}
        
        # Should not raise an error
        selector = ConcreteLessonSelector()
        assert selector.select_daily_lesson([{"test": "lesson"}]) == {"test": "lesson"}
        assert selector.select_daily_lesson([]) == {}