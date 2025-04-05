from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
from pydub import AudioSegment
import os
import math

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# File paths
SUMMARY_PATH = Path("text/summary.txt")
AUDIO_DIR = Path("audio")
OUTPUT_PATH = AUDIO_DIR / "output.mp3"
CHUNK_LIMIT = 3500

def split_text(text, limit):
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 < limit:
            current_chunk += para + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def synthesize_summary():
    text = SUMMARY_PATH.read_text(encoding="utf-8")
    chunks = split_text(text, CHUNK_LIMIT)

    AUDIO_DIR.mkdir(exist_ok=True)
    combined = AudioSegment.empty()

    for i, chunk in enumerate(chunks):
        temp_path = AUDIO_DIR / f"chunk_{i+1}.mp3"
        print(f"\n Synthesizing chunk {i+1}/{len(chunks)}...")
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            input=chunk
        ) as response:
            response.stream_to_file(temp_path)
        combined += AudioSegment.from_mp3(temp_path)

    combined.export(OUTPUT_PATH, format="mp3")
    print(f"\n✅ Final audio saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    synthesize_summary()