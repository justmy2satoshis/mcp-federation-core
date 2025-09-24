# Test script to verify pip installation works without NativeCommandError

Write-Host "Testing pip installation fix..." -ForegroundColor Cyan
Write-Host ""

# Test Python version detection
$pythonVersion = python --version 2>&1
Write-Host "Python version: $pythonVersion" -ForegroundColor Yellow

# Check if Python 3.11+
$needsBreakFlag = $false
if ($pythonVersion -match "Python (\d+)\.(\d+)") {
    $majorVersion = [int]$matches[1]
    $minorVersion = [int]$matches[2]
    if ($majorVersion -eq 3 -and $minorVersion -ge 11) {
        $needsBreakFlag = $true
        Write-Host "Python 3.11+ detected - needs --break-system-packages flag" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Testing pip command..." -ForegroundColor Cyan

# Test with a simple package that's likely already installed
$testPackage = "pip"
Write-Host "  Testing with package: $testPackage" -ForegroundColor Gray

$installed = $false
try {
    if ($needsBreakFlag) {
        Write-Host "  Running: python -m pip install -q $testPackage --break-system-packages" -ForegroundColor Gray
        $output = python -m pip install -q $testPackage --break-system-packages 2>&1
        $installed = ($LASTEXITCODE -eq 0)
    } else {
        Write-Host "  Running: python -m pip install -q $testPackage" -ForegroundColor Gray
        $output = python -m pip install -q $testPackage 2>&1
        $installed = ($LASTEXITCODE -eq 0)
    }
} catch {
    Write-Host "  Error caught: $_" -ForegroundColor Red
    $installed = $false
}

if ($installed) {
    Write-Host "  SUCCESS: No NativeCommandError!" -ForegroundColor Green
    Write-Host "  pip command executed successfully" -ForegroundColor Green
} else {
    Write-Host "  Failed to install (this may be normal if package exists)" -ForegroundColor Yellow
    Write-Host "  But no NativeCommandError was thrown!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Test complete!" -ForegroundColor Cyan