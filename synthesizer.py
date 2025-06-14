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

    print(f"\nReading the Summary Text ... ")
    text = SUMMARY_PATH.read_text(encoding="utf-8")

    print(f"\nSplitting Text into Chunks ...")
    chunks = split_text(text, CHUNK_LIMIT)

    AUDIO_DIR.mkdir(exist_ok=True)
    combined = AudioSegment.empty()

    print(f"\nStarting to Synthesize Chunks ...")

    for i, chunk in enumerate(chunks):
        temp_path = AUDIO_DIR / f"chunk_{i+1}.mp3"
        print(f"\n Synthesizing chunk {i+1}/{len(chunks)}...")
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            # model="tts-1",
            # voice="onyx",
            voice="alloy",
            instructions="Speak in a cheerful and positive tone. Show excitement when necessary! Remember, you are the voice of a super engaging and popular YouTube video!!",
            input=chunk
        ) as response:
            response.stream_to_file(temp_path)
        combined += AudioSegment.from_mp3(temp_path)

    combined.export(OUTPUT_PATH, format="mp3")
    print(f"\nFinal audio saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    synthesize_summary()