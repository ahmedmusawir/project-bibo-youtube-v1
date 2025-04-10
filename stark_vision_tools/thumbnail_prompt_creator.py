# thumbnail_prompt_creator.py

from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import os

# === Load .env ===
load_dotenv()

# === Model Setup ===
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4.5-preview-2025-02-27")

# === File Paths ===
SUMMARY_PATH = Path("text/summary.txt")
TITLES_PATH = Path("stark_vision_tools/output/titles.json")
PROMPT_PATH = Path("stark_vision_tools/output/thumbnail_prompt.txt")

# === Load Summary ===
summary_text = SUMMARY_PATH.read_text(encoding="utf-8").strip()

# === Load Title (optional boost to prompt relevance) ===
title = ""
if TITLES_PATH.exists():
    import json
    with open(TITLES_PATH, "r", encoding="utf-8") as f:
        titles = json.load(f)
        if titles:
            title = titles[0]

# === Prompt Construction ===
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an expert AI visual designer helping a content creator produce a stunning YouTube thumbnail.\n"
        "Create a vivid, DALL-E 3-compatible prompt for a cinematic thumbnail image.\n"
        "The thumbnail should be emotionally engaging, bold, and visually clear even at small sizes.\n"
        "Avoid text overlays. Ensure a dramatic subject focus and cohesive color tone.\n"
        "Image should feel related to the video summary and title below.\n"
        "Output only the prompt to be passed to DALL-E 3 — no extra text."
    )),
    ("user", (
        f"Title: {title}\n\nSummary:\n{summary_text}"
    ))
])

# === Run Chain ===
chain = prompt | llm | StrOutputParser()
image_prompt = chain.invoke({})

# === Save Prompt ===
PROMPT_PATH.write_text(image_prompt.strip(), encoding="utf-8")

print("✅ thumbnail_prompt_creator.py complete.")
