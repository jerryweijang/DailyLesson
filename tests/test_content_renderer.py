"""
Unit tests for content_renderer module
"""
import pytest
import json
import urllib.parse
from content_renderer import EnhancedHtmlRenderer, JsonRenderer, LegacyHtmlRenderer
from datetime import datetime


class TestEnhancedHtmlRenderer:
    """Test EnhancedHtmlRenderer class"""
    
    def test_enhanced_html_renderer_initialization(self):
        """Test EnhancedHtmlRenderer can be initialized"""
        renderer = EnhancedHtmlRenderer()
        assert renderer is not None
    
    def test_render_with_image_url(self):
        """Test rendering with image URL"""
        renderer = EnhancedHtmlRenderer()
        
        lesson_data = {
            "title": "【1-1】植物的營養",
            "subject": "自然",
            "image_url": "https://example.com/image.jpg"
        }
        
        html = renderer.render(lesson_data, "2024-01-01")
        
        assert isinstance(html, str)
        assert "【1-1】植物的營養" in html
        assert "自然" in html
        assert "https://example.com/image.jpg" in html
        assert "img src=" in html
        assert "lesson-image" in html
        assert "perplexity.ai" in html
    
    def test_render_without_image_url(self):
        """Test rendering without image URL"""
        renderer = EnhancedHtmlRenderer()
        
        lesson_data = {
            "title": "【第一課】聲音鐘",
            "subject": "國文"
        }
        
        html = renderer.render(lesson_data, "2024-01-01")
        
        assert isinstance(html, str)
        assert "【第一課】聲音鐘" in html
        assert "國文" in html
        assert "image-placeholder" in html
        assert "課程圖像生成中..." in html
        assert "perplexity.ai" in html
    
    def test_render_html_structure(self):
        """Test that rendered HTML has proper structure"""
        renderer = EnhancedHtmlRenderer()
        
        lesson_data = {
            "title": "測試課程",
            "subject": "測試科目",
            "image_url": "https://example.com/test.jpg"
        }
        
        html = renderer.render(lesson_data, "2024-01-01")
        
        # Check HTML structure
        assert "<!DOCTYPE html>" in html
        assert "<html lang=\"zh-Hant\">" in html
        assert "<head>" in html
        assert "<body>" in html
        assert "</html>" in html
        
        # Check meta tags
        assert "<meta charset=\"utf-8\">" in html
        assert "viewport" in html
        
        # Check CSS classes
        assert "container" in html
        assert "countdown" in html
        assert "manual-link" in html
        
        # Check JavaScript
        assert "script" in html
        assert "countdown" in html
        assert "setInterval" in html
    
    def test_render_perplexity_link_encoding(self):
        """Test that Perplexity link is properly URL encoded"""
        renderer = EnhancedHtmlRenderer()
        
        lesson_data = {
            "title": "測試課程【特殊字元】",
            "subject": "測試科目"
        }
        
        html = renderer.render(lesson_data, "2024-01-01")
        
        # Check that the link is properly encoded
        assert "perplexity.ai/search?q=" in html
        assert "%E6%B8%AC%E8%A9%A6" in html  # "測試" URL encoded
    
    def test_generate_image_html_with_url(self):
        """Test _generate_image_html with URL"""
        renderer = EnhancedHtmlRenderer()
        
        image_html = renderer._generate_image_html("https://example.com/image.jpg")
        
        assert "<img src=" in image_html
        assert "https://example.com/image.jpg" in image_html
        assert "lesson-image" in image_html
        assert "onerror" in image_html
    
    def test_generate_image_html_without_url(self):
        """Test _generate_image_html without URL"""
        renderer = EnhancedHtmlRenderer()
        
        image_html = renderer._generate_image_html(None)
        
        assert "<div class=\"image-placeholder\">" in image_html
        assert "課程圖像生成中..." in image_html
        
        # Test with empty string
        image_html_empty = renderer._generate_image_html("")
        assert "<div class=\"image-placeholder\">" in image_html_empty


