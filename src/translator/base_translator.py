from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTranslator(ABC):
    """Base abstract class for text translation"""
    
    @abstractmethod
    def translate(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'en', 'es', 'fr')
            
        Returns:
            Dictionary containing:
                - translated_text: Translated text
                - source_language: Detected source language (if available)
                - target_language: Target language
                - model_info: Information about the model used
        """
        pass 