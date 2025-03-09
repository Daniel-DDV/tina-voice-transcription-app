# app/models/model_utils.py

import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from app.models.azure_speech_utils import transcribe_audio_file, transcribe_with_timestamps as azure_transcribe_with_timestamps

def load_model():
    """
    This function now serves as a compatibility layer.
    It returns None values for the original model components since we're using Azure Speech.
    """
    print("Using Azure Speech Services for transcription")
    return None, None, None

def transcribe(audio_file_path, asr_pipeline=None):
    """
    Transcribe audio using Azure Speech Services.
    The asr_pipeline parameter is kept for compatibility with the original code.
    """
    print("🎙️ Bezig met transcriberen van audio via Azure Speech... Een moment geduld alstublieft.")
    result = transcribe_audio_file(audio_file_path)
    return result

def transcribe_with_timestamps(audio_file_path, asr_pipeline=None):
    """
    Transcribe audio with timestamps using Azure Speech Services.
    The asr_pipeline parameter is kept for compatibility with the original code.
    """
    print("🎙️ Bezig met transcriberen van audio met tijdstempels via Azure Speech... Een moment geduld alstublieft.")
    result = azure_transcribe_with_timestamps(audio_file_path)
    return result