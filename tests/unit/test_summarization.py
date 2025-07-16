import os
import shutil
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Import the function to be tested
from src.summarization import summarize_transcript

# Define test constants for a temporary directory
TEST_PROJECT_NAME = "unit_test_summary_project_langchain"
TEST_PROJECT_PATH = os.path.join("projects", TEST_PROJECT_NAME)
TEST_TRANSCRIPT_PATH_STR = os.path.join(TEST_PROJECT_PATH, "transcript.txt")
TEST_SUMMARY_PATH_STR = os.path.join(TEST_PROJECT_PATH, "summary.txt")

# Convert to Path objects for patching, as used in the source
TEST_TRANSCRIPT_PATH = Path(TEST_TRANSCRIPT_PATH_STR)
TEST_SUMMARY_PATH = Path(TEST_SUMMARY_PATH_STR)


@pytest.fixture
def setup_teardown_test_files():
    """Create dummy files and directories for testing and clean up afterward."""
    # Setup
    os.makedirs(TEST_PROJECT_PATH, exist_ok=True)
    with open(TEST_TRANSCRIPT_PATH, "w") as f:
        f.write("This is a dummy transcript for testing.")
    
    yield # This is where the test runs

    # Teardown
    shutil.rmtree(TEST_PROJECT_PATH)

# We need to patch all external dependencies and file paths within the module
@patch('src.summarization.create_stuff_documents_chain')
@patch('src.summarization.TextLoader')
@patch('src.summarization.ChatAnthropic')
@patch('src.summarization.TRANSCRIPT_PATH', new=TEST_TRANSCRIPT_PATH)
@patch('src.summarization.SUMMARY_PATH', new=TEST_SUMMARY_PATH)
def test_summarize_transcript_with_langchain_mock(
    mock_chat_anthropic, 
    mock_text_loader, 
    mock_create_chain,
    setup_teardown_test_files # Use the fixture
):
    """
    Tests the summarize_transcript function by mocking the entire LangChain chain.
    """
    # 1. Setup Mocks
    # Mock the loader
    mock_text_loader.return_value.load.return_value = [MagicMock(page_content="dummy content")]

    # Mock the chain and its invocation
    mock_chain_instance = MagicMock()
    mock_chain_instance.invoke.return_value = "This is the mocked summary from the chain."
    mock_create_chain.return_value = mock_chain_instance

    # 2. Execution
    summarize_transcript()

    # 3. Verification
    # Ensure the loader was called with the correct (patched) path
    mock_text_loader.assert_called_once_with(str(TEST_TRANSCRIPT_PATH))

    # Ensure the chain was created and invoked
    mock_create_chain.assert_called_once()
    mock_chain_instance.invoke.assert_called_once()

    # Check that the summary file was created with the mocked content
    assert os.path.exists(TEST_SUMMARY_PATH)
    with open(TEST_SUMMARY_PATH, "r") as f:
        content = f.read()
    assert content == "This is the mocked summary from the chain."
