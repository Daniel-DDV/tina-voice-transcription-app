# app/helpers/audio_utils.py

import os
from pydub import AudioSegment
import subprocess

def convert_to_supported_format(audio_file_path):
    """
    Converteert het opgegeven audiobestand naar een ondersteund formaat (WAV) als het dat nog niet is.
    Het geconverteerde bestand wordt opgeslagen in dezelfde directory als het origineel.
    """
    supported_formats = ('.wav', '.flac')
    file_ext = os.path.splitext(audio_file_path)[1].lower()

    if file_ext in supported_formats:
        print(f"✅ Het bestand '{audio_file_path}' is al in een ondersteund formaat.")
        return audio_file_path

    # Definieer het nieuwe bestandspad met .wav-extensie (in plaats van mp3)
    new_file_path = os.path.splitext(audio_file_path)[0] + '.wav'

    try:
        # Laad het audiobestand
        print(f"🔄 Bezig met het converteren van '{audio_file_path}' naar WAV-formaat...")
        audio = AudioSegment.from_file(audio_file_path)
        # Exporteer als WAV met specifieke parameters voor Azure Speech Services
        audio.export(new_file_path, format='wav', 
                     parameters=["-ar", "16000", "-ac", "1", "-sample_fmt", "s16"])
        print(f"✅ Conversie geslaagd! Nieuw bestand: '{new_file_path}'")
        return new_file_path
    except Exception as e:
        print(f"❌ Fout tijdens conversie: {e}")
        return None

def get_audio_duration(audio_file_path):
    try:
        audio = AudioSegment.from_file(audio_file_path)
        duration = len(audio) / 1000.0  # Duur in seconden
        return duration
    except Exception as e:
        print(f"❌ Fout bij het verkrijgen van de duur: {e}")
        return 0

def split_audio_file(audio_file_path, max_segment_length):
    """
    Splits het audiobestand in segmenten van de maximale gespecificeerde lengte.
    Retourneert een lijst met bestandspaden naar de segmenten.
    """
    duration = get_audio_duration(audio_file_path)
    if duration <= max_segment_length:
        # Geen splitsing nodig
        return [audio_file_path]

    print(f"🔄 Bezig met het splitsen van '{audio_file_path}' in segmenten...")
    segments_dir = os.path.join(os.path.dirname(audio_file_path), "segments")
    os.makedirs(segments_dir, exist_ok=True)

    segment_paths = []
    try:
        # Gebruik ffmpeg om de audio in segmenten te splitsen
        command = [
            "ffmpeg",
            "-i", audio_file_path,
            "-f", "segment",
            "-segment_time", str(max_segment_length),
            "-c", "copy",
            os.path.join(segments_dir, "segment_%03d" + os.path.splitext(audio_file_path)[1])
        ]
        subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        # Verkrijg lijst van segmentbestanden
        segment_files = sorted(os.listdir(segments_dir))
        segment_paths = [os.path.join(segments_dir, f) for f in segment_files if f.startswith("segment_")]

        print(f"✅ Splitsen geslaagd! {len(segment_paths)} segmenten aangemaakt.")
        return segment_paths
    except Exception as e:
        print(f"❌ Fout tijdens splitsen: {e}")
        return []