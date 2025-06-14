import os
from dotenv import load_dotenv
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# --- SETUP ---
load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
vertexai.init(project=PROJECT_ID, location=REGION)

# --- NEW: Define an output directory ---
OUTPUT_DIR = "GENERATED_IMAGES"
# Create the directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# PROMPT = "A photorealistic, high-resolution scene of a massive, futuristic data center labeled \"StarGate\" in Abilene, Texas, glowing with electricity and illuminated by realistic lighting at dusk. Giant power lines hum with energy, and towering digital screens clearly display: \"1.2 GW – Enough to power 750,000 homes.\" In the background, a map of the U.S. shows a rising gauge: \"Data Centers: 8% of U.S. electricity by 2035.\" All text is crystal-clear and without spelling mistakes."

# PROMPT = "A photorealistic, high-resolution scene showing a dramatic landscape: on one side, gleaming solar panels and wind turbines under a bright sky, and on the other, a smoky fossil fuel power plant emitting plumes. In the foreground, bold text reads “Sustainability, Climate Goals, and True Costs” in clear, flawless lettering. Realistic lighting emphasizes the sharp contrast between renewables and fossil fuels."

PROMPT = "A photorealistic scene of Lockmiller standing beside a futuristic, modular mobile data center powered by flared natural gas flames in a remote oil field at dusk, glowing servers visible through open panels, with clear text “AI-driven Finance & Crypto Innovation” in bold, flawless lettering across the scene."

print(f"Project: {PROJECT_ID}, Region: {REGION}")
print("Loading Imagen model...")

# --- MODEL LOADING ---
# Fast but not very relaiable for prompting
# generation_model = ImageGenerationModel.from_pretrained("imagen-4.0-fast-generate-preview-06-06")
# Very reliable for prompting
generation_model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-preview-06-06")

print("Model loaded. Generating images...")

# --- IMAGE GENERATION ---
response = generation_model.generate_images(
    prompt=PROMPT,
    number_of_images=4,
    aspect_ratio="16:9",
    add_watermark=True
)

print(f"Successfully generated {len(response.images)} images.")

# --- SAVING IMAGES ---
for i, image in enumerate(response.images):
    # --- NEW: Join the directory and filename ---
    filename = f"stargate_output_{i+1}.png"
    output_path = os.path.join(OUTPUT_DIR, filename)
    
    image.save(location=output_path)
    print(f"✅ Saved image to: {output_path}")