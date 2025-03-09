# app/models/azure_speech_utils.py

import os
import tempfile
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import time
from pydub import AudioSegment

# Load environment variables from root project directory
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), '.env')
load_dotenv(dotenv_path)

def get_azure_speech_config():
    """
    Create and return an Azure Speech config using environment variables.
    """
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    
    print(f"Azure Speech Key: {'*' * len(speech_key) if speech_key else 'NOT FOUND'}")
    print(f"Azure Speech Region: {service_region if service_region else 'NOT FOUND'}")
    
    if not speech_key or not service_region:
        raise ValueError("Azure Speech credentials not found in environment variables")
    
    # Create speech configuration
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    
    # Set speech recognition language to Dutch
    speech_config.speech_recognition_language = "nl-NL"
    
    return speech_config

def transcribe_audio_file(audio_file_path):
    """
    Transcribe an audio file using Azure Speech Services.
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
    """
    print(f"Starting transcription of file: {audio_file_path}")
    
    # Verify file exists
    if not os.path.exists(audio_file_path):
        print(f"Error: File not found: {audio_file_path}")
        return "Error: Audio file not found"
    
    # Check file size
    file_size = os.path.getsize(audio_file_path)
    print(f"Audio file size: {file_size} bytes")
    
    try:
        speech_config = get_azure_speech_config()
        
        # Create audio configuration for the audio file
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        
        # Create a speech recognizer and collect results
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config, 
            audio_config=audio_config
        )
        
        # Use the same approach as the working example, but adapted for file transcription
        transcript = []
        done = False
        
        def recognized_cb(evt):
            if evt.result.text:
                print(f"RECOGNIZED: {evt.result.text}")
                transcript.append(evt.result.text)
        
        def canceled_cb(evt):
            print(f"CANCELED: {evt.reason}")
            if evt.reason == speechsdk.CancellationReason.Error:
                print(f"Error details: {evt.error_details}")
            nonlocal done
            done = True
        
        def session_stopped_cb(evt):
            print("Session stopped")
            nonlocal done
            done = True
        
        # Connect callbacks
        speech_recognizer.recognized.connect(recognized_cb)
        speech_recognizer.canceled.connect(canceled_cb)
        speech_recognizer.session_stopped.connect(session_stopped_cb)
        
        # Start continuous recognition
        print("Starting speech recognition...")
        speech_recognizer.start_continuous_recognition()
        
        # Wait for recognition to complete (using a simple timeout approach)
        timeout = 30  # Maximum seconds to wait
        start_time = time.time()
        while not done and time.time() - start_time < timeout:
            time.sleep(0.5)
        
        # Stop recognition
        speech_recognizer.stop_continuous_recognition()
        
        # Return results
        if not transcript:
            return "No speech could be recognized"
        
        complete_transcript = " ".join(transcript)
        print(f"Transcription result: {complete_transcript}")
        return complete_transcript
        
    except Exception as e:
        print(f"Exception during transcription: {str(e)}")
        return f"Error: {str(e)}"

def transcribe_with_timestamps(audio_file_path):
    """
    Transcribe an audio file with timestamps using Azure Speech Services.
    
    Args:
        audio_file_path (str): Path to the audio file
        
    Returns:
        dict: Transcription result with timestamps
    """
    print(f"Starting transcription with timestamps for file: {audio_file_path}")
    
    # For now, use the simple transcription and add a placeholder timestamp
    transcription = transcribe_audio_file(audio_file_path)
    
    # Check if the transcription is an error
    if transcription.startswith("Error:") or transcription.startswith("No speech"):
        # Return error format
        result = {
            "text": transcription,
            "chunks": []
        }
    else:
        # Create a result format similar to what the original code expected
        result = {
            "text": transcription,
            "chunks": [{"text": transcription, "timestamp": [0.0, None]}]
        }
    
    print(f"Transcription result: {result}")
    return result
