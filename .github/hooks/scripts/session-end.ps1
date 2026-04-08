$logDir = Join-Path $PSScriptRoot "..\logs"
$logDir = [IO.Path]::GetFullPath($logDir)

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path (Join-Path $logDir "sessions.log") -Value "[$timestamp] Session ended"