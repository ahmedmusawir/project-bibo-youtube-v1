from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
from PIL import Image, ImageOps
import os

# Constants
IMAGE_DIR = "images"
AUDIO_FILE = "audio/output-gpt-4.5.mp3"
VIDEO_OUTPUT = "output/video.mp4"
VIDEO_SIZE = (1920, 1080)
FADE_DURATION = 1  # seconds

# Load audio to get its duration
audio = AudioFileClip(AUDIO_FILE)
audio_duration = audio.duration

# Prepare image clips
image_clips = []
image_files = sorted(os.listdir(IMAGE_DIR))

# Calculate dynamic duration per image
num_images = len(image_files)
if num_images == 0:
    raise RuntimeError("No images found in the images directory.")

duration_per_image = audio_duration / num_images

width, height = VIDEO_SIZE

for filename in image_files:
    filepath = os.path.join(IMAGE_DIR, filename)
    try:
        img = Image.open(filepath)
        img = ImageOps.exif_transpose(img)
        img = img.resize((width, height), resample=Image.LANCZOS)
        img.save(filepath)

        clip = ImageClip(filepath).set_duration(duration_per_image)
        clip = clip.fadein(FADE_DURATION).fadeout(FADE_DURATION)
        image_clips.append(clip)
    except Exception as e:
        print(f"Skipping {filename} due to error: {e}")

# Final check
if not image_clips:
    raise RuntimeError("No valid image clips could be created.")

# Concatenate image clips into a video
video = concatenate_videoclips(image_clips, method="compose")
video = video.set_audio(audio)

# Ensure output directory exists
os.makedirs(os.path.dirname(VIDEO_OUTPUT), exist_ok=True)

# Write the final video
video.write_videofile(VIDEO_OUTPUT, fps=24)

print("\nVideo rendering complete! Check:", VIDEO_OUTPUT)
