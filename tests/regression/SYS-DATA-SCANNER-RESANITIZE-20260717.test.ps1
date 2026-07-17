param(
    [string]$SessionControl = "$env:USERPROFILE\.codex\skills\session-control\scripts\session_control.py"
)

$ErrorActionPreference = "Stop"
$repo = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$artifact = Join-Path $repo "data\external\kff\kff-disability-page.html"

& python $SessionControl scan --path $repo
if ($LASTEXITCODE -ne 0) {
    throw "Corrected whole-tree credential scan failed."
}

$text = [System.IO.File]::ReadAllText($artifact)
$markers = [regex]::Matches($text, "apiKey\s*:\s*'\[REMOVED_EXTERNAL_CLIENT_KEY\]'")
if ($markers.Count -ne 1) {
    throw "Expected exactly one external client-key removal marker."
}

Write-Output "PASS: sanitized data tree and durable removal marker"
