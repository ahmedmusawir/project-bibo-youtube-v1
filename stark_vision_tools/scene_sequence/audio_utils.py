# audio_utils.py

from pydub.utils import mediainfo
from pathlib import Path

def get_audio_duration(audio_path_str: str) -> float:
    """
    Returns the duration of the audio file in seconds.
    Also prints the human-readable format (mm:ss)
    """
    audio_path = Path(audio_path_str)

    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path_str}")

    info = mediainfo(str(audio_path))
    duration = float(info['duration'])

    minutes = int(duration // 60)
    seconds = int(duration % 60)
    print(f"🎧 Audio duration is {minutes} min {seconds} sec")

    return duration


if __name__ == "__main__":
    try:
        duration = get_audio_duration("audio/output.mp3")
        print(f"✅ Duration in seconds: {duration:.2f}")
    except Exception as e:
        print(f"❌ Error: {e}")
