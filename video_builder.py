from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from PIL import Image, ImageOps
import numpy as np
import os

# Constants
IMAGE_DIR = "images"
AUDIO_FILE = "audio/output-gpt-4.5.mp3"
VIDEO_OUTPUT = "output/video.mp4"
VIDEO_SIZE = (1920, 1080)
FADE_DURATION = 1  # seconds

# Time per image (in seconds)
DURATION_PER_IMAGE = 7

# Collect image clips
image_clips = []
width, height = VIDEO_SIZE

for filename in sorted(os.listdir(IMAGE_DIR)):
    filepath = os.path.join(IMAGE_DIR, filename)
    try:
        img = Image.open(filepath)
        img = ImageOps.exif_transpose(img)
        img = img.resize((width, height), resample=Image.LANCZOS)

        # Convert to NumPy array and pass to ImageClip
        img_array = np.array(img)
        clip = ImageClip(img_array).set_duration(DURATION_PER_IMAGE)
        clip = clip.fadein(FADE_DURATION).fadeout(FADE_DURATION)
        image_clips.append(clip)
    except Exception as e:
        print(f"⚠️ Skipping {filename} due to error: {e}")

# Final fallback check
if not image_clips:
    raise RuntimeError("No valid images found to create video.")

# Create final video clip
video = concatenate_videoclips(image_clips, method="compose")

# Add background narration
if os.path.exists(AUDIO_FILE):
    audio = AudioFileClip(AUDIO_FILE)
    video = video.set_audio(audio).subclip(0, audio.duration)

# Ensure output directory exists
os.makedirs(os.path.dirname(VIDEO_OUTPUT), exist_ok=True)

# Export video
video.write_videofile(VIDEO_OUTPUT, fps=24)

print("\n✅ Video rendering complete! Check:", VIDEO_OUTPUT)
