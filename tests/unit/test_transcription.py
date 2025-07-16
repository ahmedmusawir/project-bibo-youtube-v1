import os
import pytest
from unittest.mock import patch, MagicMock

from src.transcription import transcribe_youtube_audio

# Define a dummy URL for testing
TEST_YOUTUBE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

@patch('src.transcription.client')
@patch('src.transcription._download_audio_to_temp')
def test_transcribe_youtube_audio_unit(
    mock_downloader,
    mock_openai_client,
    tmp_path # Pytest's built-in fixture for a temporary directory
):
    """
    Unit test for transcribe_youtube_audio.
    Mocks the downloader and the OpenAI API call.
    Uses pytest's tmp_path fixture to avoid creating files in the project directory.
    """
    # 1. Setup Mocks and Temporary Files
    # tmp_path provides a Path object to a temporary directory
    test_output_path = tmp_path / "transcript.txt"
    dummy_audio_path = tmp_path / "dummy_audio.mp3"

    # Mock the downloader to return a path to our fake audio file
    with open(dummy_audio_path, "w") as f:
        f.write("dummy audio")
    mock_downloader.return_value = str(dummy_audio_path)

    # Mock the OpenAI client
    mock_transcript_text = "This is a mocked transcript."
    mock_openai_client.audio.transcriptions.create.return_value = mock_transcript_text

    # 2. Execution
    # Call the function with the test URL and the temporary output path
    result_path = transcribe_youtube_audio(TEST_YOUTUBE_URL, str(test_output_path))

    # 3. Verification
    # Check that the downloader and OpenAI client were called
    mock_downloader.assert_called_once_with(TEST_YOUTUBE_URL)
    mock_openai_client.audio.transcriptions.create.assert_called_once()

    # Check that the function returned the correct path
    assert result_path == str(test_output_path)

    # Check that the output file was created with the correct content
    assert os.path.exists(test_output_path)
    with open(test_output_path, "r") as f:
        content = f.read()
    assert content == mock_transcript_text
