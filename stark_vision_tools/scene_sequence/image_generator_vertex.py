import os
import json
import time
from pathlib import Path
from dotenv import load_dotenv

# Import the necessary Vertex AI library
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# --- 1. SETUP & INITIALIZATION ---

# Load environment variables from your .env file
# (GOOGLE_CLOUD_PROJECT, GOOGLE_APPLICATION_CREDENTIALS)
load_dotenv()

# Initialize the Vertex AI SDK. This authenticates and connects to your project.
# It only needs to be done once at the start of the script.
try:
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    vertexai.init(project=PROJECT_ID, location=REGION)
    print(f"✅ Vertex AI initialized for project: {PROJECT_ID}")
except Exception as e:
    print(f"❌ Error initializing Vertex AI: {e}")
    exit()

# --- 2. PATHS & CONFIGURATION ---

# Use the same file structure as your OpenAI script for seamless integration
PROMPT_FILE = Path("stark_vision_tools/scene_sequence/output/scene_prompts.txt")
IMAGE_DIR = Path("images/sequence_vertex") # Using a new folder to avoid overwriting old images
LOG_FILE = Path("stark_vision_tools/scene_sequence/output/image_log_vertex.json")

# Create the output directory if it doesn't already exist
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

# --- 3. LOAD MODEL ---

print("Loading Imagen model...")
# Load your preferred Imagen model once. This is much more efficient than loading it in the loop.
# "imagen-4.0-generate-preview-06-06" is a great choice for quality.
generation_model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-preview-06-06")
# generation_model = ImageGenerationModel.from_pretrained("imagen-4.0-fast-generate-preview-06-06")
# generation_model = ImageGenerationModel.from_pretrained("imagen-4.0-ultra-generate-preview-06-06")
print("✅ Model loaded successfully.")

# --- 4. READ PROMPTS ---

try:
    prompts_text = PROMPT_FILE.read_text(encoding="utf-8")
    # Filter for lines that start with a number (e.g., "1. A scene...")
    numbered_prompts = [line for line in prompts_text.strip().splitlines() if line.strip() and line.strip()[0].isdigit()]
    print(f"Found {len(numbered_prompts)} prompts to process.")
except FileNotFoundError:
    print(f"❌ Error: Prompt file not found at {PROMPT_FILE}")
    exit()

# --- 5. GENERATE IMAGES (MAIN LOOP) ---

log_data = []

for i, prompt in enumerate(numbered_prompts):
    try:
        # Extract the actual prompt text after the number (e.g., "1. ...")
        prompt_text = prompt.split(".", 1)[-1].strip()
        print(f"\n🎨 Generating image {i+1:03} → {prompt_text[:80]}...") # Print first 80 chars

        # --- This is the core Vertex AI API call ---
        response = generation_model.generate_images(
            prompt=prompt_text,
            number_of_images=1,   # Generate one image per prompt, like the old script
            aspect_ratio="16:9",  # Set to 16:9 for your YouTube videos
            add_watermark=False   # Typically set to False for production assets
        )

        # Get the first (and only) image from the response
        image = response.images[0]

        # Define the output filename and full path
        filename = f"{i+1:03}.png" # Saving as PNG for best quality
        filepath = IMAGE_DIR / filename

        # Save the image directly to the file path. No need to download from a URL.
        image.save(location=str(filepath))

        # Log the prompt and the local filepath of the saved image
        log_data.append({"index": i+1, "prompt": prompt_text, "filepath": str(filepath)})
        print(f"✅ Saved: {filepath}")

        # Vertex AI has generous rate limits, so a long sleep is often not needed.
        # time.sleep(1) # You can uncomment this if you ever run into quota issues.

    except Exception as e:
        print(f"❌ Error generating image {i+1:03}: {e}")

# --- 6. SAVE LOG ---

LOG_FILE.write_text(json.dumps(log_data, indent=2), encoding="utf-8")
print(f"\n📝 Image generation log saved: {LOG_FILE.name}")
print("🎉 All tasks complete.")
