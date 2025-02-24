import pytest
from src.summarizer.openai_summarizer import OpenAISummarizer
from unittest.mock import patch, Mock

class TestOpenAISummarizer:
    """Test suite for OpenAISummarizer class"""
    
    @pytest.fixture
    def summarizer(self):
        return OpenAISummarizer(model="gpt-4o-mini", temperature=0.1, max_length=2000)

    def test_input_validation(self, summarizer):
        """Test input validation"""
        # Test empty string
        with pytest.raises(ValueError, match="Text to summarize cannot be empty"):
            summarizer.summarize("")
        
        # Test None input
        with pytest.raises(ValueError, match="Text to summarize cannot be empty"):
            summarizer.summarize(None)
        
        # Test invalid number of points
        with pytest.raises(ValueError, match="Number of points must be positive"):
            summarizer.bullet_point_summary("text", num_points=0)
        
        with pytest.raises(ValueError, match="Number of points must be positive"):
            summarizer.bullet_point_summary("text", num_points=-1)

    def test_init_custom_values(self):
        """Test initialization with custom values"""
        summarizer = OpenAISummarizer(
            model="gpt-4o-mini",
            temperature=0.5,
            max_length=1000
        )
        
        assert summarizer.model == "gpt-4o-mini"
        assert summarizer.max_length == 1000
        assert summarizer.client is not None 