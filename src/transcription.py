import os
from dotenv import load_dotenv
from openai import OpenAI
from yt_dlp import YoutubeDL  # Use yt_dlp instead of pytube
from pathlib import Path

# Load environment variables from .env file
load_dotenv()
client = OpenAI()

def _download_audio_with_yt_dlp(url, output_path):
    """Helper function to download audio using yt-dlp."""
    # Ensure output_path is a Path object for yt-dlp
    path_obj = Path(output_path)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(path_obj.with_suffix('')), # yt-dlp needs a string path
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_youtube_audio(youtube_url, project_path):
    """
    Downloads audio from a YouTube URL using yt-dlp, transcribes it, 
    and saves the transcript.
    """
    print(f"-> Starting transcription for URL: {youtube_url}")
    
    # Define output paths
    raw_audio_path = os.path.join(project_path, "0_raw_audio.mp3")
    transcript_path = os.path.join(project_path, "0_transcript.txt")

    # Download audio using yt-dlp
    print(f"-> Downloading audio for '{youtube_url}'...")
    _download_audio_with_yt_dlp(youtube_url, raw_audio_path)

    # Transcribe audio using OpenAI Whisper
    print("-> Transcribing audio with Whisper API...")
    with open(raw_audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )

    # Save the transcript to a file
    with open(transcript_path, "w") as f:
        f.write(transcript)

    print(f"✅ Transcription complete. Saved to: {transcript_path}")
    return transcript_path