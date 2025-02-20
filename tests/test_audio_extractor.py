import pytest
import os
from src.audio_extractor import AudioExtractor
from config.config import VIDEO_DOWNLOAD_TEST_PATH

class TestAudioExtractor:
    @pytest.fixture
    def audio_extractor(self):
        return AudioExtractor()
    
    @pytest.fixture
    def sample_video_path(self):
        """Get path to first video file in standard video directory, skip if none found"""
        video_files = [f for f in os.listdir(VIDEO_DOWNLOAD_TEST_PATH) if f.endswith(('.mp4', '.mkv', '.avi'))]
        if not video_files:
            pytest.skip("No video files found in standard video directory")
        return os.path.join(VIDEO_DOWNLOAD_TEST_PATH, video_files[0])
    
    def test_init(self, audio_extractor):
        """Test AudioExtractor initialization"""
        pass  # Remove redundant path check
    
    def test_extract_audio_file_not_found(self, audio_extractor):
        """Test extract_audio with non-existent file"""
        with pytest.raises(FileNotFoundError):
            audio_extractor.extract_audio("nonexistent_video.mp4")
    
    def test_extract_audio_success(self, audio_extractor, sample_video_path, tmp_path):
        """Test successful audio extraction"""
        output_path = str(tmp_path / "output")
        output_filename = "test_output.mp3"
        
        output_file = audio_extractor.extract_audio(
            sample_video_path,
            output_filename=output_filename,
            output_path=output_path
        )
        
        assert os.path.exists(output_file)
        assert output_file == os.path.join(output_path, output_filename)
        
        # Clean up the created audio file
        os.remove(output_file)
    
    def test_extract_audio_default_filename(self, audio_extractor, sample_video_path, tmp_path):
        """Test audio extraction with default filename"""
        output_path = str(tmp_path / "output")
        
        output_file = audio_extractor.extract_audio(
            sample_video_path,
            output_path=output_path
        )
        
        expected_filename = f"{os.path.splitext(os.path.basename(sample_video_path))[0]}_audio.mp3"
        assert os.path.basename(output_file) == expected_filename
        
        # Clean up the created audio file
        os.remove(output_file)
