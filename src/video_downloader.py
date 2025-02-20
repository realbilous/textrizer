from abc import ABC, abstractmethod
from typing import Optional
import youtube_dl
import os
from pathlib import Path
from config.config import VIDEO_DOWNLOAD_PATH, AUDIO_DOWNLOAD_PATH  

class VideoDownloader(ABC):
    """Abstract base class for video downloading functionality."""
    
    @abstractmethod
    def download(self, url: str, output_path: str, filename: Optional[str] = None) -> str:
        """
        Download video from the given URL.
        
        Args:
            url: URL of the video to download
            output_path: Path where the video should be saved
            filename: Optional custom filename (without extension)
            
        Returns:
            str: Path to the downloaded video file
        """
        pass

class YouTubeDLDownloader(VideoDownloader):
    """Implementation of VideoDownloader using youtube-dl Python module."""
    
    def __init__(self):
        """Initialize the downloader."""
        self._verify_youtube_dl()

    def _verify_youtube_dl(self):
        """Verify that youtube-dl module is installed."""
        try:
            import youtube_dl
        except ImportError:
            raise RuntimeError("youtube-dl module not found. Please install it with 'pip install youtube-dl'")

    def _get_video_info(self, url: str) -> dict:
        """
        Get video information using youtube-dl.
        
        Args:
            url: Video URL
            
        Returns:
            dict: Video information
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                return ydl.extract_info(url, download=False)
        except youtube_dl.utils.DownloadError as e:
            raise ValueError(f"Error getting video info: {str(e)}")

    def download(self, url: str, output_path: str = VIDEO_DOWNLOAD_PATH, filename: Optional[str] = None) -> str:
        """
        Download video using youtube-dl.
        
        Args:
            url: Video URL
            output_path: Path where the video should be saved (defaults to VIDEO_DOWNLOAD_PATH from config)
            filename: Optional custom filename (without extension)
            
        Returns:
            str: Path to the downloaded video file
            
        Raises:
            ValueError: If the URL is invalid or video cannot be downloaded
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)
            
            # Get video info to determine the title if filename is not provided
            if not filename:
                video_info = self._get_video_info(url)
                filename = video_info.get('title', 'video')
                
            # Clean filename of invalid characters
            filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_'))
            output_template = str(Path(output_path) / f"{filename}.%(ext)s")
            
            ydl_opts = {
                'format': 'best',  # Best quality
                'outtmpl': output_template,
                'noplaylist': True,  # Don't download playlists
            }
            
            # Download the video
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=True)
                ext = video_info['ext']
                final_path = str(Path(output_path) / f"{filename}.{ext}")
                
                if not os.path.exists(final_path):
                    raise FileNotFoundError("Downloaded file not found")
                    
                return final_path
            
        except youtube_dl.utils.DownloadError as e:
            raise ValueError(f"Error downloading video: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")

    def download_audio(self, url: str, output_path: str = AUDIO_DOWNLOAD_PATH, filename: Optional[str] = None) -> str:
        """
        Download only the audio from a video.
        
        Args:
            url: Video URL
            output_path: Path where the audio should be saved (defaults to AUDIO_DOWNLOAD_PATH from config)
            filename: Optional custom filename (without extension)
            
        Returns:
            str: Path to the downloaded audio file
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_path, exist_ok=True)
            
            # Get video info to determine the title if filename is not provided
            if not filename:
                video_info = self._get_video_info(url)
                filename = video_info.get('title', 'audio')
                
            # Clean filename of invalid characters
            filename = "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_'))
            output_template = str(Path(output_path) / f"{filename}.%(ext)s")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_template,
                'noplaylist': True,
            }
            
            # Download and extract audio
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            # Check for the output file
            audio_path = str(Path(output_path) / f"{filename}.mp3")
            if not os.path.exists(audio_path):
                raise FileNotFoundError("Downloaded audio file not found")
                
            return audio_path
            
        except youtube_dl.utils.DownloadError as e:
            raise ValueError(f"Error downloading audio: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}") 