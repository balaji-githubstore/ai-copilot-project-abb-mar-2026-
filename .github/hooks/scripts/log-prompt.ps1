$inputJson = [Console]::In.ReadToEnd()

function Get-StringValue {
    param(
        [Parameter(Mandatory = $true)]
        $Value
    )

    if ($null -eq $Value) {
        return $null
    }

    if ($Value -is [string]) {
        return $Value
    }

    if ($Value -is [System.Collections.IEnumerable] -and -not ($Value -is [string])) {
        foreach ($item in $Value) {
            $result = Get-StringValue -Value $item
            if (-not [string]::IsNullOrWhiteSpace($result)) {
                return $result
            }
        }
    }

    if ($Value.PSObject -and $Value.PSObject.Properties.Count -gt 0) {
        foreach ($property in $Value.PSObject.Properties) {
            if ($property.Name -in @("prompt", "message", "text", "content", "userPrompt")) {
                $result = Get-StringValue -Value $property.Value
                if (-not [string]::IsNullOrWhiteSpace($result)) {
                    return $result
                }
            }
        }

        foreach ($property in $Value.PSObject.Properties) {
            $result = Get-StringValue -Value $property.Value
            if (-not [string]::IsNullOrWhiteSpace($result)) {
                return $result
            }
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
$promptText = ""

if (-not [string]::IsNullOrWhiteSpace($inputJson)) {
    try {
        $hookData = $inputJson | ConvertFrom-Json -Depth 20
        $promptText = Get-StringValue -Value $hookData
    } catch {
        $promptText = $inputJson.Trim()
    }
}

if ([string]::IsNullOrWhiteSpace($promptText)) {
    $promptText = "<empty prompt payload>"
}

$line = "[$timestamp] $promptText"
Add-Content -Path (Join-Path $logDir "user-prompts.log") -Value $line