class TestJsonRenderer:
    """Test JsonRenderer class"""
    
    def test_json_renderer_initialization(self):
        """Test JsonRenderer can be initialized"""
        renderer = JsonRenderer()
        assert renderer is not None
    
    def test_render_basic_lesson_data(self):
        """Test rendering basic lesson data to JSON"""
        renderer = JsonRenderer()
        
        lesson_data = {
            "title": "【1-1】植物的營養",
            "subject": "自然",
            "image_url": "https://example.com/image.jpg"
        }
        
        json_str = renderer.render(lesson_data, "2024-01-01")
        
        assert isinstance(json_str, str)
        
        # Parse the JSON to verify structure
        data = json.loads(json_str)
        
        assert "date" in data
        assert "lessons" in data
        assert "generated_at" in data
        
        assert data["date"] == "2024-01-01"
        assert isinstance(data["lessons"], list)
        assert len(data["lessons"]) == 1
        assert data["lessons"][0] == lesson_data
    
    def test_render_lesson_data_without_image(self):
        """Test rendering lesson data without image to JSON"""
        renderer = JsonRenderer()
        
        lesson_data = {
            "title": "【第一課】聲音鐘",
            "subject": "國文"
        }
        
        json_str = renderer.render(lesson_data, "2024-02-01")
        
        data = json.loads(json_str)
        
        assert data["date"] == "2024-02-01"
        assert data["lessons"][0]["title"] == "【第一課】聲音鐘"
        assert data["lessons"][0]["subject"] == "國文"
        assert "image_url" not in data["lessons"][0]
    
    def test_render_json_format(self):
        """Test that JSON is properly formatted"""
        renderer = JsonRenderer()
        
        lesson_data = {
            "title": "測試課程",
            "subject": "測試科目"
        }
        
        json_str = renderer.render(lesson_data, "2024-01-01")
        
        # Check that JSON is formatted with indentation
        assert "  " in json_str  # Indentation
        assert "\n" in json_str  # Line breaks
        
        # Check that Chinese characters are not escaped
        assert "測試課程" in json_str
        assert "測試科目" in json_str
    
    def test_render_generated_at_timestamp(self):
        """Test that generated_at timestamp is valid"""
        renderer = JsonRenderer()
        
        lesson_data = {"title": "測試", "subject": "測試"}
        
        json_str = renderer.render(lesson_data, "2024-01-01")
        data = json.loads(json_str)
        
        # Check that generated_at is a valid ISO timestamp
        generated_at = data["generated_at"]
        assert isinstance(generated_at, str)
        
        # Should be able to parse as datetime
        parsed_time = datetime.fromisoformat(generated_at)
        assert isinstance(parsed_time, datetime)


class TestLegacyHtmlRenderer:
    """Test LegacyHtmlRenderer class"""
    
    def test_legacy_html_renderer_initialization(self):
        """Test LegacyHtmlRenderer can be initialized"""
        renderer = LegacyHtmlRenderer()
        assert renderer is not None
    
    def test_render_legacy_format(self):
        """Test rendering in legacy HTML format"""
        renderer = LegacyHtmlRenderer()
        
        lesson_data = {
            "title": "【1-1】植物的營養",
            "subject": "自然",
            "image_url": "https://example.com/image.jpg"
        }
        
        html = renderer.render(lesson_data, "2024-01-01")
        
        assert isinstance(html, str)
        assert "【1-1】植物的營養" in html
        assert "<!DOCTYPE html>" in html
        assert "<html lang=\"zh-Hant\">" in html
        assert "meta http-equiv=\"refresh\"" in html
        assert "perplexity.ai" in html
    
    def test_render_legacy_redirect(self):
        """Test that legacy renderer creates proper redirect"""
        renderer = LegacyHtmlRenderer()
        
        lesson_data = {
            "title": "測試課程",
            "subject": "測試科目"
        }
        
        html = renderer.render(lesson_data, "2024-01-01")
        
        # Check for meta refresh tag
        assert "meta http-equiv=\"refresh\"" in html
        assert "content=\"0;url=" in html
        
        # Check for fallback link
        assert "如果沒有自動跳轉" in html
        assert "href=" in html
    
    def test_render_legacy_url_encoding(self):
        """Test that legacy renderer properly encodes URLs"""
        renderer = LegacyHtmlRenderer()
        
        lesson_data = {
            "title": "測試課程【特殊字元】",
            "subject": "測試科目"
        }
        
        html = renderer.render(lesson_data, "2024-01-01")
        
        # Check that the URL is properly encoded
        assert "perplexity.ai/search?q=" in html
        assert "%E6%B8%AC%E8%A9%A6" in html  # "測試" URL encoded
    
    def test_render_legacy_minimal_structure(self):
        """Test that legacy renderer has minimal HTML structure"""
        renderer = LegacyHtmlRenderer()
        
        lesson_data = {"title": "簡單課程", "subject": "簡單科目"}
        
        html = renderer.render(lesson_data, "2024-01-01")
        
        # Check basic HTML structure
        assert "<!DOCTYPE html>" in html
        assert "<head>" in html
        assert "<body>" in html
        assert "</html>" in html
        
        # Check that it's simpler than EnhancedHtmlRenderer
        assert "container" not in html
        assert "countdown" not in html
        assert "script" not in html


