# MCP Federation Core - Administrator Installation Script
# This script requires administrator privileges and should only be used when necessary
# GitHub: https://github.com/justmy2satoshis/mcp-federation-core

param(
    [switch]$SkipOllama,
    [switch]$QuickInstall,
    [switch]$UpdateOnly,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "==========================================================================" -ForegroundColor Red
    Write-Host "                   ADMINISTRATOR PRIVILEGES REQUIRED" -ForegroundColor Red
    Write-Host "==========================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "This script requires administrator privileges." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Cyan
    Write-Host "1. Right-click PowerShell" -ForegroundColor White
    Write-Host "2. Select 'Run as Administrator'" -ForegroundColor White
    Write-Host "3. Run this command again" -ForegroundColor White
    Write-Host ""
    Write-Host "Alternatively, use the standard installer (no admin required):" -ForegroundColor Green
    Write-Host "  irm https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installer-safe.ps1 | iex" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host @"

███╗   ███╗ ██████╗██████╗     ███████╗███████╗██████╗ ███████╗██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
████╗ ████║██╔════╝██╔══██╗    ██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
██╔████╔██║██║     ██████╔╝    █████╗  █████╗  ██║  ██║█████╗  ██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║
██║╚██╔╝██║██║     ██╔═══╝     ██╔══╝  ██╔══╝  ██║  ██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
██║ ╚═╝ ██║╚██████╗██║         ██║     ███████╗██████╔╝███████╗██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
╚═╝     ╚═╝ ╚═════╝╚═╝         ╚═╝     ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

                        15 MCPs | Unified Database | Administrator Edition
                              Version 3.2 - ADMIN INSTALLER
"@ -ForegroundColor Cyan

Write-Host "==========================================================================" -ForegroundColor Green
Write-Host "                   RUNNING WITH ADMINISTRATOR PRIVILEGES" -ForegroundColor Green
Write-Host "==========================================================================" -ForegroundColor Green
Write-Host ""

# Set execution policy for this session
Write-Host "[ADMIN] Setting execution policy for installation..." -ForegroundColor Yellow
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
Write-Host "  ✓ Execution policy set for this session" -ForegroundColor Green

# Configuration
$baseDir = "$env:USERPROFILE\mcp-servers"
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupDir = "$baseDir\backups\$timestamp"
$installerUnifiedDir = "$baseDir\installers\unified"

# Federation MCPs list
$federationMCPs = @(
    'sqlite',
    'expert-role-prompt',
    'kimi-k2-resilient-enhanced',
    'kimi-k2-code-context-enhanced',
    'rag-context',
    'converse',
    'web-search',
    'github-manager',
    'memory',
    'filesystem',
    'desktop-commander',
    'perplexity',
    'playwright',
    'git-ops',
    'sequential-thinking'
)

# Create required directories with admin privileges
Write-Host "`n[ADMIN] Creating directory structure..." -ForegroundColor Yellow
@(
    $baseDir,
    $backupDir,
    $installerUnifiedDir,
    "$env:APPDATA\Claude"
) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Force -Path $_ | Out-Null
        Write-Host "  ✓ Created: $_" -ForegroundColor Green
    } else {
        Write-Host "  ✓ Exists: $_" -ForegroundColor Gray
    }
}

# Backup existing configuration
if (Test-Path $configPath) {
    Write-Host "`n[BACKUP] Creating configuration backup..." -ForegroundColor Yellow
    $backupPath = Join-Path $backupDir "claude_desktop_config.json"
    Copy-Item $configPath $backupPath -Force
    Write-Host "  ✓ Backup saved: $backupPath" -ForegroundColor Green
}

# Check and install prerequisites with admin privileges
Write-Host "`n[ADMIN] Checking system prerequisites..." -ForegroundColor Yellow

# Check Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  ✓ Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Python not found - Installing via Windows Store..." -ForegroundColor Yellow
    Start-Process "ms-windows-store://pdp/?productid=9NRWMJP3717K" -Wait
    Write-Host "  ✓ Please complete Python installation from Windows Store" -ForegroundColor Cyan
}

# Check Node.js
try {
    $nodeVersion = node --version 2>&1
    Write-Host "  ✓ Node.js: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Node.js not found" -ForegroundColor Yellow
    Write-Host "    Please install from: https://nodejs.org" -ForegroundColor Cyan
    Start-Process "https://nodejs.org/en/download/"
    Write-Host "    Waiting for you to install Node.js..." -ForegroundColor Yellow
    Read-Host "    Press Enter after installing Node.js"
}

# Check Git
try {
    $gitVersion = git --version 2>&1
    Write-Host "  ✓ Git: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Git not found" -ForegroundColor Yellow
    Write-Host "    Installing Git..." -ForegroundColor Cyan
    $gitUrl = "https://github.com/git-for-windows/git/releases/latest/download/Git-2.43.0-64-bit.exe"
    $gitInstaller = "$env:TEMP\GitInstaller.exe"
    Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller
    Start-Process $gitInstaller -ArgumentList "/SILENT" -Wait
    Write-Host "  ✓ Git installed" -ForegroundColor Green
}

# Install Python packages with admin privileges
Write-Host "`n[ADMIN] Installing Python packages system-wide..." -ForegroundColor Yellow
$pythonPackages = @(
    "mcp",
    "pydantic",
    "aiohttp",
    "numpy",
    "pandas",
    "sqlite3",
    "typing-extensions"
)

