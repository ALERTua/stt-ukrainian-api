#!/bin/bash
# Bash test script for STT API

if [ -z "$1" ]; then
    echo "Usage: $0 <audio_file>"
    exit 1
fi

AUDIO_FILE="$1"
API_URL="${2:-http://127.0.0.1:8000}"

echo "Transcribing: $AUDIO_FILE"

curl -X POST "$API_URL/v1/audio/transcriptions" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@$AUDIO_FILE" \
  -F "model=whisper-1" \
  -F "response_format=json"

echo ""
