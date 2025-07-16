import os
import pytest
from unittest.mock import patch, MagicMock

from src.text_to_speech import synthesize_speech, split_text

# A long string to test the chunking logic
TEST_SUMMARY_CONTENT = "This is a test summary. " * 300

# A custom mock class to replace pydub.AudioSegment
# This gives us explicit control over the behavior, avoiding MagicMock complexity.
class FakeAudioSegment:
    _instance = None

    def __init__(self, *args, **kwargs):
        self.export_was_called = False
        self.exported_to_path = None

    def __add__(self, other):
        # When chunks are added, just return the same shared instance.
        return self.__class__._instance

    def export(self, out_f, format):
        # This is the key method we want to verify.
        instance = self.__class__._instance
        instance.export_was_called = True
        instance.exported_to_path = out_f
        # Create a dummy file to satisfy os.path.exists checks in the test.
        with open(out_f, 'w') as f:
            f.write("dummy audio data")

    @classmethod
    def empty(cls):
        # Always return the same, single instance to track calls across the function.
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def from_mp3(cls, file_path):
        # When loading a chunk, it also returns the same shared instance.
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

@patch('src.text_to_speech.client')
# Here, we replace the real AudioSegment with our FakeAudioSegment
@patch('src.text_to_speech.AudioSegment', new=FakeAudioSegment)
def test_synthesize_speech_unit_with_fake_class(
    mock_openai_client,
    tmp_path
):
    """
    Unit test for synthesize_speech using a custom fake class for AudioSegment.
    This approach is more explicit and reliable than complex MagicMock configuration.
    """
    # 1. Setup
    temp_summary_path = tmp_path / "summary.txt"
    temp_audio_path = tmp_path / "audio.mp3"
    temp_summary_path.write_text(TEST_SUMMARY_CONTENT)

    # Mock the OpenAI API response
    mock_response = MagicMock()
    mock_openai_client.audio.speech.with_streaming_response.create.return_value = mock_response

    # 2. Execution
    result_path = synthesize_speech(str(temp_summary_path), str(temp_audio_path))

    # 3. Verification
    # Verify the text was split correctly and the API was called for each chunk
    chunks = split_text(TEST_SUMMARY_CONTENT, 4096)
    assert mock_openai_client.audio.speech.with_streaming_response.create.call_count == len(chunks)

    # Verify that our fake export method was called by checking the instance
    fake_segment_instance = FakeAudioSegment._instance
    assert fake_segment_instance.export_was_called is True
    assert fake_segment_instance.exported_to_path == str(temp_audio_path)

    # Final check on the return value and file existence
    assert result_path == str(temp_audio_path)
    assert os.path.exists(result_path)

    # Cleanup the class attribute to ensure test isolation
    FakeAudioSegment._instance = None