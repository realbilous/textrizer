from src.video_downloader import YouTubeDLDownloader
from src.audio_extractor import AudioExtractor
from src.transcriber.whisper_transcriber import WhisperTranscriber

def main():
    # Add your main program logic here
    downloader = YouTubeDLDownloader()
    full_video_file_path = downloader.download("https://www.youtube.com/watch?v=hpyNpGhsNfA")

    audio_extractor = AudioExtractor()
    full_audio_file_path = audio_extractor.extract_audio(full_video_file_path)

    transcriber = WhisperTranscriber(model_name="openai/whisper-small")
    transcription = transcriber.transcribe(full_audio_file_path)
    print(transcription)


if __name__ == "__main__":
    main()
