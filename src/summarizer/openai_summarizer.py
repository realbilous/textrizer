from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from .base_summarizer import BaseSummarizer

class OpenAISummarizer(BaseSummarizer):
    """Summarizer using OpenAI's GPT models"""
    
    def __init__(self, model: str = "gpt-4o-mini", temperature: float = 0.1, max_length: int = 2000):
        """
        Initialize OpenAI summarizer
        
        Args:
            model: OpenAI model to use
            temperature: Temperature for the model (lower means more focused/deterministic)
            max_length: Target maximum length for summaries
        """
        self.client = ChatOpenAI(
            model_name=model,
            temperature=temperature,
        )
        self.model = model
        self.max_length = max_length
    
    def summarize(self, text: str, focus_points: Optional[str] = None) -> Dict[str, Any]:
        """
        Summarize the given text with optional focus on specific points
        
        Args:
            text: Text to summarize
            focus_points: Optional string indicating specific areas of interest
            
        Returns:
            Dictionary containing:
                - summary: Summarized text
                - focus_points: Areas of focus (if provided)
                - model: Model used for summarization
                - metadata: Additional information
        """
        if not text:
            raise ValueError("Text to summarize cannot be empty")
        
        # Construct the system message based on whether focus points are provided
        if focus_points:
            system_message = (
                "You are an expert summarizer. Create a concise summary of the following text, "
                f"focusing particularly on these aspects: {focus_points}. "
                f"Aim to keep the summary under {self.max_length} characters while maintaining "
                "accuracy and capturing key points."
            )
        else:
            system_message = (
                "You are an expert summarizer. Create a concise but comprehensive summary "
                f"of the following text. Aim to keep the summary under {self.max_length} "
                "characters while maintaining accuracy and capturing key points."
            )
        
        # Get the summary from the model
        response = self.client.invoke(
            system_message + "\n\nText to summarize: " + text
        )
        
        summary = response.content
        
        # Prepare metadata about the summarization
        metadata = {
            "original_length": len(text),
            "summary_length": len(summary),
            "compression_ratio": len(summary) / len(text),
            "max_length": self.max_length
        }
        
        return {
            "summary": summary,
            "focus_points": focus_points,
            "model": self.model,
            "metadata": metadata
        }
    
    def bullet_point_summary(self, text: str, num_points: int = 5, focus_points: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a bullet-point summary of the key points
        
        Args:
            text: Text to summarize
            num_points: Number of bullet points to generate
            focus_points: Optional string indicating specific areas of interest
            
        Returns:
            Dictionary containing summary and metadata
        """
        if not text:
            raise ValueError("Text to summarize cannot be empty")
        
        if num_points <= 0:
            raise ValueError("Number of points must be positive")
        
        system_message = (
            f"You are an expert summarizer. Extract the {num_points} most important points "
            "from the following text as bullet points. "
        )
        
        if focus_points:
            system_message += f"Focus particularly on these aspects: {focus_points}."
        
        response = self.client.invoke(
            system_message + "\n\nText to summarize: " + text
        )
        
        bullet_points = response.content
        
        return {
            "summary": bullet_points,
            "format": "bullet_points",
            "num_points": num_points,
            "focus_points": focus_points,
            "model": self.model
        } 