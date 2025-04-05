from pathlib import Path
from openai import OpenAI
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Hardcoded YouTube URL
youtube_url = "https://www.youtube.com/watch?v=wazHMMaiDEA"

# Output paths
RAW_DIR = Path("raw")
TEXT_DIR = Path("text")
RAW_DIR.mkdir(exist_ok=True)
TEXT_DIR.mkdir(exist_ok=True)

AUDIO_FILE = RAW_DIR / "audio.mp3"
TRANSCRIPT_FILE = TEXT_DIR / "transcript.txt"

def download_audio(url: str, output_path: Path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_audio(audio_path: Path, output_txt: Path):
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    output_txt.write_text(transcript.text)

def transcribe_youtube():
    print("Downloading audio...")
    download_audio(youtube_url, AUDIO_FILE)
    print("Transcribing audio...")
    transcribe_audio(AUDIO_FILE, TRANSCRIPT_FILE)
    print(f"Transcript saved to {TRANSCRIPT_FILE}")

if __name__ == "__main__":
    transcribe_youtube()
