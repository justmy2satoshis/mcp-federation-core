# MCP Federation Core - Safe Uninstaller Script
# This script removes ONLY Federation MCPs, preserving user configurations

Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host "MCP Federation Core - Safe Uninstaller" -ForegroundColor Cyan
Write-Host "====================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python detected: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Yellow
    exit 1
}

# Define installation path
$mcpBasePath = "$HOME\mcp-servers\installers\unified"
$uninstallerScript = "$mcpBasePath\uninstall.py"

# Check if uninstaller exists
if (-not (Test-Path $uninstallerScript)) {
    Write-Host "ERROR: Uninstaller not found at $uninstallerScript" -ForegroundColor Red
    Write-Host ""
    Write-Host "The Federation Core may not be installed, or installation is incomplete." -ForegroundColor Yellow
    Write-Host "If you need to manually remove MCPs, edit:" -ForegroundColor Yellow
    Write-Host "  %APPDATA%\Claude\claude_desktop_config.json" -ForegroundColor Cyan
    exit 1
}

Write-Host "Found uninstaller at: $uninstallerScript" -ForegroundColor Green
Write-Host ""

# Run the uninstaller with selective mode by default
Write-Host "Starting selective uninstall (preserves your other MCPs)..." -ForegroundColor Yellow
Write-Host ""

# Execute Python uninstaller
python $uninstallerScript --mode selective

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "====================================================================" -ForegroundColor Green
    Write-Host "Uninstallation completed successfully!" -ForegroundColor Green
    Write-Host "====================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Restart Claude Desktop to apply changes" -ForegroundColor White
    Write-Host "2. Your other MCPs remain untouched" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Uninstallation encountered issues. Please check the output above." -ForegroundColor Yellow
    Write-Host "You may need to run this script as Administrator." -ForegroundColor Yellow
}