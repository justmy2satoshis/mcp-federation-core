# MCP Enterprise Suite Unified Installation Script
# Supports Claude Desktop, Claude Code CLI, or both

param(
    [string]$Environment = 'auto',
    [switch]$SkipDependencies = $false,
    [switch]$Verbose = $false
)

Write-Host @"
╔══════════════════════════════════════════════╗
║     🚀 MCP Enterprise Suite Installer 🚀      ║
║          Version 1.0.0 - Unified             ║
╚══════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

# Detect environment
if ($Environment -eq 'auto') {
    $hasClaudeCode = Get-Command claude -ErrorAction SilentlyContinue
    $hasClaudeDesktop = Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"

    if ($hasClaudeCode -and $hasClaudeDesktop) {
        $Environment = 'both'
    } elseif ($hasClaudeCode) {
        $Environment = 'code'
    } elseif ($hasClaudeDesktop) {
        $Environment = 'desktop'
    } else {
        Write-Host "❌ No Claude installation detected!" -ForegroundColor Red
        Write-Host "Please install Claude Desktop or Claude Code CLI first." -ForegroundColor Yellow
        exit 1
    }
}

Write-Host "✓ Environment detected: $Environment" -ForegroundColor Green
Write-Host ""

# Get repository root
$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $RepoRoot

# Install dependencies
if (-not $SkipDependencies) {
    Write-Host "📦 Installing dependencies..." -ForegroundColor Yellow

    # Check for Node.js
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Node.js not found! Please install Node.js first." -ForegroundColor Red
        exit 1
    }

    # Check for Python
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        Write-Host "❌ Python not found! Please install Python first." -ForegroundColor Red
        exit 1
    }

    # Install npm dependencies for Node.js MCPs
    $mcpsPath = Join-Path $RepoRoot "mcps"
    Get-ChildItem -Path $mcpsPath -Directory | ForEach-Object {
        $packageJson = Join-Path $_.FullName "package.json"
        if (Test-Path $packageJson) {
            Write-Host "  Installing npm dependencies for $($_.Name)..." -ForegroundColor Gray
            Push-Location $_.FullName
            npm install --silent 2>$null
            Pop-Location
        }

        $requirements = Join-Path $_.FullName "requirements.txt"
        if (Test-Path $requirements) {
            Write-Host "  Installing Python dependencies for $($_.Name)..." -ForegroundColor Gray
            pip install -r $requirements --quiet 2>$null
        }
    }

    Write-Host "✓ Dependencies installed" -ForegroundColor Green
}

# Configure based on environment
Write-Host ""
Write-Host "🔧 Configuring MCPs for $Environment..." -ForegroundColor Yellow

switch ($Environment) {
    'desktop' {
        & "$PSScriptRoot\install-desktop.ps1" -Verbose:$Verbose
    }
    'code' {
        & "$PSScriptRoot\install-code.ps1" -Verbose:$Verbose
    }
    'both' {
        Write-Host "  Configuring Claude Desktop..." -ForegroundColor Gray
        & "$PSScriptRoot\install-desktop.ps1" -Verbose:$Verbose
        Write-Host ""
        Write-Host "  Configuring Claude Code CLI..." -ForegroundColor Gray
        & "$PSScriptRoot\install-code.ps1" -Verbose:$Verbose
    }
}

Write-Host ""
Write-Host "🎯 Running validation..." -ForegroundColor Yellow
& "$PSScriptRoot\validate-installation.ps1" -Environment $Environment

Write-Host ""
Write-Host @"
╔══════════════════════════════════════════════╗
║        ✅ Installation Complete! ✅           ║
╚══════════════════════════════════════════════╝
"@ -ForegroundColor Green

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Copy .env.template to .env and add your API keys" -ForegroundColor White
Write-Host "  2. Restart Claude Desktop or CLI to load new MCPs" -ForegroundColor White
Write-Host "  3. Test MCPs with 'claude mcp list' (CLI) or check Desktop UI" -ForegroundColor White
Write-Host ""
Write-Host "Documentation: ./docs/setup/SETUP_GUIDE.md" -ForegroundColor Gray
Write-Host "Issues? Visit: https://github.com/yourusername/mcp-enterprise-suite" -ForegroundColor Gray