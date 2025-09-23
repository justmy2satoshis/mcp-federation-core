# MCP Federation Core Installer v3.2.2 - FIXED VERSION
# This version ACTUALLY configures MCPs (not just prints messages)
# GitHub: https://github.com/justmy2satoshis/mcp-federation-core

param(
    [switch]$SkipOllama,
    [switch]$SkipPython,
    [switch]$QuickInstall,
    [switch]$UpdateOnly,
    [switch]$Force,
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Display banner - ASCII art without special characters
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "                   MCP FEDERATION CORE v3.2.2 FIXED                        " -ForegroundColor Cyan
Write-Host "               15 MCPs | Unified Database | Easy Setup                     " -ForegroundColor White
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$baseDir = "$env:USERPROFILE\mcp-servers"
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupDir = "$baseDir\backups\$timestamp"
$installerUnifiedDir = "$baseDir\installers\unified"
$dbPath = "$baseDir\mcp-unified.db"

# Federation MCP configurations with ACTUAL DETAILS
$federationMCPConfigs = @{
    'sqlite' = @{
        command = "npx"
        args = @("-y", "@modelcontextprotocol/server-sqlite", "$dbPath")
    }
    'expert-role-prompt' = @{
        command = "node"
        args = @("$baseDir\expert-role-prompt\index.js")
    }
    'kimi-k2-resilient-enhanced' = @{
        command = "python"
        args = @("-m", "kimi_k2_resilient")
        env = @{
            KIMI_DB_PATH = "$baseDir\kimi-resilient.db"
        }
    }
    'kimi-k2-code-context-enhanced' = @{
        command = "python"
        args = @("-m", "kimi_k2_code_context")
    }
    'rag-context' = @{
        command = "python"
        args = @("-m", "rag_context")
        env = @{
            RAG_DB_PATH = "$baseDir\rag-context.db"
        }
    }
    'converse' = @{
        command = "node"
        args = @("$baseDir\converse\index.js")
    }
    'web-search' = @{
        command = "npx"
        args = @("-y", "@modelcontextprotocol/server-brave-search")
        env = @{
            BRAVE_API_KEY = "YOUR_BRAVE_API_KEY"
        }
    }
    'github-manager' = @{
        command = "npx"
        args = @("-y", "@modelcontextprotocol/server-github")
        env = @{
            GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"
        }
    }
    'memory' = @{
        command = "npx"
        args = @("-y", "@modelcontextprotocol/server-memory")
    }
    'filesystem' = @{
        command = "npx"
        args = @("-y", "@modelcontextprotocol/server-filesystem")
        env = @{
            ALLOWED_PATHS = "$HOME"
        }
    }
    'desktop-commander' = @{
        command = "node"
        args = @("$baseDir\desktop-commander\index.js")
    }
    'perplexity' = @{
        command = "node"
        args = @("$baseDir\perplexity\index.js")
        env = @{
            PERPLEXITY_API_KEY = "YOUR_PERPLEXITY_API_KEY"
        }
    }
    'playwright' = @{
        command = "npx"
        args = @("-y", "@modelcontextprotocol/server-playwright")
    }
    'git-ops' = @{
        command = "npx"
        args = @("-y", "@modelcontextprotocol/server-git")
    }
    'sequential-thinking' = @{
        command = "node"
        args = @("$baseDir\sequential-thinking\index.js")
    }
}

# Function to test admin rights
function Test-AdminRights {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to create backup
function New-ConfigBackup {
    param(
        [string]$ConfigPath,
        [string]$BackupDir
    )

    if (Test-Path $ConfigPath) {
        New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null

        $backupPath = Join-Path $BackupDir "claude_desktop_config.json"
        Copy-Item $ConfigPath $backupPath -Force

        # Create restore script
        $restoreScript = @"
# MCP Federation Restore Script
# Generated: $(Get-Date)

`$backupFile = '$backupPath'
`$targetFile = '$ConfigPath'

if (Test-Path `"`$backupFile`") {
    Copy-Item `"`$backupFile`" `"`$targetFile`" -Force
    Write-Host 'Configuration restored from backup' -ForegroundColor Green
    Write-Host 'Please restart Claude Desktop' -ForegroundColor Yellow
} else {
    Write-Host 'Backup file not found' -ForegroundColor Red
}
"@

        $restoreScript | Out-File (Join-Path $BackupDir "RESTORE.ps1") -Encoding UTF8

        return $backupPath
    }
    return $null
}

# Function to detect existing MCPs
function Get-ExistingMCPs {
    param([string]$ConfigPath)

    $existing = @()
    if (Test-Path $ConfigPath) {
        try {
            $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
            if ($config.mcpServers) {
                $existing = $config.mcpServers.PSObject.Properties.Name
            }
        }
        catch {
            Write-Host "Warning: Could not parse existing config" -ForegroundColor Yellow
        }
    }
    return $existing
}

# Main installation logic
if ($WhatIf) {
    Write-Host "[WHATIF MODE] No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

# Check prerequisites
Write-Host "[PREREQUISITES] Checking system requirements..." -ForegroundColor Yellow

$prereqMet = $true
$prereqs = @(
    @{Name="Python"; Command="python"; Version="--version"},
    @{Name="Node.js"; Command="node"; Version="--version"},
    @{Name="Git"; Command="git"; Version="--version"},
    @{Name="npm"; Command="npm"; Version="--version"}
)

foreach ($prereq in $prereqs) {
    try {
        $output = & $prereq.Command $prereq.Version 2>&1
        Write-Host "  OK: $($prereq.Name) - $output" -ForegroundColor Green
    }
    catch {
        Write-Host "  MISSING: $($prereq.Name)" -ForegroundColor Red
        $prereqMet = $false
    }
}

if (-not $prereqMet -and -not $Force) {
    Write-Host ""
    Write-Host "Prerequisites not met. Install missing components or use -Force to continue anyway." -ForegroundColor Red
    exit 1
}

# Check for existing MCPs
Write-Host ""
Write-Host "[ANALYSIS] Checking for existing MCPs..." -ForegroundColor Yellow

$existingMCPs = Get-ExistingMCPs -ConfigPath $configPath
$conflictingMCPs = @()

foreach ($mcp in $federationMCPConfigs.Keys) {
    if ($mcp -in $existingMCPs) {
        $conflictingMCPs += $mcp
    }
}

if ($existingMCPs.Count -gt 0) {
    Write-Host "  Found $($existingMCPs.Count) existing MCPs" -ForegroundColor Cyan
    if ($conflictingMCPs.Count -gt 0) {
        Write-Host "  Conflicts detected with $($conflictingMCPs.Count) Federation MCPs" -ForegroundColor Yellow
    }
}

# Create backup if needed
if ($existingMCPs.Count -gt 0 -and -not $WhatIf) {
    Write-Host ""
    Write-Host "[BACKUP] Creating configuration backup..." -ForegroundColor Yellow

    New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
    $backupPath = New-ConfigBackup -ConfigPath $configPath -BackupDir $backupDir

    if ($backupPath) {
        Write-Host "  Backup saved: $backupPath" -ForegroundColor Green
        Write-Host "  Restore script: $backupDir\RESTORE.ps1" -ForegroundColor Green
    }
}

# Handle conflicts
if ($conflictingMCPs.Count -gt 0 -and -not $Force) {
    Write-Host ""
    Write-Host "[CONFLICT] The following MCPs will be replaced:" -ForegroundColor Yellow

    foreach ($conflict in $conflictingMCPs) {
        Write-Host "  - $conflict" -ForegroundColor Yellow
    }

    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "  1. Continue with replacement (backup created)" -ForegroundColor White
    Write-Host "  2. Cancel installation" -ForegroundColor White

    if (-not $WhatIf) {
        do {
            $choice = Read-Host "Select option (1-2)"
        } while ($choice -notmatch '^[1-2]$')

        if ($choice -eq '2') {
            Write-Host ""
            Write-Host "Installation cancelled" -ForegroundColor Red
            exit 0
        }
    }
}

# Create required directories
if (-not $WhatIf) {
    Write-Host ""
    Write-Host "[SETUP] Creating directory structure..." -ForegroundColor Yellow

    @($baseDir, $installerUnifiedDir, "$env:APPDATA\Claude") | ForEach-Object {
        if (-not (Test-Path $_)) {
            New-Item -ItemType Directory -Force -Path $_ | Out-Null
            Write-Host "  Created: $_" -ForegroundColor Green
        }
        else {
            Write-Host "  Exists: $_" -ForegroundColor Gray
        }
    }
}

# Download uninstaller files
if (-not $WhatIf) {
    Write-Host ""
    Write-Host "[UNINSTALLER] Setting up uninstaller files..." -ForegroundColor Yellow

    $uninstallerFiles = @(
        @{File="uninstall.py"; Url="https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installers/unified/uninstall.py"},
        @{File="uninstall.bat"; Url="https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installers/unified/uninstall.bat"},
        @{File="uninstall.sh"; Url="https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installers/unified/uninstall.sh"}
    )

    foreach ($item in $uninstallerFiles) {
        $targetPath = Join-Path $installerUnifiedDir $item.File
        try {
            Invoke-WebRequest -Uri $item.Url -OutFile $targetPath -UseBasicParsing
            Write-Host "  Downloaded: $($item.File)" -ForegroundColor Green
        }
        catch {
            Write-Host "  Failed: $($item.File) - $_" -ForegroundColor Red
        }
    }
}

# Install Python packages
if ($SkipPython) {
    Write-Host ""
    Write-Host "[PYTHON] Skipping Python package installation (-SkipPython flag)" -ForegroundColor Yellow
} elseif (-not $UpdateOnly -and -not $WhatIf) {
    Write-Host ""
    Write-Host "[PYTHON] Installing required packages..." -ForegroundColor Yellow

    # Check Python version for PEP 668 compliance (Python 3.11+)
    $pythonVersion = python --version 2>&1
    $needsBreakFlag = $false

    if ($pythonVersion -match "Python (\d+)\.(\d+)") {
        $majorVersion = [int]$matches[1]
        $minorVersion = [int]$matches[2]
        if ($majorVersion -eq 3 -and $minorVersion -ge 11) {
            $needsBreakFlag = $true
            Write-Host "  Python 3.11+ detected - using --break-system-packages flag" -ForegroundColor Gray
        }
    }

    $packages = @("mcp", "pydantic", "aiohttp", "numpy")
    foreach ($package in $packages) {
        Write-Host "  Installing $package..." -ForegroundColor Gray -NoNewline

        # Try installation with appropriate flags
        $installed = $false

        try {
            if ($needsBreakFlag) {
                # Use python -m pip for better Windows compatibility
                $output = python -m pip install -q $package --break-system-packages 2>&1
                $installed = ($LASTEXITCODE -eq 0)
            } else {
                # Standard install for older Python versions
                $output = python -m pip install -q $package 2>&1
                $installed = ($LASTEXITCODE -eq 0)
            }
        } catch {
            # Silently handle any errors
            $installed = $false
        }

        if ($installed) {
            Write-Host " Done" -ForegroundColor Green
        } else {
            Write-Host " Failed" -ForegroundColor Yellow
        }
    }
}

# CRITICAL FIX: ACTUALLY Configure MCPs (not just print messages)
if (-not $WhatIf) {
    Write-Host ""
    Write-Host "[CONFIGURATION] Setting up Federation MCPs..." -ForegroundColor Yellow

    # Load existing config or create new one
    if (Test-Path $configPath) {
        Write-Host "  Loading existing configuration..." -ForegroundColor Gray
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
    } else {
        Write-Host "  Creating new configuration..." -ForegroundColor Gray
        $config = @{
            mcpServers = @{}
        } | ConvertTo-Json | ConvertFrom-Json
    }

    # Ensure mcpServers property exists
    if (-not $config.mcpServers) {
        $config | Add-Member -NotePropertyName "mcpServers" -NotePropertyValue @{} -Force
    }

    # ACTUALLY ADD EACH MCP CONFIGURATION
    $configuredCount = 0
    foreach ($mcpName in $federationMCPConfigs.Keys) {
        Write-Host "  Configuring: $mcpName" -ForegroundColor Gray

        $mcpConfig = $federationMCPConfigs[$mcpName]

        # Create the MCP entry
        $mcpEntry = @{
            command = $mcpConfig.command
            args = $mcpConfig.args
        }

        # Add environment variables if present
        if ($mcpConfig.env) {
            $mcpEntry.env = $mcpConfig.env
        }

        # Add to config
        if ($config.mcpServers.PSObject.Properties.Name -contains $mcpName) {
            $config.mcpServers.PSObject.Properties.Remove($mcpName)
        }
        $config.mcpServers | Add-Member -NotePropertyName $mcpName -NotePropertyValue $mcpEntry -Force

        $configuredCount++
    }

    # CRITICAL: SAVE THE CONFIGURATION TO FILE
    Write-Host "  Saving configuration to: $configPath" -ForegroundColor Yellow

    try {
        # Ensure directory exists
        $configDir = Split-Path $configPath -Parent
        if (-not (Test-Path $configDir)) {
            New-Item -ItemType Directory -Path $configDir -Force | Out-Null
        }

        # Save with proper formatting
        $jsonContent = $config | ConvertTo-Json -Depth 10
        $jsonContent | Set-Content -Path $configPath -Encoding UTF8 -Force

        Write-Host "  Configuration saved successfully!" -ForegroundColor Green

        # VERIFY the save worked
        Write-Host "  Verifying configuration..." -ForegroundColor Yellow
        $verification = Get-Content $configPath -Raw | ConvertFrom-Json
        $verifiedCount = @($verification.mcpServers.PSObject.Properties.Name).Count

        if ($verifiedCount -eq $configuredCount) {
            Write-Host "  Verified: $verifiedCount MCPs configured successfully" -ForegroundColor Green
        } else {
            Write-Host "  WARNING: Expected $configuredCount MCPs but found $verifiedCount" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "  ERROR: Failed to save configuration: $_" -ForegroundColor Red
        exit 1
    }
}

# Create database
if (-not $WhatIf) {
    Write-Host ""
    Write-Host "[DATABASE] Creating unified database..." -ForegroundColor Yellow

    if (-not (Test-Path $dbPath)) {
        # Create empty database file
        New-Item -ItemType File -Path $dbPath -Force | Out-Null
        Write-Host "  Created: $dbPath" -ForegroundColor Green
    }
    else {
        Write-Host "  Exists: $dbPath" -ForegroundColor Gray
    }
}

# Ollama installation
if (-not $SkipOllama -and -not $WhatIf) {
    Write-Host ""
    Write-Host "[OLLAMA] Checking Ollama installation..." -ForegroundColor Yellow

    try {
        ollama --version | Out-Null
        Write-Host "  Ollama is installed" -ForegroundColor Green
    }
    catch {
        Write-Host "  Ollama not installed" -ForegroundColor Yellow
        Write-Host "  Download from: https://ollama.ai" -ForegroundColor Cyan
    }
}

# Summary
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "                        INSTALLATION COMPLETE                               " -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

if (-not $WhatIf) {
    # Show actual configuration count
    try {
        $finalConfig = Get-Content $configPath -Raw | ConvertFrom-Json
        $actualMCPCount = @($finalConfig.mcpServers.PSObject.Properties.Name).Count
        Write-Host "Summary:" -ForegroundColor Cyan
        Write-Host "  - MCPs Configured: $actualMCPCount" -ForegroundColor White
    }
    catch {
        Write-Host "Summary:" -ForegroundColor Cyan
        Write-Host "  - MCPs Configured: Unknown (could not verify)" -ForegroundColor Yellow
    }
} else {
    Write-Host "Summary:" -ForegroundColor Cyan
    Write-Host "  - MCPs to Configure: 15" -ForegroundColor White
}

Write-Host "  - Database: $dbPath" -ForegroundColor White
Write-Host "  - Uninstaller: $installerUnifiedDir\uninstall.bat" -ForegroundColor White

if ($backupPath) {
    Write-Host "  - Backup: $backupPath" -ForegroundColor White
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Restart Claude Desktop" -ForegroundColor White
Write-Host "  2. Verify all MCPs appear in settings" -ForegroundColor White
Write-Host "  3. Configure API keys as needed" -ForegroundColor White
Write-Host ""

if ($WhatIf) {
    Write-Host "[WHATIF] No changes were made. Remove -WhatIf to perform installation." -ForegroundColor Yellow
}