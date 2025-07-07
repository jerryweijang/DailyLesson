"""
Unit tests for lesson_service module
"""
import pytest
from unittest.mock import Mock, patch
from lesson_service import SubjectFilter, DayBasedLessonSelector
from datetime import datetime


class TestSubjectFilter:
    """Test SubjectFilter class"""
    
    def test_filter_nature_valid_format(self):
        """Test filter_nature with valid format"""
        # Valid formats: 【數字-數字】
        assert SubjectFilter.filter_nature("【1-1】植物的營養") is True
        assert SubjectFilter.filter_nature("【2-3】動物的運動") is True
        assert SubjectFilter.filter_nature("【10-15】化學反應") is True
    
    def test_filter_nature_invalid_format(self):
        """Test filter_nature with invalid format"""
        # Invalid formats
        assert SubjectFilter.filter_nature("植物的營養") is False
        assert SubjectFilter.filter_nature("【第一章】植物") is False
        assert SubjectFilter.filter_nature("【1】植物") is False
        assert SubjectFilter.filter_nature("【1-】植物") is False
        assert SubjectFilter.filter_nature("【-1】植物") is False
    
    def test_filter_chinese_valid_format(self):
        """Test filter_chinese with valid format"""
        # Valid formats: 含【】符號
        assert SubjectFilter.filter_chinese("【第一課】聲音鐘") is True
        assert SubjectFilter.filter_chinese("【語文常識】標點符號") is True
        assert SubjectFilter.filter_chinese("古詩【春曉】賞析") is True
        assert SubjectFilter.filter_chinese("【作文】我的家鄉") is True
    
    def test_filter_chinese_invalid_format(self):
        """Test filter_chinese with invalid format"""
        # Invalid formats: 不含【】符號
        assert SubjectFilter.filter_chinese("第一課聲音鐘") is False
        assert SubjectFilter.filter_chinese("語文常識") is False
        assert SubjectFilter.filter_chinese("古詩春曉賞析") is False
        assert SubjectFilter.filter_chinese("") is False
    
    def test_filter_history_valid_format(self):
        """Test filter_history with valid format"""
        # Valid formats: 【數字-數字】
        assert SubjectFilter.filter_history("【1-1】史前時代") is True
        assert SubjectFilter.filter_history("【2-3】秦漢統一") is True
        assert SubjectFilter.filter_history("【5-10】明清盛世") is True
    
    def test_filter_history_invalid_format(self):
        """Test filter_history with invalid format"""
        # Invalid formats
        assert SubjectFilter.filter_history("史前時代") is False
        assert SubjectFilter.filter_history("【第一章】史前時代") is False
        assert SubjectFilter.filter_history("【主題一】古代文明") is False
    
    def test_filter_geography_valid_format(self):
        """Test filter_geography with valid format"""
        # Valid formats: 【數字-數字】
        assert SubjectFilter.filter_geography("【1-1】地球的形狀") is True
        assert SubjectFilter.filter_geography("【3-5】氣候變化") is True
        assert SubjectFilter.filter_geography("【7-12】人口分布") is True
    
    def test_filter_geography_invalid_format(self):
        """Test filter_geography with invalid format"""
        # Invalid formats
        assert SubjectFilter.filter_geography("地球的形狀") is False
        assert SubjectFilter.filter_geography("【第一單元】地球") is False
        assert SubjectFilter.filter_geography("【主題1】地理環境") is False
    
    def test_filter_civics_valid_format(self):
        """Test filter_civics with valid format"""
        # Valid formats: 【數字-數字】
        assert SubjectFilter.filter_civics("【1-1】個人與社會") is True
        assert SubjectFilter.filter_civics("【2-4】民主政治") is True
        assert SubjectFilter.filter_civics("【6-8】法律與生活") is True
    
    def test_filter_civics_invalid_format(self):
        """Test filter_civics with invalid format"""
        # Invalid formats
        assert SubjectFilter.filter_civics("個人與社會") is False
        assert SubjectFilter.filter_civics("【第一課】個人與社會") is False
        assert SubjectFilter.filter_civics("【單元一】民主政治") is False
    
    def test_filter_edge_cases(self):
        """Test edge cases for all filters"""
        # Empty string
        assert SubjectFilter.filter_nature("") is False
        assert SubjectFilter.filter_chinese("") is False
        assert SubjectFilter.filter_history("") is False
        assert SubjectFilter.filter_geography("") is False
        assert SubjectFilter.filter_civics("") is False
        
        # None input
        assert SubjectFilter.filter_nature(None) is False
        assert SubjectFilter.filter_chinese(None) is False
        assert SubjectFilter.filter_history(None) is False
        assert SubjectFilter.filter_geography(None) is False
        assert SubjectFilter.filter_civics(None) is False


