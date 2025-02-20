from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Dict, Any

class BaseTranscriber(ABC):
    """Abstract base class for audio transcription"""
    
    @abstractmethod
    def transcribe(self, audio_path: str | Path) -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        
        Raises:
            FileNotFoundError: If audio file doesn't exist
            ValueError: If audio file format is not supported
        """
        pass
    
    @abstractmethod
    def transcribe_with_metadata(self, audio_path: str | Path) -> Dict[str, Any]:
        """
        Transcribe audio file to text and return additional metadata
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary containing transcribed text and additional metadata
            (e.g., confidence scores, timestamps, etc.)
        """
        pass 