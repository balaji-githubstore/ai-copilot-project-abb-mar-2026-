$inputJson = [Console]::In.ReadToEnd()

$logDir = Join-Path $PSScriptRoot "..\logs"
$logDir = [IO.Path]::GetFullPath($logDir)

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$promptText = ""

if (-not [string]::IsNullOrWhiteSpace($inputJson)) {
    try {
        $hookData = $inputJson | ConvertFrom-Json -Depth 10
        if ($hookData.prompt) {
            $promptText = [string]$hookData.prompt
        } elseif ($hookData.message) {
            $promptText = [string]$hookData.message
        }
    } catch {
        $promptText = "<unparseable hook input>"
    }
}

if ([string]::IsNullOrWhiteSpace($promptText)) {
    $promptText = "<empty prompt>"
}

$line = "[$timestamp] $promptText"
Add-Content -Path (Join-Path $logDir "user-prompts.log") -Value $line