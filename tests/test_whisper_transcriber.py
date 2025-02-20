import pytest
from pathlib import Path
from src.transcriber.whisper_transcriber import WhisperTranscriber
from config.config import AUDIO_DOWNLOAD_TEST_PATH

class TestWhisperTranscriber:
    @pytest.fixture
    def transcriber(self):
        return WhisperTranscriber(model_name="openai/whisper-small")
    
    def test_init_default(self, transcriber):
        """Test default initialization"""
        assert transcriber.model_name == "openai/whisper-small"
        assert transcriber.device in ["cuda", "cpu"]
    
    def test_transcribe_file_not_found(self, transcriber):
        """Test transcription with non-existent file"""
        with pytest.raises(FileNotFoundError):
            transcriber.transcribe("nonexistent_audio.mp3")
    
    def test_transcribe_success(self, transcriber):
        """Test successful transcription with a sample audio file"""
        # Check for audio files in default location
        audio_path = Path(AUDIO_DOWNLOAD_TEST_PATH) / "sample_audio.mp3"

        text = transcriber.transcribe(audio_path)
        assert isinstance(text, str)
        assert len(text) > 0
    
    def test_transcribe_with_metadata(self, transcriber):
        """Test transcription with metadata"""
        # Check for audio files in default location
        audio_path = Path(AUDIO_DOWNLOAD_TEST_PATH) / "sample_audio.mp3"
        
        result = transcriber.transcribe_with_metadata(audio_path)

        assert isinstance(result, dict)
        assert "text" in result
        assert "model_name" in result 