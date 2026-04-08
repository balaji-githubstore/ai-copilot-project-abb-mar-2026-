$payload = @{
    systemMessage = "Python pytest automation workspace loaded. Prefer explicit waits, page objects, and assertpy in test files."
}

$payload | ConvertTo-Json -Compress