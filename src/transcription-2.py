import os
from dotenv import load_dotenv
from openai import OpenAI
from pytube import YouTube
from pydub import AudioSegment


load_dotenv() # This line loads the .env file

client = OpenAI()

def transcribe_youtube_audio(youtube_url, project_path):
    """
    Downloads audio from a YouTube URL, transcribes it, and saves the transcript.
    
    Args:
        youtube_url (str): The URL of the YouTube video.
        project_path (str): The base path for the project to save the output file.

    Returns:
        str: The file path of the saved transcript.
    """
    print(f"-> Starting transcription for URL: {youtube_url}")
    
    # Define output paths
    raw_audio_path = os.path.join(project_path, "0_raw_audio.mp3")
    transcript_path = os.path.join(project_path, "0_transcript.txt")

    # Download audio from YouTube
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    print(f"-> Downloading audio for '{yt.title}'...")
    audio_stream.download(output_path=project_path, filename="0_raw_audio.mp3")

    # Transcribe audio using OpenAI Whisper
    print("-> Transcribing audio with Whisper API...")
    with open(raw_audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file, 
            response_format="text"
        )

    # Save the transcript to a file
    with open(transcript_path, "w") as f:
        f.write(transcript)

    print(f"✅ Transcription complete. Saved to: {transcript_path}")
    return transcript_path

# This block allows you to run the file directly for testing if needed,
# but it won't run when imported by pytest.
if __name__ == '__main__':
    # Get user input only when running this file directly
    url = input("Enter YouTube URL: ").strip()
    project_name = input("Enter project name: ").strip()
    
    # Create a dummy project path for direct execution
    dummy_project_path = os.path.join("projects", project_name)
    if not os.path.exists(dummy_project_path):
        os.makedirs(dummy_project_path)
        
    transcribe_youtube_audio(url, dummy_project_path)