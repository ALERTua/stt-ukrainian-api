# PowerShell test script for STT API

param(
    [Parameter(Mandatory=$true)]
    [string]$AudioFile,

    [string]$ApiUrl = "http://127.0.0.1:8000"
)

$form = @{
    file = Get-Item -Path $AudioFile
    model = "whisper-1"
    response_format = "json"
}

Write-Host "Transcribing: $AudioFile"
$response = Invoke-RestMethod -Uri "$ApiUrl/v1/audio/transcriptions" -Method POST -Form $form

Write-Host "Transcription result:"
Write-Host $response.text
