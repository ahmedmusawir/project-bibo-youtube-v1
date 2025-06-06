# prompt_generator.py

from pathlib import Path
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

# === Load .env ===
load_dotenv()

# === Config ===
SUMMARY_PATH = Path("text/summary.txt")
PROMPT_OUTPUT_PATH = Path("stark_vision_tools/scene_sequence/output/scene_prompts.txt")

# === Model Setup ===
llm = ChatOpenAI(model="gpt-4.1")

# === Prompt Template ===
prompt_template = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a visual scene director for a cinematic explainer video.\n"
        "Your job is to create a list of {num_images} vivid, distinct, and sequential visual prompts.\n"
        "These will be used to generate AI images that tell the story of the video based on the summary.\n"
        "Each prompt should focus on a specific visual moment, scene, or detail relevant to the topic.\n"
        "They should follow a logical flow and show progression — from intro to climax to conclusion.\n"
        "Avoid repetition. Use creative, emotionally engaging phrasing.\n"
        "Number each prompt (e.g., 1. … 2. …) and keep each under 40 words.\n"
        "Output only the list of prompts — no explanations."
    )),
    ("user", "{summary}")
])

# === Function ===
def generate_scene_prompts(summary: str, num_images: int) -> str:
    chain = prompt_template | llm | StrOutputParser()
    return chain.invoke({"summary": summary, "num_images": num_images})


# === CLI Test ===
if __name__ == "__main__":
    try:
        from sequence_image_creator import calculate_num_images

        summary_text = SUMMARY_PATH.read_text(encoding="utf-8").strip()
        num_images = calculate_num_images("audio/output.mp3")

        print(f"📜 Generating {num_images} prompts from summary...")
        output = generate_scene_prompts(summary_text, num_images)

        PROMPT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
        PROMPT_OUTPUT_PATH.write_text(output, encoding="utf-8")
        print(f"✅ scene_prompts.txt created with {num_images} prompts.")

    except Exception as e:
        print(f"❌ Error: {e}")