class TestContentRenderersIntegration:
    """Integration tests for content renderers"""
    
    def test_all_renderers_with_same_data(self):
        """Test all renderers with the same lesson data"""
        lesson_data = {
            "title": "【1-1】植物的營養",
            "subject": "自然",
            "image_url": "https://example.com/image.jpg"
        }
        
        date_str = "2024-01-01"
        
        enhanced_renderer = EnhancedHtmlRenderer()
        json_renderer = JsonRenderer()
        legacy_renderer = LegacyHtmlRenderer()
        
        enhanced_html = enhanced_renderer.render(lesson_data, date_str)
        json_str = json_renderer.render(lesson_data, date_str)
        legacy_html = legacy_renderer.render(lesson_data, date_str)
        
        # All should return strings
        assert isinstance(enhanced_html, str)
        assert isinstance(json_str, str)
        assert isinstance(legacy_html, str)
        
        # All should contain the lesson title
        assert "【1-1】植物的營養" in enhanced_html
        assert "【1-1】植物的營養" in json_str
        assert "【1-1】植物的營養" in legacy_html
        
        # Enhanced should be longer (more features)
        assert len(enhanced_html) > len(legacy_html)
        
        # JSON should be parseable
        json_data = json.loads(json_str)
        assert json_data["lessons"][0]["title"] == "【1-1】植物的營養"
    
    def test_renderers_with_missing_data(self):
        """Test all renderers with minimal lesson data"""
        lesson_data = {
            "title": "簡單課程",
            "subject": "簡單科目"
        }
        
        date_str = "2024-01-01"
        
        enhanced_renderer = EnhancedHtmlRenderer()
        json_renderer = JsonRenderer()
        legacy_renderer = LegacyHtmlRenderer()
        
        # Should not raise errors with minimal data
        enhanced_html = enhanced_renderer.render(lesson_data, date_str)
        json_str = json_renderer.render(lesson_data, date_str)
        legacy_html = legacy_renderer.render(lesson_data, date_str)
        
        # All should still work
        assert "簡單課程" in enhanced_html
        assert "簡單課程" in json_str
        assert "簡單課程" in legacy_html
    
    def test_url_encoding_consistency(self):
        """Test that URL encoding is consistent across HTML renderers"""
        lesson_data = {
            "title": "測試課程【特殊字元】？！",
            "subject": "測試科目"
        }
        
        enhanced_renderer = EnhancedHtmlRenderer()
        legacy_renderer = LegacyHtmlRenderer()
        
        enhanced_html = enhanced_renderer.render(lesson_data, "2024-01-01")
        legacy_html = legacy_renderer.render(lesson_data, "2024-01-01")
        
        # Both should contain properly encoded URLs
        assert "perplexity.ai/search?q=" in enhanced_html
        assert "perplexity.ai/search?q=" in legacy_html
        
        # Should contain URL encoded Chinese characters
        assert "%E6%B8%AC%E8%A9%A6" in enhanced_html
        assert "%E6%B8%AC%E8%A9%A6" in legacy_html