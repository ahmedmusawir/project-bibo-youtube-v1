from pathlib import Path
from openai import OpenAI
from yt_dlp import YoutubeDL
import subprocess
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Hardcoded YouTube URL
youtube_url = "https://youtu.be/2IK3DFHRFfw"

# Output paths
RAW_DIR = Path("raw")
TEXT_DIR = Path("text")
RAW_DIR.mkdir(exist_ok=True)
TEXT_DIR.mkdir(exist_ok=True)

# Use WAV format for better Whisper compatibility
DOWNLOADED_FILE = RAW_DIR / "audio_raw"
AUDIO_FILE = RAW_DIR / "audio.wav"
TRANSCRIPT_FILE = TEXT_DIR / "transcript.txt"

def get_downloaded_file_path(base_path: Path) -> Path:
    # Find the file that starts with audio_raw.*
    for file in base_path.parent.glob(base_path.name + ".*"):
        return file
    raise FileNotFoundError("Downloaded file not found with any known extension.")


def download_audio(url: str, output_path: Path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path.with_suffix('')),  # No extension
        'quiet': False
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def convert_to_wav(input_path: Path, output_path: Path):
    # Force mono, 16kHz, WAV format
    subprocess.run([
        "ffmpeg", "-y",
        "-i", str(input_path),
        "-ar", "16000",
        "-ac", "1",
        str(output_path)
    ], check=True)

def transcribe_audio(audio_path: Path, output_txt: Path):
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    output_txt.write_text(transcript.text)

def transcribe_youtube():
    print("Downloading audio...")
    download_audio(youtube_url, DOWNLOADED_FILE)
    print("Converting to WAV...")
    # convert_to_wav(DOWNLOADED_FILE.with_suffix(".webm"), AUDIO_FILE)
    input_file = get_downloaded_file_path(DOWNLOADED_FILE)
    convert_to_wav(input_file, AUDIO_FILE)

    print("Transcribing audio...")
    transcribe_audio(AUDIO_FILE, TRANSCRIPT_FILE)
    print(f"Transcript saved to {TRANSCRIPT_FILE}")

if __name__ == "__main__":
    transcribe_youtube()
