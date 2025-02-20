import os
from moviepy import VideoFileClip
from config.config import VIDEO_DOWNLOAD_PATH, AUDIO_DOWNLOAD_PATH

class AudioExtractor:
    """Class to handle audio extraction from video files"""
    
    def __init__(self):
        """Initialize AudioExtractor

        Args:
            None
        """
        self.default_audio_path = AUDIO_DOWNLOAD_PATH
        
    def extract_audio(self, video_path: str, output_filename: str = None, output_path: str = None) -> str:
        """Extract audio from a video file

        Args:
            video_path (str): Path to the video file
            output_filename (str, optional): Name for the output audio file. Defaults to None.
            output_path (str, optional): Path to save the audio file. Defaults to None.

        Returns:
            str: Path to the extracted audio file

        Raises:
            FileNotFoundError: If video file doesn't exist
            ValueError: If video path is invalid
        """
        if not video_path or not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        # Use default output path if none provided
        if output_path is None:
            output_path = self.default_audio_path
            
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
            
        # Generate output filename if none provided
        if output_filename is None:
            base_name = os.path.splitext(os.path.basename(video_path))[0]
            output_filename = f"{base_name}_audio"
            
        # Ensure filename ends with .mp3
        if not output_filename.endswith('.mp3'):
            output_filename += '.mp3'
            
        output_file = os.path.join(output_path, output_filename)
        
        try:
            video = VideoFileClip(video_path)
            audio = video.audio
            audio.write_audiofile(output_file)
            audio.close()
            video.close()
        except Exception as e:
            raise ValueError(f"Failed to extract audio: {str(e)}")
            
        return output_file 