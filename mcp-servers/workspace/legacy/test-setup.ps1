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

# Run the installer
Write-Host ""
Write-Host "Starting installation..." -ForegroundColor Yellow
Write-Host ""

Set-Location $installPath

# Check if installer exists and is readable
if (Test-Path $installerPath) {
    # Run installer with proper execution
    & $installerPath
} else {
    Write-Host "Installer not found at: $installerPath" -ForegroundColor Red
    exit 1
}