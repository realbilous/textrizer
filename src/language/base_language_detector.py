from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseLanguageDetector(ABC):
    """Abstract base class for language detectors"""
    
    @abstractmethod
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing:
                - language_code: ISO language code (e.g., 'en', 'es')
                - confidence: Confidence score of the detection
                - model: Model used for detection
        """
        pass 