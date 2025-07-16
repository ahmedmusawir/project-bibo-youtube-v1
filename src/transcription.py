import os
import tempfile
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from yt_dlp import YoutubeDL

# Load environment variables from .env file
load_dotenv()
client = OpenAI()

def _download_audio_to_temp(url: str) -> str:
    """Downloads audio to a temporary file and returns the path."""
    temp_dir = tempfile.gettempdir()
    temp_audio_path = os.path.join(temp_dir, "temp_audio_for_transcription.mp3")
    
    ydl_opts = {
        'format': 'bestaudio/best',
        # Use a fixed name in a temp directory
        'outtmpl': os.path.join(temp_dir, "temp_audio_for_transcription"),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'overwrite': True, # Overwrite if the file exists
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return temp_audio_path

def transcribe_youtube_audio(youtube_url: str, output_transcript_path: str):
    """
    Downloads audio from a YouTube URL, transcribes it, and saves the transcript
    to the specified path.

    Args:
        youtube_url (str): The URL of the YouTube video.
        output_transcript_path (str): The absolute path to save the transcript file.
    """
    print(f"-> Starting transcription for URL: {youtube_url}")
    
    # 1. Download audio to a temporary file
    print("-> Downloading audio...")
    temp_audio_path = _download_audio_to_temp(youtube_url)

    # 2. Transcribe the temporary audio file
    print("-> Transcribing audio with Whisper API...")
    with open(temp_audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )

    # 3. Save the transcript to the specified output file
    # Ensure the directory exists
    output_dir = os.path.dirname(output_transcript_path)
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_transcript_path, "w", encoding='utf-8') as f:
        f.write(transcript)

    # 4. Clean up the temporary audio file
    os.remove(temp_audio_path)

    print(f"✅ Transcription complete. Saved to: {output_transcript_path}")
    return output_transcript_path
