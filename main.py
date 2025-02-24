import argparse
import os
from pathlib import Path
from datetime import datetime
from src.video_downloader import YouTubeDLDownloader
from src.audio_extractor import AudioExtractor
from src.transcriber.whisper_transcriber import WhisperTranscriber
from src.translator.openai_translator import OpenAITranslator
from src.summarizer.openai_summarizer import OpenAISummarizer
from src.language.openai_language_detector import OpenAILanguageDetector

def parse_args():
    parser = argparse.ArgumentParser(
        description='Download YouTube video, transcribe, summarize, and translate it.'
    )
    parser.add_argument(
        '--video_url',
        '-v',
        type=str,
        required=True,
        help='YouTube video URL to process'
    )
    parser.add_argument(
        '--language',
        '-l',
        type=str,
        default='en',
        help='Target language for translation (default: English)'
    )
    parser.add_argument(
        '--output_path',
        '-o',
        type=str,
        default=os.getcwd(),
        help='Output directory path (default: current directory)'
    )
    parser.add_argument(
        '--focus_points',
        '-f',
        type=str,
        default="methodology, problems and solutions",
        help='Aspects to focus on in the summary'
    )
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_args()
    
    output_path = Path(args.output_path)
    
    # Initialize components
    downloader = YouTubeDLDownloader()
    audio_extractor = AudioExtractor()
    transcriber = WhisperTranscriber(model_name="openai/whisper-small")
    summarizer = OpenAISummarizer()
    lang_detector = OpenAILanguageDetector()
    translator = OpenAITranslator()
    
    # Process the video
    print(f"Downloading video from: {args.video_url}")
    video_path = downloader.download(args.video_url)
    
    print("Extracting audio...")
    audio_path = audio_extractor.extract_audio(video_path)
    
    print("Transcribing audio...")
    transcription = transcriber.transcribe(audio_path)
    
    print("Detecting language...")
    detected_lang = lang_detector.detect_language(transcription)["language_code"]
    
    print("Generating summary...")
    transcription_summary = summarizer.summarize(
        transcription,
        focus_points=args.focus_points
    )["summary"]
    
    # Only translate if target language is different from detected language
    if detected_lang != args.language:
        print(f"Translating from {detected_lang} to {args.language}...")
        translation = translator.translate(
            transcription_summary,
            args.language
        )["translated_text"]
    else:
        print(f"Content already in target language ({args.language}), skipping translation.")
        translation = transcription_summary
    
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = output_path / Path(video_path).stem / timestamp
    output_path.mkdir(parents=True, exist_ok=True)

    # Save outputs with timestamp
    transcription_path = output_path / "transcription.txt"
    summary_path = output_path / "summary.txt"
    translation_path = output_path / f"translation_{args.language}.txt"    
    

    # Save transcription
    with open(transcription_path, "w", encoding="utf-8") as f:
        f.write(transcription)
    
    # Save summary
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(transcription_summary)
    
    # Save translation
    with open(translation_path, "w", encoding="utf-8") as f:
        f.write(translation)
    
    print("\nProcessing complete! Files saved:")
    print(f"- Transcription:", transcription_path)
    print(f"- Summary:", summary_path)
    print(f"- Translation:", translation_path)

if __name__ == "__main__":
    main()
