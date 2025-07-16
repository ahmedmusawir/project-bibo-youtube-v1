import os
import shutil
from unittest.mock import patch, MagicMock

from src.text_to_speech import text_to_speech

# Define test constants
TEST_PROJECT_NAME = "unit_test_tts_project"
TEST_PROJECT_PATH = os.path.join("projects", TEST_PROJECT_NAME)
TEST_SUMMARY_PATH = os.path.join(TEST_PROJECT_PATH, "1_summary.txt")

def setup_module():
    """Create a dummy summary file for testing."""
    if os.path.exists(TEST_PROJECT_PATH):
        shutil.rmtree(TEST_PROJECT_PATH)
    os.makedirs(TEST_PROJECT_PATH)
    with open(TEST_SUMMARY_PATH, "w") as f:
        f.write("This is a test summary for text to speech conversion.")

def teardown_module():
    """Clean up the test directory."""
    shutil.rmtree(TEST_PROJECT_PATH)

@patch('src.text_to_speech.OpenAI')
def test_text_to_speech_with_mock(mock_openai):
    """
    Tests the text_to_speech function by mocking the OpenAI API call.
    """
    # 1. Setup the mock
    mock_client_instance = mock_openai.return_value
    # Mock the speech.create().write_to_file() chain
    mock_speech = MagicMock()
    mock_client_instance.audio.speech.create.return_value = mock_speech

    # 2. Execution
    audio_file_path = text_to_speech(TEST_SUMMARY_PATH, TEST_PROJECT_PATH)

    # 3. Verification
    expected_path = os.path.join(TEST_PROJECT_PATH, "2_audio.mp3")
    assert audio_file_path == expected_path
    
    # Verify that the API was called with the correct parameters
    mock_client_instance.audio.speech.create.assert_called_once()
    
    # Verify that the method to save the file was called
    mock_speech.write_to_file.assert_called_once_with(expected_path)