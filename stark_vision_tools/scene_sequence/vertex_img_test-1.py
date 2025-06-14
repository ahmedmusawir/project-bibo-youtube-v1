import os
from dotenv import load_dotenv
from google.cloud import aiplatform
# from google.cloud.aiplatform.gapic.schema import predict

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")         # Put this in your .env
REGION = os.getenv("GOOGLE_CLOUD_REGION", "us-central1")  # Optional, fallback default

# Initialize Vertex client
aiplatform.init(project=PROJECT_ID, location=REGION)
print("Vertex AI initialized.")

# Model Names for Looping
MODEL_NAMES = {
    "Ultra_6c": "projects/{}/locations/{}/publishers/google/models/imagen-4-ultra".format(PROJECT_ID, REGION),
    "Standard_4c": "projects/{}/locations/{}/publishers/google/models/imagen-4".format(PROJECT_ID, REGION),
    "Fast_2c": "projects/{}/locations/{}/publishers/google/models/imagen-4-fast".format(PROJECT_ID, REGION)
}

# The image prompts
PROMPT = "A photorealistic, high-resolution scene of a massive, futuristic data center labeled \"StarGate\" in Abilene, Texas, glowing with electricity and illuminated by realistic lighting at dusk. Giant power lines hum with energy, and towering digital screens clearly display: \"1.2 GW – Enough to power 750,000 homes.\" In the background, a map of the U.S. shows a rising gauge: \"Data Centers: 8% of U.S. electricity by 2035.\" All text is crystal-clear and without spelling mistakes."

# The image gen function
def generate_vertex_image(model_name, prompt, output_filename):
    from google.cloud import aiplatform_v1

    # Use PredictionService client with regional endpoint
    endpoint = f"{REGION}-aiplatform.googleapis.com"
    client = aiplatform_v1.PredictionServiceClient(client_options={"api_endpoint": endpoint})

    # Build the instance input for Imagen 4
    instance = {
        "prompt": prompt,
    }

    instances = [instance]
    parameters = {}

    # Actually run the prediction
    response = client.predict(
        endpoint=model_name,
        instances=instances,
        parameters=parameters,
    )

    # Get the image bytes from the response
    image_base64 = response.predictions[0]["bytesBase64Encoded"]
    import base64
    image_bytes = base64.b64decode(image_base64)

    with open(output_filename, "wb") as img_file:
        img_file.write(image_bytes)
    print(f"Saved: {output_filename}")

# Generating images
print("Generating images...")
for label, model_path in MODEL_NAMES.items():
    filename = f"test_output_{label.lower()}.jpg"
    print(f"Generating image with Imagen 4 {label} ...")
    generate_vertex_image(model_path, PROMPT, filename)

