$inputJson = [Console]::In.ReadToEnd()

$logDir = Join-Path $PSScriptRoot "..\logs"
$logDir = [IO.Path]::GetFullPath($logDir)

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$toolName = "unknown"

if (-not [string]::IsNullOrWhiteSpace($inputJson)) {
    try {
        $hookData = $inputJson | ConvertFrom-Json -Depth 10
        if ($hookData.toolName) {
            $toolName = [string]$hookData.toolName
        } elseif ($hookData.tool) {
            $toolName = [string]$hookData.tool
        }
    } catch {
        $toolName = "unparseable"
    }
}

Add-Content -Path (Join-Path $logDir "tool-usage.log") -Value "[$timestamp] PostToolUse: $toolName"

$payload = @{
    continue = $true
}

$payload | ConvertTo-Json -Compress