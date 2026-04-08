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

$permissionDecision = "allow"
$permissionReason = "Allowed by default."
$toolName = $null

if (-not [string]::IsNullOrWhiteSpace($inputJson)) {
    try {
        $hookData = $inputJson | ConvertFrom-Json -Depth 20
        $toolName = Get-ToolName -Value $hookData

        $highRiskTools = @(
            "run_in_terminal",
            "apply_patch",
            "create_file",
            "DeleteFile",
            "EditFile"
        )

        if ($highRiskTools -contains $toolName) {
            $permissionDecision = "ask"
            $permissionReason = "This tool can modify files or system state."
        }
    } catch {
        $toolName = Get-ToolNameFromText -Text $inputJson
        if ([string]::IsNullOrWhiteSpace($toolName)) {
            $permissionDecision = "ask"
            $permissionReason = "Unable to parse tool hook input."
        }
    }
}

if ($permissionDecision -eq "allow") {
    $highRiskTools = @(
        "run_in_terminal",
        "apply_patch",
        "create_file",
        "DeleteFile",
        "EditFile"
    )

    if ($highRiskTools -contains $toolName) {
        $permissionDecision = "ask"
        $permissionReason = "This tool can modify files or system state."
    }
}

$payload = @{
    hookSpecificOutput = @{
        hookEventName = "PreToolUse"
        permissionDecision = $permissionDecision
        permissionDecisionReason = $permissionReason
    }
}

$payload | ConvertTo-Json -Compress