import os
import shutil
import pytest
from unittest.mock import patch, MagicMock

from src.transcription import transcribe_youtube_audio

TEST_YOUTUBE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Dummy URL
TEST_PROJECT_NAME = "test_transcription_project_mocked"
TEST_PROJECT_PATH = os.path.join("projects", TEST_PROJECT_NAME)


@pytest.fixture
def test_project_dir():
    """A fixture to create and clean up a test directory."""
    if os.path.exists(TEST_PROJECT_PATH):
        shutil.rmtree(TEST_PROJECT_PATH)
    os.makedirs(TEST_PROJECT_PATH)
    
    yield TEST_PROJECT_PATH
    
    shutil.rmtree(TEST_PROJECT_PATH)


@patch('src.transcription.client')
@patch('src.transcription.YouTube')
def test_transcribe_youtube_audio_mocked(mock_youtube, mock_openai_client, test_project_dir):
    """
    Tests the transcription process with pytube and OpenAI mocked to ensure
    the function works correctly without making real network calls.
    """
    # 1. Setup Mocks
    # Mock for pytube (YouTube)
    mock_yt_instance = MagicMock()
    mock_yt_instance.title = "Mocked Video Title"
    mock_stream = MagicMock()
    
    # The download method needs to create a dummy file for the next step to open.
    def create_dummy_audio_file(output_path, filename):
        # Use the project path provided by the fixture
        audio_file_path = os.path.join(output_path, filename)
        with open(audio_file_path, "w") as f:
            f.write("dummy audio data")
        return audio_file_path # download() doesn't return anything, but this is for clarity

    mock_stream.download.side_effect = create_dummy_audio_file
    mock_yt_instance.streams.filter.return_value.first.return_value = mock_stream
    mock_youtube.return_value = mock_yt_instance

    # Mock for OpenAI client
    mock_transcript_text = "This is a mocked transcript."
    mock_openai_client.audio.transcriptions.create.return_value = mock_transcript_text

    # 2. Execution
    transcript_file_path = transcribe_youtube_audio(TEST_YOUTUBE_URL, test_project_dir)

    # 3. Verification
    # Verify YouTube mock was called as expected
    mock_youtube.assert_called_once_with(TEST_YOUTUBE_URL)
    mock_yt_instance.streams.filter.assert_called_once_with(only_audio=True)
    mock_stream.download.assert_called_once_with(output_path=test_project_dir, filename="0_raw_audio.mp3")

    # Verify OpenAI mock was called as expected
    mock_openai_client.audio.transcriptions.create.assert_called_once()
    
    # Verify the output file path and content
    expected_path = os.path.join(test_project_dir, "0_transcript.txt")
    assert transcript_file_path == expected_path
    assert os.path.exists(transcript_file_path)
    
    with open(transcript_file_path, "r") as f:
        content = f.read()
    assert content == mock_transcript_text