$inputJson = [Console]::In.ReadToEnd()
$permissionDecision = "allow"
$permissionReason = "Allowed by default."

if (-not [string]::IsNullOrWhiteSpace($inputJson)) {
    try {
        $hookData = $inputJson | ConvertFrom-Json -Depth 10
        $toolName = [string]$hookData.toolName
        if ([string]::IsNullOrWhiteSpace($toolName) -and $hookData.tool) {
            $toolName = [string]$hookData.tool
        }

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
        $permissionDecision = "ask"
        $permissionReason = "Unable to parse tool hook input."
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