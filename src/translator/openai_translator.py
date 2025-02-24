from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from .base_translator import BaseTranslator

class OpenAITranslator(BaseTranslator):
    """Translator using OpenAI's GPT models"""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.1):
        """
        Initialize OpenAI translator
        
        Args:
            model: OpenAI model to use
            temperature: Temperature for the model
        """
        self.client = ChatOpenAI(
            model_name=model, 
            temperature=temperature,
        )
        self.model = model
    
    def translate(self, text: str, target_language: str) -> Dict[str, Any]:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language code (e.g., 'en', 'es', 'fr')
            
        Returns:
            Dictionary containing:
                - translated_text: Translated text
                - target_language: Target language
                - model: Model used for translation
                - usage: Token usage statistics
        """
        system_message = (
            f"You are a professional translator. Translate the following text to {target_language}. "
            "Maintain the original meaning, tone, and style as much as possible."
        )
        
        response = self.client.predict(
            system_message + "\n\nText to translate: " + text
        )
        
        return {
            "translated_text": response,
            "target_language": target_language,
            "model": self.model,
        }
    
    def batch_translate(self, texts: List[str], target_language: str) -> List[Dict[str, Any]]:
        """
        Translate multiple texts
        
        Args:
            texts: List of texts to translate
            target_language: Target language code
            
        Returns:
            List of translation results, each containing metadata
        """
        return [self.translate(text, target_language) for text in texts] 