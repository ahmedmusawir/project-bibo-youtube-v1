# sequence_image_creator.py

# from stark_vision_tools.scene_sequence.audio_utils import get_audio_duration
from audio_utils import get_audio_duration

SECONDS_PER_IMAGE = 12
AUDIO_FILE_PATH = "audio/output.mp3"


def calculate_num_images(audio_path: str, seconds_per_image: int = SECONDS_PER_IMAGE) -> int:
    duration = get_audio_duration(audio_path)
    num_images = round(duration / seconds_per_image)
    return num_images


if __name__ == "__main__":
    try:
        total_images = calculate_num_images(AUDIO_FILE_PATH)
        print(f"🎬 Audio is {AUDIO_FILE_PATH} → Generate {total_images} scene images")
    except Exception as e:
        print(f"❌ Error: {e}")
