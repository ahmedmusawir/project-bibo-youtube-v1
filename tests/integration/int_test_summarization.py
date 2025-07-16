import os
import shutil
from unittest.mock import patch
from pathlib import Path

# Import the function to be tested
from src.summarization import summarize_transcript

# Define test constants for a temporary directory
LIVE_TEST_PROJECT_NAME = "live_test_summary"
LIVE_TEST_PROJECT_PATH = os.path.join("projects", LIVE_TEST_PROJECT_NAME)

# Define the paths for the temporary files
# These need to be Path objects to match the source code's type
LIVE_TRANSCRIPT_PATH = Path(os.path.join(LIVE_TEST_PROJECT_PATH, "transcript.txt"))
LIVE_SUMMARY_PATH = Path(os.path.join(LIVE_TEST_PROJECT_PATH, "summary.txt"))

def run_live_summary_test():
    """
    Performs a real summarization to verify the live service.
    This test makes a real API call to Anthropic.
    """
    print("\n--- Starting Live Summarization Test ---")
    
    # 1. Setup: Create a clean directory and a dummy transcript
    if os.path.exists(LIVE_TEST_PROJECT_PATH):
        shutil.rmtree(LIVE_TEST_PROJECT_PATH)
    os.makedirs(LIVE_TEST_PROJECT_PATH)
    with open(LIVE_TRANSCRIPT_PATH, "w") as f:
        # A simple but meaningful sentence for a real summary
        f.write("Artificial intelligence is transforming the world.")
        
    try:
        # 2. Execution: Use patch to temporarily change the file paths in the source module
        with patch('src.summarization.TRANSCRIPT_PATH', LIVE_TRANSCRIPT_PATH),             patch('src.summarization.SUMMARY_PATH', LIVE_SUMMARY_PATH):
            
            summarize_transcript()

        # 3. Verification: Check that a summary file was created and is not empty
        assert os.path.exists(LIVE_SUMMARY_PATH)
        assert os.path.getsize(LIVE_SUMMARY_PATH) > 0
        
        with open(LIVE_SUMMARY_PATH, "r") as f:
            summary_content = f.read()
            print(f"Generated Summary Preview: {summary_content[:100]}...")

        print("\n--- ✅ Live Test Successful ---")

    except Exception as e:
        print(f"\n--- ❌ Live Test Failed ---")
        print(f"An error occurred: {e}")
    finally:
        # 4. Teardown: Clean up the created files
        if os.path.exists(LIVE_TEST_PROJECT_PATH):
            shutil.rmtree(LIVE_TEST_PROJECT_PATH)
            print("--- Test cleanup complete. ---")

if __name__ == "__main__":
    run_live_summary_test()
