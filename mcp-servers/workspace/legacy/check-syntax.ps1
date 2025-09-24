# PowerShell Syntax Checker
param(
    [string]$FilePath = "..\..\installer-safe.ps1"
)

$fullPath = (Resolve-Path $FilePath -ErrorAction SilentlyContinue).Path
if (-not $fullPath) {
    Write-Host "File not found: $FilePath" -ForegroundColor Red
    exit 1
}

Write-Host "Checking syntax for: $fullPath" -ForegroundColor Cyan
Write-Host ""

$errors = $null
$tokens = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile(
    $fullPath,
    [ref]$tokens,
    [ref]$errors
)

if ($errors.Count -eq 0) {
    Write-Host "✓ No syntax errors found!" -ForegroundColor Green
} else {
    Write-Host "✗ Found $($errors.Count) syntax error(s):" -ForegroundColor Red
    Write-Host ""

    foreach ($error in $errors) {
        Write-Host "Line $($error.Extent.StartLineNumber): $($error.Message)" -ForegroundColor Yellow
        Write-Host "  Near: $($error.Extent.Text)" -ForegroundColor Gray
        Write-Host ""
    }
}

# Additional checks
Write-Host "Additional Analysis:" -ForegroundColor Cyan
Write-Host "  Total Lines: $($ast.Extent.EndLineNumber)" -ForegroundColor Gray

$functionCount = ($ast.FindAll({$args[0] -is [System.Management.Automation.Language.FunctionDefinitionAst]}, $true)).Count
Write-Host "  Functions: $functionCount" -ForegroundColor Gray

$variableCount = ($tokens | Where-Object {$_.Kind -eq 'Variable'}).Count
Write-Host "  Variables: $variableCount" -ForegroundColor Gray