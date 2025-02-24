from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseSummarizer(ABC):
    """Abstract base class for text summarizers"""
    
    @abstractmethod
    def summarize(self, text: str, focus_points: Optional[str] = None) -> Dict[str, Any]:
        """
        Summarize the given text
        
        Args:
            text: Text to summarize
            focus_points: Optional string indicating specific areas of interest
            
        Returns:
            Dictionary containing:
                - summary: Summarized text
                - focus_points: Areas of focus (if provided)
                - model: Model used for summarization
                - metadata: Additional information about the summarization
        """
        pass 