# MCP Federation Core - Setup Script v3.2
# This simple script downloads and runs the installer locally
# Avoids antivirus detection by not using Invoke-Expression

Write-Host ""
Write-Host "MCP Federation Core - Setup v3.2" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Create installation directory
$installPath = "$HOME\mcp-servers\mcp-federation-core"
Write-Host "Creating installation directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path $installPath | Out-Null

# Download the installer
Write-Host "Downloading installer..." -ForegroundColor Yellow
$installerUrl = "https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installer.ps1"
$installerPath = "$installPath\installer.ps1"

try {
    # Use -UseBasicParsing to avoid IE dependency
    Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing
    Write-Host "Installer downloaded successfully" -ForegroundColor Green
} catch {
    Write-Host "Failed to download installer: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Alternative: Download manually from:" -ForegroundColor Yellow
    Write-Host $installerUrl -ForegroundColor Cyan
    exit 1
}

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "3\.(1[1-9]|[2-9][0-9])") {
    Write-Host "  Python 3.11+ detected - installer will handle package installation properly" -ForegroundColor Green
}

# Run the installer
Write-Host ""
Write-Host "Starting installation..." -ForegroundColor Yellow
Write-Host ""

Set-Location $installPath

# Check if installer exists and is readable
if (Test-Path $installerPath) {
    # Run installer with proper execution
    & $installerPath

    # Check if installation succeeded
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "============================================" -ForegroundColor Yellow
        Write-Host "Installation encountered issues" -ForegroundColor Yellow
        Write-Host "============================================" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "If you saw pip errors, try one of these:" -ForegroundColor Cyan
        Write-Host "  1. Run installer skipping Python:" -ForegroundColor White
        Write-Host "     .\installer.ps1 -SkipPython" -ForegroundColor Green
        Write-Host ""
        Write-Host "  2. Install Python packages manually:" -ForegroundColor White
        Write-Host "     pip install mcp pydantic aiohttp numpy --break-system-packages" -ForegroundColor Green
        Write-Host ""
        Write-Host "  3. Use a Python virtual environment" -ForegroundColor White
        Write-Host ""
    }
} else {
    Write-Host "Installer not found at: $installerPath" -ForegroundColor Red
    exit 1
}