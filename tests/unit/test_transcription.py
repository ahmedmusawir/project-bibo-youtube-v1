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
@patch('src.transcription._download_audio_with_yt_dlp')
def test_transcribe_youtube_audio_mocked(mock_download, mock_openai_client, test_project_dir):
    """
    Tests the transcription process with yt-dlp and OpenAI mocked to ensure
    the function works correctly without making real network calls.
    """
    # 1. Setup Mocks
    # Mock for yt-dlp downloader
    def create_dummy_audio_file(url, output_path):
        with open(output_path, "w") as f:
            f.write("dummy audio data")

    mock_download.side_effect = create_dummy_audio_file

    # Mock for OpenAI client
    mock_transcript_text = "This is a mocked transcript."
    mock_openai_client.audio.transcriptions.create.return_value = mock_transcript_text

    # 2. Execution
    transcript_file_path = transcribe_youtube_audio(TEST_YOUTUBE_URL, test_project_dir)

    # 3. Verification
    # Verify yt-dlp mock was called as expected
    raw_audio_path = os.path.join(test_project_dir, "0_raw_audio.mp3")
    mock_download.assert_called_once_with(TEST_YOUTUBE_URL, raw_audio_path)

    # Verify OpenAI mock was called as expected
    mock_openai_client.audio.transcriptions.create.assert_called_once()
    
    # Verify the output file path and content
    expected_path = os.path.join(test_project_dir, "0_transcript.txt")
    assert transcript_file_path == expected_path
    assert os.path.exists(transcript_file_path)
    
    with open(transcript_file_path, "r") as f:
        content = f.read()
    assert content == mock_transcript_text