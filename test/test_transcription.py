"""Test script for STT API transcription endpoint."""

import os
from pathlib import Path

# noinspection PyPackageRequirements
import requests


def test_real_wav():
    audio_file_path: Path = (Path(__file__).parent / "test_audio.mp3").resolve()
    api_url: str = f"http://127.0.0.1:{os.getenv('UVICORN_PORT', "8080")}"
    expected_text: str = (
        "за інформацією від державної служби з надзвичайних ситуацій станом на сьому  ранку п'яятнадцятого  липня."
    )  # sic!

    with audio_file_path.open("rb") as f:
        response = requests.post(
            f"{api_url}/v1/audio/transcriptions",
            files={"file": f},
            data={"model": "whisper-1", "response_format": "json"},
            timeout=30,
        )
    assert response.status_code == 200  # noqa: PLR2004
    response_text = response.json()["text"].lower()
    assert expected_text == response_text, f"Response text does not match: {response_text}"
