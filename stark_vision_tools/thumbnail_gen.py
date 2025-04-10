# thumbnail_gen.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

# === Load API Key ===
load_dotenv()
client = OpenAI()

# === Paths ===
PROMPT_PATH = Path("stark_vision_tools/output/thumbnail_prompt.txt")
THUMBNAIL_PATH = Path("stark_vision_tools/output/thumbnail.jpg")

# === Read Prompt ===
prompt = PROMPT_PATH.read_text(encoding="utf-8").strip()

# === Generate Image ===
response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1792x1024",
    style="vivid",
    quality="hd",
    n=1,
    response_format="url",
)

# === Download the image ===
import requests
image_url = response.data[0].url
img_data = requests.get(image_url).content

with open(THUMBNAIL_PATH, "wb") as handler:
    handler.write(img_data)

print("✅ thumbnail_gen.py complete. Thumbnail saved as thumbnail.jpg")