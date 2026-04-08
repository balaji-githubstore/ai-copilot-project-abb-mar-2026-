$inputJson = [Console]::In.ReadToEnd()

function Get-ToolName {
    param(
        [Parameter(Mandatory = $true)]
        $Value
    )

    if ($null -eq $Value) {
        return $null
    }

    if ($Value -is [string]) {
        return $null
    }

    if ($Value.PSObject -and $Value.PSObject.Properties.Count -gt 0) {
        foreach ($key in @("toolName", "tool", "name", "tool_name")) {
            $property = $Value.PSObject.Properties[$key]
            if ($property -and -not [string]::IsNullOrWhiteSpace([string]$property.Value)) {
                return [string]$property.Value
            }
        }

        foreach ($property in $Value.PSObject.Properties) {
            $result = Get-ToolName -Value $property.Value
            if (-not [string]::IsNullOrWhiteSpace($result)) {
                return $result
            }
        }
    }

    if ($Value -is [System.Collections.IEnumerable]) {
        foreach ($item in $Value) {
            $result = Get-ToolName -Value $item
            if (-not [string]::IsNullOrWhiteSpace($result)) {
                return $result
            }
        }
    }

    return $null
}

function Get-ToolNameFromText {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text
    )

    $patterns = @(
        '"tool_name"\s*:\s*"([^"]+)"',
        '"toolName"\s*:\s*"([^"]+)"',
        '"name"\s*:\s*"([^"]+)"'
    )

    foreach ($pattern in $patterns) {
        $match = [regex]::Match($Text, $pattern)
        if ($match.Success) {
            return $match.Groups[1].Value
        }
    }

    return $null
}

$logDir = Join-Path $PSScriptRoot "..\logs"
$logDir = [IO.Path]::GetFullPath($logDir)

if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$toolName = "unknown"

if (-not [string]::IsNullOrWhiteSpace($inputJson)) {
    try {
        $hookData = $inputJson | ConvertFrom-Json -Depth 20
        $resolvedToolName = Get-ToolName -Value $hookData
        if (-not [string]::IsNullOrWhiteSpace($resolvedToolName)) {
            $toolName = $resolvedToolName
        }
    } catch {
        $resolvedToolName = Get-ToolNameFromText -Text $inputJson
        if (-not [string]::IsNullOrWhiteSpace($resolvedToolName)) {
            $toolName = $resolvedToolName
        } else {
            $toolName = $inputJson.Trim()
        }
    }
}

if ([string]::IsNullOrWhiteSpace($toolName)) {
    $toolName = "unknown"
}

Add-Content -Path (Join-Path $logDir "tool-usage.log") -Value "[$timestamp] PostToolUse: $toolName"

$payload = @{
    continue = $true
}

$payload | ConvertTo-Json -Compress