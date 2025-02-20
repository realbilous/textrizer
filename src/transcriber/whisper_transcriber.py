from pathlib import Path
from typing import Dict, Any, Optional
import torch
import librosa
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import soundfile as sf

from .base_transcriber import BaseTranscriber

import torchaudio
from torchaudio.transforms import Resample

class WhisperTranscriber(BaseTranscriber):
    """Transcriber using Whisper models from HuggingFace"""
    
    def __init__(self, model_name: str = "openai/whisper-large-v3"):
        """
        Initialize Whisper transcriber
        
        Args:
            model_name: Name of the Whisper model to use from HuggingFace
        """
        self.torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load model and processor
        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name,
                                                                     torch_dtype=self.torch_dtype, 
                                                                     low_cpu_mem_usage=True, 
                                                                     use_safetensors=True)
        self.model.to(self.device)
    
    def transcribe(self, audio_path: str | Path) -> str:
        """
        Transcribe audio file to text
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        result = self.transcribe_with_metadata(audio_path)
        return result["text"]
    
    def transcribe_with_metadata(self, audio_path: str | Path) -> Dict[str, Any]:
        """
        Transcribe audio file and return metadata
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            Dictionary containing:
                - text: Transcribed text
                - language: Detected language
                - segments: List of segments with timestamps
        """
        audio_path = Path(audio_path)
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        # Load the audio file
        waveform, original_sample_rate = torchaudio.load(audio_path)
        
        # Convert stereo to mono if needed
        if waveform.shape[0] > 1:
            waveform = waveform.mean(dim=0, keepdim=True)

        # Define the resampling transform
        resample_transform = Resample(orig_freq=original_sample_rate, new_freq=16000)

        # Apply the resampling
        resampled_waveform = resample_transform(waveform)
        
        inputs = self.processor(resampled_waveform.squeeze(), 
                                return_tensors="pt", 
                                truncation=False, 
                                padding="longest", 
                                return_attention_mask=True, 
                                sampling_rate=16_000)
        
        inputs = inputs.to(dtype=self.torch_dtype, device=self.device)

        # Generate tokens with better parameters
        predicted_ids = self.model.generate(
            **inputs,
            do_sample=True,
            temperature=0.0,
            no_repeat_ngram_size=3,
            return_timestamps=True,
            num_beams=2,
            # length_penalty=1.0,
            top_p=0.95
        )
        
        # Decode tokens to text
        transcription = self.processor.batch_decode(
            predicted_ids, 
            skip_special_tokens=True
        )[0]
        
        # Get metadata from model outputs
        metadata = {
            "text": transcription,
            "model_name": self.model_name,
            "device": self.device
        }
        
        return metadata 