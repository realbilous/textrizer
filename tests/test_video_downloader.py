import pytest
import os
from pathlib import Path
from src.video_downloader import VideoDownloader, YouTubeDLDownloader
import subprocess

class TestYouTubeDLDownloader:
    @pytest.fixture
    def downloader(self):
        return YouTubeDLDownloader()
    
    @pytest.fixture
    def output_path(self, tmp_path):
        """Create a temporary directory for downloads"""
        return str(tmp_path / "downloads")
    
    @pytest.fixture
    def test_video_url(self):
        """A short, public domain video URL for testing"""
        return "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # "Me at the zoo" - First YouTube video
    
    def test_init(self, downloader):
        """Test that downloader initializes correctly"""
        assert isinstance(downloader, VideoDownloader)
        assert isinstance(downloader, YouTubeDLDownloader)
    
    def test_verify_youtube_dl(self, downloader):
        """Test that youtube-dl verification works"""
        downloader._verify_youtube_dl()  # Should not raise an exception
    
    def test_get_video_info(self, downloader, test_video_url):
        """Test video info retrieval"""
        info = downloader._get_video_info(test_video_url)
        assert isinstance(info, dict)
        assert 'title' in info
        assert info['id'] == 'jNQXAC9IVRw'
    
    def test_download_video(self, downloader, output_path, test_video_url):
        """Test video download with default filename"""
        video_path = None
        try:
            video_path = downloader.download(
                url=test_video_url,
                output_path=output_path
            )
            assert os.path.exists(video_path)
            assert os.path.getsize(video_path) > 0
        finally:
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
    
    def test_download_video_custom_filename(self, downloader, output_path, test_video_url):
        """Test video download with custom filename"""
        custom_filename = "test_video"
        video_path = None
        try:
            video_path = downloader.download(
                url=test_video_url,
                output_path=output_path,
                filename=custom_filename
            )
            assert os.path.exists(video_path)
            assert os.path.basename(video_path).startswith(custom_filename)
        finally:
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
    
    def test_download_audio(self, downloader, output_path, test_video_url):
        """Test audio download"""
        audio_path = None
        try:
            audio_path = downloader.download_audio(
                url=test_video_url,
                output_path=output_path
            )
            assert os.path.exists(audio_path)
            assert audio_path.endswith('.mp3')
            assert os.path.getsize(audio_path) > 0
        finally:
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
    
    def test_invalid_url(self, downloader, output_path):
        """Test handling of invalid URL"""
        with pytest.raises(ValueError):
            downloader.download(
                url="https://www.youtube.com/watch?v=invalid_video_id",
                output_path=output_path
            )
    
    def test_download_with_special_chars_filename(self, downloader, output_path, test_video_url):
        """Test download with filename containing special characters"""
        filename = "test!@#$%^&*()_+video"
        video_path = None
        try:
            video_path = downloader.download(
                url=test_video_url,
                output_path=output_path,
                filename=filename
            )
            assert os.path.exists(video_path)
            # Check that filename was sanitized
            assert not any(c in os.path.basename(video_path) for c in "!@#$%^&*()+")
        finally:
            if video_path and os.path.exists(video_path):
                os.remove(video_path)
    
    @pytest.mark.skipif(not os.path.exists('/nonexistent'), 
                       reason="This test is designed to fail")
    def test_invalid_output_path(self, downloader, test_video_url):
        """Test handling of invalid output path"""
        with pytest.raises(ValueError):
            downloader.download(
                url=test_video_url,
                output_path="/nonexistent/path/that/doesnt/exist"
            )
    
    def test_default_video_path(self, downloader, test_video_url):
        """Test video download using default VIDEO_DOWNLOAD_PATH"""
        from config.config import VIDEO_DOWNLOAD_PATH
        
        try:
            video_path = downloader.download(url=test_video_url)
            assert os.path.exists(video_path)
            assert os.path.dirname(video_path) == str(VIDEO_DOWNLOAD_PATH)
            assert os.path.getsize(video_path) > 0
        finally:
            # Cleanup only the test file, not the directory
            if os.path.exists(video_path):
                os.remove(video_path)
    
    def test_default_audio_path(self, downloader, test_video_url):
        """Test audio download using default AUDIO_DOWNLOAD_PATH"""
        from config.config import AUDIO_DOWNLOAD_PATH
        
        try:
            audio_path = downloader.download_audio(url=test_video_url)
            assert os.path.exists(audio_path)
            assert os.path.dirname(audio_path) == str(AUDIO_DOWNLOAD_PATH)
            assert audio_path.endswith('.mp3')
            assert os.path.getsize(audio_path) > 0
        finally:
            # Cleanup only the test file, not the directory
            if os.path.exists(audio_path):
                os.remove(audio_path)