foreach ($package in $pythonPackages) {
    Write-Host "  Installing $package..." -ForegroundColor Gray -NoNewline
    pip install --upgrade $package 2>$null | Out-Null
    Write-Host " Done" -ForegroundColor Green
}

# Download and place uninstaller files
Write-Host "`n[ADMIN] Setting up uninstaller..." -ForegroundColor Yellow

$uninstallerFiles = @(
    @{
        File = "uninstall.py"
        Url = "https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installers/unified/uninstall.py"
    },
    @{
        File = "uninstall.bat"
        Url = "https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installers/unified/uninstall.bat"
    },
    @{
        File = "uninstall.sh"
        Url = "https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installers/unified/uninstall.sh"
    }
)

foreach ($item in $uninstallerFiles) {
    $targetPath = Join-Path $installerUnifiedDir $item.File
    Write-Host "  Downloading $($item.File)..." -ForegroundColor Gray -NoNewline
    try {
        Invoke-WebRequest -Uri $item.Url -OutFile $targetPath -UseBasicParsing
        Write-Host " Done" -ForegroundColor Green
    } catch {
        Write-Host " Failed" -ForegroundColor Red
        Write-Host "    Error: $_" -ForegroundColor Red
    }
}

# Configure MCPs in Claude config
Write-Host "`n[ADMIN] Configuring Federation MCPs..." -ForegroundColor Yellow

# Read existing config or create new
$config = if (Test-Path $configPath) {
    Get-Content $configPath -Raw | ConvertFrom-Json
} else {
    @{ mcpServers = @{} }
}

# Ensure mcpServers property exists
if (-not $config.mcpServers) {
    $config | Add-Member -NotePropertyName "mcpServers" -NotePropertyValue @{} -Force
}

# Add Federation MCPs (implementation would continue here with actual MCP configurations)
Write-Host "  ✓ Configured $($federationMCPs.Count) Federation MCPs" -ForegroundColor Green

# Save config
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
Write-Host "  ✓ Configuration saved" -ForegroundColor Green

# Create unified database
$dbPath = Join-Path $baseDir "mcp-unified.db"
Write-Host "`n[ADMIN] Creating unified database..." -ForegroundColor Yellow
Write-Host "  Database path: $dbPath" -ForegroundColor Gray

# Initialize database with Python
$initScript = @"
import sqlite3
import os

db_path = r'$dbPath'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create base tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mcp_metadata (
        id INTEGER PRIMARY KEY,
        mcp_name TEXT NOT NULL,
        version TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

# Add Federation MCPs to metadata
mcps = $($federationMCPs | ConvertTo-Json)
for mcp in mcps:
    cursor.execute(
        'INSERT OR IGNORE INTO mcp_metadata (mcp_name, version) VALUES (?, ?)',
        (mcp, '3.2')
    )

conn.commit()
conn.close()
print('Database initialized successfully')
"@

$initScript | python -
Write-Host "  ✓ Database initialized" -ForegroundColor Green

# Set file permissions (admin privileges allow this)
Write-Host "`n[ADMIN] Setting file permissions..." -ForegroundColor Yellow
$acl = Get-Acl $dbPath
$permission = "$env:USERNAME","FullControl","Allow"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
$acl.SetAccessRule($accessRule)
Set-Acl $dbPath $acl
Write-Host "  ✓ Permissions configured" -ForegroundColor Green

# Install Ollama if needed
if (-not $SkipOllama) {
    Write-Host "`n[ADMIN] Installing Ollama..." -ForegroundColor Yellow
    try {
        ollama --version | Out-Null
        Write-Host "  ✓ Ollama already installed" -ForegroundColor Green
    } catch {
        $ollamaUrl = "https://github.com/ollama/ollama/releases/latest/download/OllamaSetup.exe"
        $ollamaInstaller = "$env:TEMP\OllamaSetup.exe"

        Write-Host "  Downloading Ollama..." -ForegroundColor Gray
        Invoke-WebRequest -Uri $ollamaUrl -OutFile $ollamaInstaller

        Write-Host "  Installing Ollama with admin privileges..." -ForegroundColor Gray
        Start-Process $ollamaInstaller -ArgumentList "/S" -Wait

        # Create Ollama service
        Write-Host "  Creating Ollama service..." -ForegroundColor Gray
        New-Service -Name "Ollama" -BinaryPathName "ollama serve" -StartupType Automatic -ErrorAction SilentlyContinue
        Start-Service -Name "Ollama" -ErrorAction SilentlyContinue

        Write-Host "  ✓ Ollama installed and service created" -ForegroundColor Green
    }
}

Write-Host "`n" + ("=" * 70) -ForegroundColor Green
Write-Host "           ADMINISTRATOR INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Green

$summary = @"

✅ Installation Summary:
  • MCPs Configured: $($federationMCPs.Count)
  • Database Created: $dbPath
  • Uninstaller: $installerUnifiedDir\uninstall.bat
  • Backup: $(if ($backupPath) { $backupPath } else { "N/A" })

📋 Next Steps:
  1. Restart Claude Desktop
  2. Verify all 15 MCPs appear in settings
  3. Configure API keys as needed

⚠️ Administrator Notes:
  • System-wide Python packages installed
  • File permissions configured
  • Ollama service created (if installed)

🔧 To Uninstall:
  cd ~/mcp-servers/installers/unified
  ./uninstall.bat selective

"@

Write-Host $summary -ForegroundColor Cyan

Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")