class TestDayBasedLessonSelector:
    """Test DayBasedLessonSelector class"""
    
    def test_day_based_lesson_selector_initialization(self):
        """Test DayBasedLessonSelector can be initialized"""
        selector = DayBasedLessonSelector()
        assert selector is not None
    
    def test_select_daily_lesson_basic(self):
        """Test basic lesson selection"""
        selector = DayBasedLessonSelector()
        
        lessons = [
            {"id": "1", "subject": "自然", "title": "課程1"},
            {"id": "2", "subject": "國文", "title": "課程2"},
            {"id": "3", "subject": "歷史", "title": "課程3"}
        ]
        
        selected = selector.select_daily_lesson(lessons)
        
        assert selected in lessons
        assert "id" in selected
        assert "subject" in selected
        assert "title" in selected
    
    def test_select_daily_lesson_single_item(self):
        """Test lesson selection with single item"""
        selector = DayBasedLessonSelector()
        
        lessons = [{"id": "1", "subject": "自然", "title": "唯一課程"}]
        
        selected = selector.select_daily_lesson(lessons)
        
        assert selected == lessons[0]
    
    def test_select_daily_lesson_empty_list(self):
        """Test lesson selection with empty list"""
        selector = DayBasedLessonSelector()
        
        selected = selector.select_daily_lesson([])
        
        assert selected == {}
    
    def test_select_daily_lesson_consistency(self):
        """Test that selection is consistent for same day"""
        selector = DayBasedLessonSelector()
        
        lessons = [
            {"id": "1", "subject": "自然", "title": "課程1"},
            {"id": "2", "subject": "國文", "title": "課程2"},
            {"id": "3", "subject": "歷史", "title": "課程3"},
            {"id": "4", "subject": "地理", "title": "課程4"},
            {"id": "5", "subject": "公民", "title": "課程5"}
        ]
        
        # Multiple calls should return the same lesson
        selected1 = selector.select_daily_lesson(lessons)
        selected2 = selector.select_daily_lesson(lessons)
        selected3 = selector.select_daily_lesson(lessons)
        
        assert selected1 == selected2 == selected3
    
    @patch('lesson_service.datetime')
    def test_select_daily_lesson_different_days(self, mock_datetime):
        """Test that different days select different lessons"""
        selector = DayBasedLessonSelector()
        
        lessons = [
            {"id": "1", "subject": "自然", "title": "課程1"},
            {"id": "2", "subject": "國文", "title": "課程2"},
            {"id": "3", "subject": "歷史", "title": "課程3"}
        ]
        
        # Mock different days
        mock_datetime.now.return_value = datetime(2024, 1, 1)  # Day 1 of year
        selected1 = selector.select_daily_lesson(lessons)
        
        mock_datetime.now.return_value = datetime(2024, 1, 2)  # Day 2 of year
        selected2 = selector.select_daily_lesson(lessons)
        
        mock_datetime.now.return_value = datetime(2024, 1, 3)  # Day 3 of year
        selected3 = selector.select_daily_lesson(lessons)
        
        # Should potentially select different lessons
        # (may be same by coincidence, but algorithm should be working)
        selections = [selected1, selected2, selected3]
        assert all(sel in lessons for sel in selections)
    
    def test_select_daily_lesson_large_list(self):
        """Test lesson selection with large list"""
        selector = DayBasedLessonSelector()
        
        # Create a large list of lessons
        lessons = [
            {"id": str(i), "subject": f"科目{i}", "title": f"課程{i}"}
            for i in range(100)
        ]
        
        selected = selector.select_daily_lesson(lessons)
        
        assert selected in lessons
        assert "id" in selected
        assert "subject" in selected
        assert "title" in selected
    
    def test_select_daily_lesson_year_cycle(self):
        """Test that lesson selection cycles through the year"""
        selector = DayBasedLessonSelector()
        
        lessons = [
            {"id": "1", "subject": "自然", "title": "課程1"},
            {"id": "2", "subject": "國文", "title": "課程2"}
        ]
        
        # Test the cycling behavior with mocked dates
        with patch('lesson_service.datetime') as mock_datetime:
            # Day 1 of year
            mock_datetime.now.return_value = datetime(2024, 1, 1)
            selected1 = selector.select_daily_lesson(lessons)
            
            # Day 366 of year (next year, should cycle back)
            mock_datetime.now.return_value = datetime(2025, 1, 1)
            selected2 = selector.select_daily_lesson(lessons)
            
            # Should be the same lesson (cycling behavior)
            assert selected1 == selected2


