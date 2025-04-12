from moviepy import ImageClip, concatenate_videoclips, AudioFileClip
from moviepy import vfx
from PIL import Image, ImageOps
from PIL.Image import Resampling
import numpy as np
import os

# Constants
IMAGE_DIR = "images/sequence"
AUDIO_FILE = "audio/output.mp3"
VIDEO_OUTPUT = "output/video.mp4"
VIDEO_SIZE = (1920, 1080)
FADE_DURATION = 1  # seconds
DURATION_PER_IMAGE = 7  # seconds

# Collect image clips
image_clips = []
width, height = VIDEO_SIZE

for idx, filename in enumerate(sorted(os.listdir(IMAGE_DIR))):
    filepath = os.path.join(IMAGE_DIR, filename)
    try:
        img = Image.open(filepath).convert("RGB")
        img = ImageOps.exif_transpose(img)
        img = img.resize((width, height), resample=Resampling.LANCZOS)

        # Convert to NumPy array and pass to ImageClip
        img_array = np.array(img)
        clip = ImageClip(img_array)
        clip = clip.with_duration(DURATION_PER_IMAGE)
        clip = clip.with_position(lambda t: ("center", int(10 * t)))
        clip = clip.with_effects([
            vfx.Resize(lambda t: 1 + 0.05 * t),
            vfx.FadeIn(FADE_DURATION),
            vfx.FadeOut(FADE_DURATION),
        ])
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
    audio = audio.subclipped(0, video.duration)
    video = video.with_audio(audio)

# Ensure output directory exists
os.makedirs(os.path.dirname(VIDEO_OUTPUT), exist_ok=True)

# Export video
video.write_videofile(VIDEO_OUTPUT, fps=24)

print("\n🎞️  Video rendering complete! Check:", VIDEO_OUTPUT)
