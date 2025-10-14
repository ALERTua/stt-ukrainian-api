"""Test script for STT API transcription endpoint."""

import requests

def test_transcription(audio_file_path: str, api_url: str = "http://127.0.0.1:8000"):
    """Test the transcription endpoint."""
    with open(audio_file_path, "rb") as f:
        response = requests.post(
            f"{api_url}/v1/audio/transcriptions",
            files={"file": f},
            data={
                "model": "whisper-1",
                "response_format": "json"
            }
        )

    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python test_transcription.py <audio_file_path>")
        sys.exit(1)

    test_transcription(sys.argv[1])
