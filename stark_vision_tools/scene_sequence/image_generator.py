# image_generator.py

import time
import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

# === Load API key ===
load_dotenv()
client = OpenAI()

# === Paths ===
PROMPT_FILE = Path("stark_vision_tools/scene_sequence/output/scene_prompts.txt")
IMAGE_DIR = Path("images/sequence")
LOG_FILE = Path("stark_vision_tools/scene_sequence/output/image_log.json")

# === Read Prompts ===
prompts = PROMPT_FILE.read_text(encoding="utf-8").strip().splitlines()
numbered_prompts = [line for line in prompts if line.strip() and line.strip()[0].isdigit()]

# === Create output dir ===
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# === Generate Images ===
log_data = []

for i, prompt in enumerate(numbered_prompts):
    try:
        prompt_text = prompt.split(".", 1)[-1].strip()
        print(f"🎨 Generating image {i+1:03} → {prompt_text}")

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            size="1792x1024",
            style="vivid",
            quality="hd",
            n=1,
            response_format="url",
        )

        url = response.data[0].url
        image_data = requests.get(url).content

        filename = f"{i+1:03}.jpg"
        filepath = IMAGE_DIR / filename

        with open(filepath, "wb") as f:
            f.write(image_data)

        log_data.append({"index": i+1, "prompt": prompt_text, "url": url})
        print(f"✅ Saved: {filename}")

        time.sleep(1.5)  # slight delay to avoid rate limits

    except Exception as e:
        print(f"❌ Error generating image {i+1:03}: {e}")

# === Save Log ===
import json
LOG_FILE.write_text(json.dumps(log_data, indent=2), encoding="utf-8")
print(f"📝 Image generation log saved: {LOG_FILE.name}")
