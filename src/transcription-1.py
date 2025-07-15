from pathlib import Path
from openai import OpenAI
from yt_dlp import YoutubeDL
from pydub import AudioSegment
import os
from dotenv import load_dotenv

# Ask user for the YouTube URL interactively
youtube_url = input("Enter YouTube URL: ").strip()

# Load API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Constants
# youtube_url = "https://youtu.be/xQUPXeYGsYk"
RAW_DIR = Path("raw")
TEXT_DIR = Path("text")
RAW_DIR.mkdir(exist_ok=True)
TEXT_DIR.mkdir(exist_ok=True)
AUDIO_FILE = RAW_DIR / "audio.mp3"
TRANSCRIPT_FILE = TEXT_DIR / "transcript.txt"

# === Download MP3 ===
def download_audio(url: str, output_path: Path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path.with_suffix('')),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# === Split MP3 into 10-minute chunks ===
def split_audio_chunks(mp3_path: Path, chunk_dir: Path, chunk_length_ms: int = 600_000):
    audio = AudioSegment.from_mp3(mp3_path)
    chunks = []
    for i in range(0, len(audio), chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        chunk_path = chunk_dir / f"chunk_{i//chunk_length_ms + 1}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)
    return chunks

# === Transcribe Each Chunk ===
def transcribe_chunks(chunk_paths, output_txt: Path):
    with output_txt.open("w", encoding="utf-8") as f:
        for idx, chunk_path in enumerate(chunk_paths, 1):
            print(f"Transcribing chunk {idx}...")
            with open(chunk_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            f.write(f"[Chunk {idx}]\n{transcript.text}\n\n")

# === Main ===
def transcribe_youtube():
    print("Downloading audio...")
    download_audio(youtube_url, AUDIO_FILE)

    print("Splitting into chunks...")
    chunk_paths = split_audio_chunks(AUDIO_FILE, RAW_DIR)

    print("Transcribing chunks...")
    transcribe_chunks(chunk_paths, TRANSCRIPT_FILE)

    print(f"Transcript saved to {TRANSCRIPT_FILE}")

if __name__ == "__main__":
    transcribe_youtube()
