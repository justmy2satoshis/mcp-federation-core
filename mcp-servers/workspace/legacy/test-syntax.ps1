# Test PowerShell Script Syntax

param(
    [string]$ScriptPath = ".\setup.ps1"
)

if (-not (Test-Path $ScriptPath)) {
    Write-Host "Script not found: $ScriptPath" -ForegroundColor Red
    exit 1
}

$errors = $null
$tokens = $null

$ast = [System.Management.Automation.Language.Parser]::ParseFile(
    (Resolve-Path $ScriptPath).Path,
    [ref]$tokens,
    [ref]$errors
)

if ($errors) {
    Write-Host "Syntax errors found:" -ForegroundColor Red
    foreach ($error in $errors) {
        Write-Host "  Line $($error.Extent.StartLineNumber): $($error.Message)" -ForegroundColor Yellow
    }
    exit 1
} else {
    Write-Host "No syntax errors found in $ScriptPath" -ForegroundColor Green
}