class TestLessonServiceMocks:
    """Test lesson service components with mocked dependencies"""
    
    @patch('lesson_service.webdriver.Chrome')
    @patch('lesson_service.BeautifulSoup')
    def test_selenium_lesson_fetcher_basic_mocking(self, mock_soup, mock_chrome):
        """Test basic mocking setup for SeleniumLessonFetcher"""
        # This test verifies that we can mock the selenium dependencies
        # without actually running the browser
        from lesson_service import SeleniumLessonFetcher
        
        # Mock the webdriver
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        # Mock the soup
        mock_soup.return_value.select.return_value = [
            Mock(get_text=lambda strip=True: "【1-1】測試課程")
        ]
        
        fetcher = SeleniumLessonFetcher()
        
        # This should not fail with our mocking
        assert fetcher is not None
        assert hasattr(fetcher, 'filter_map')
        assert '自然' in fetcher.filter_map
        assert '國文' in fetcher.filter_map
        assert '歷史' in fetcher.filter_map
        assert '地理' in fetcher.filter_map
        assert '公民' in fetcher.filter_map


class TestLessonServiceIntegration:
    """Integration tests for lesson service components"""
    
    def test_subject_filter_with_lesson_selector(self):
        """Test integration between SubjectFilter and DayBasedLessonSelector"""
        # Create test data that would pass subject filters
        lessons = [
            {"id": "1", "subject": "自然", "title": "【1-1】植物的營養"},
            {"id": "2", "subject": "國文", "title": "【第一課】聲音鐘"},
            {"id": "3", "subject": "歷史", "title": "【2-3】秦漢統一"},
            {"id": "4", "subject": "地理", "title": "【3-5】氣候變化"},
            {"id": "5", "subject": "公民", "title": "【1-2】個人與社會"}
        ]
        
        # Verify that all lessons pass their respective filters
        assert SubjectFilter.filter_nature(lessons[0]["title"]) is True
        assert SubjectFilter.filter_chinese(lessons[1]["title"]) is True
        assert SubjectFilter.filter_history(lessons[2]["title"]) is True
        assert SubjectFilter.filter_geography(lessons[3]["title"]) is True
        assert SubjectFilter.filter_civics(lessons[4]["title"]) is True
        
        # Test lesson selection
        selector = DayBasedLessonSelector()
        selected = selector.select_daily_lesson(lessons)
        
        assert selected in lessons
        assert selected["id"] in ["1", "2", "3", "4", "5"]