import os
from dotenv import load_dotenv
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# --- SETUP ---
load_dotenv()
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
vertexai.init(project=PROJECT_ID, location=REGION)

PROMPT = "A photorealistic, high-resolution scene of a massive, futuristic data center labeled \"StarGate\" in Abilene, Texas, glowing with electricity and illuminated by realistic lighting at dusk. Giant power lines hum with energy, and towering digital screens clearly display: \"1.2 GW – Enough to power 750,000 homes.\" In the background, a map of the U.S. shows a rising gauge: \"Data Centers: 8% of U.S. electricity by 2035.\" All text is crystal-clear and without spelling mistakes."

print(f"Project: {PROJECT_ID}, Region: {REGION}")
print("Loading Imagen model...")

# --- MODEL LOADING ---
generation_model = ImageGenerationModel.from_pretrained("imagen-4.0-generate-preview-05-20")

print("Model loaded. Generating images...")

# --- IMAGE GENERATION ---
# The watermark instruction is moved HERE, where it belongs.
response = generation_model.generate_images(
    prompt=PROMPT,
    number_of_images=4,
    aspect_ratio="1:1",
    add_watermark=True 
)

# Access the list of images using the .images property
print(f"Successfully generated {len(response.images)} images.")

# --- SAVING IMAGES ---
# Loop through the list inside response.images
for i, image in enumerate(response.images):
    output_filename = f"stargate_output_{i+1}.png"
    # The illegal 'include_watermark' parameter is REMOVED from the save function.
    image.save(location=output_filename) 
    print(f"✅ Saved image to: {output_filename}")