"""
Interface definitions for the Daily Lesson system
Following SOLID principles - Interface Segregation Principle
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class LessonFetcher(ABC):
    """Abstract interface for fetching lesson data"""
    
    @abstractmethod
    def fetch_lessons(self, subject_config: Dict) -> List[Dict]:
        """Fetch lessons for a given subject configuration"""
        pass


class ImageGenerator(ABC):
    """Abstract interface for image generation"""
    
    @abstractmethod
    def generate_image(self, subject: str, title: str, content: str) -> Optional[str]:
        """Generate an image for the given lesson content"""
        pass


class ContentRenderer(ABC):
    """Abstract interface for rendering content"""
    
    @abstractmethod
    def render(self, lesson_data: Dict, date_str: str) -> str:
        """Render lesson data into the appropriate format"""
        pass


class LessonSelector(ABC):
    """Abstract interface for selecting daily lessons"""
    
    @abstractmethod
    def select_daily_lesson(self, lessons: List[Dict]) -> Dict:
        """Select the lesson for today from the available lessons"""
        pass