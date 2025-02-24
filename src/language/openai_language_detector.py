from typing import Dict, Any
from langchain_openai import ChatOpenAI
from .base_language_detector import BaseLanguageDetector

class OpenAILanguageDetector(BaseLanguageDetector):
    """Language detector using OpenAI's GPT models"""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.1):
        """
        Initialize OpenAI language detector
        
        Args:
            model: OpenAI model to use
            temperature: Temperature for the model
        """
        self.client = ChatOpenAI(
            model_name=model,
            temperature=temperature,
        )
        self.model = model
    
    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing:
                - language_code: ISO language code
                - confidence: Confidence score
                - model: Model used for detection
        """
        if not text:
            raise ValueError("Text cannot be empty")
        
        system_message = (
            "You are a language detection expert. Analyze the following text "
            "and return only the ISO 639-1 language code (2 letters). "
            "For example: 'en' for English, 'es' for Spanish, etc."
        )
        
        response = self.client.invoke(
            system_message + "\n\nText to analyze: " + text[:500]  # Use first 500 chars for efficiency
        )
        
        # Extract the language code from response
        language_code = response.content.strip().lower()
        
        return {
            "language_code": language_code,
            "confidence": 1.0,  # OpenAI doesn't provide confidence scores
            "model": self.model
        } 