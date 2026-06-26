# PowerShell test script for STT API

param(
    [Parameter(Mandatory=$false)]
    [string]$AudioFile = "test/test_audio.wav",

    [string]$ApiUrl = "http://127.0.0.1:8080"
)

$form = @{
    file = Get-Item -Path $AudioFile
    model = "whisper-1"
    response_format = "json"
}

Write-Host "Transcribing: $AudioFile via $ApiUrl"
$response = Invoke-RestMethod -Uri "$ApiUrl/v1/audio/transcriptions" -Method POST -Form $form

Write-Host "Transcription result:"
Write-Host $response.text
