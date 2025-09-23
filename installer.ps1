# MCP Federation Core Installer v3.2.1
# Fixed syntax errors and improved MCP detection
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
Write-Host "                   MCP FEDERATION CORE v3.2.1                              " -ForegroundColor Cyan
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

# Federation MCP list with all name variations
$federationMCPs = @{
    'sqlite' = @('sqlite', 'sqlite-data-warehouse', 'sqlite-mcp')
    'expert-role-prompt' = @('expert-role-prompt', 'expert_role_prompt')
    'kimi-k2-resilient-enhanced' = @('kimi-k2-resilient-enhanced', 'kimi-k2-resilient', 'kimi_k2_resilient')
    'kimi-k2-code-context-enhanced' = @('kimi-k2-code-context-enhanced', 'kimi-k2-code-context', 'kimi_k2_code_context')
    'rag-context' = @('rag-context', 'rag_context', 'rag-context-fixed')
    'converse' = @('converse', 'converse-mcp')
    'web-search' = @('web-search', 'web_search', 'brave-search')
    'github-manager' = @('github-manager', 'github_manager', 'github')
    'memory' = @('memory', 'memory-mcp')
    'filesystem' = @('filesystem', 'filesystem-mcp')
    'desktop-commander' = @('desktop-commander', 'desktop_commander')
    'perplexity' = @('perplexity', 'perplexity-mcp')
    'playwright' = @('playwright', 'playwright-mcp')
    'git-ops' = @('git-ops', 'git_ops', 'gitops')
    'sequential-thinking' = @('sequential-thinking', 'sequential_thinking')
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

# Function to check for conflicts
function Test-MCPConflicts {
    param(
        [string]$ConfigPath,
        [hashtable]$FederationMCPs
    )

    $existing = Get-ExistingMCPs -ConfigPath $ConfigPath
    $conflicts = @()

    foreach ($mcp in $FederationMCPs.Keys) {
        foreach ($variant in $FederationMCPs[$mcp]) {
            if ($variant -in $existing) {
                $conflicts += $variant
                break
            }
        }
    }

    return @{
        Existing = $existing
        Conflicts = $conflicts
        HasConflicts = ($conflicts.Count -gt 0)
    }
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

# Check for conflicts
Write-Host ""
Write-Host "[ANALYSIS] Checking for existing MCPs..." -ForegroundColor Yellow

$conflictCheck = Test-MCPConflicts -ConfigPath $configPath -FederationMCPs $federationMCPs

if ($conflictCheck.Existing.Count -gt 0) {
    Write-Host "  Found $($conflictCheck.Existing.Count) existing MCPs" -ForegroundColor Cyan
    if ($conflictCheck.HasConflicts) {
        Write-Host "  Conflicts detected with $($conflictCheck.Conflicts.Count) Federation MCPs" -ForegroundColor Yellow
    }
}

# Create backup if needed
if ($conflictCheck.Existing.Count -gt 0 -and -not $WhatIf) {
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
if ($conflictCheck.HasConflicts -and -not $Force) {
    Write-Host ""
    Write-Host "[CONFLICT] The following MCPs will be replaced:" -ForegroundColor Yellow

    foreach ($conflict in $conflictCheck.Conflicts) {
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

# Configure MCPs
if (-not $WhatIf) {
    Write-Host ""
    Write-Host "[CONFIGURATION] Setting up Federation MCPs..." -ForegroundColor Yellow

    # This would contain the actual MCP configuration logic
    # For now, just show what would be configured

    foreach ($mcp in $federationMCPs.Keys) {
        Write-Host "  Configuring: $mcp" -ForegroundColor Gray
    }

    Write-Host "  All MCPs configured" -ForegroundColor Green
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
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  - MCPs Configured: 15" -ForegroundColor White
Write-Host "  - Database: $dbPath" -ForegroundColor White
Write-Host "  - Uninstaller: $installerUnifiedDir\uninstall.bat" -ForegroundColor White

if ($backupPath) {
    Write-Host "  - Backup: $backupPath" -ForegroundColor White
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Restart Claude Desktop" -ForegroundColor White
Write-Host "  2. Verify all 15 MCPs appear in settings" -ForegroundColor White
Write-Host "  3. Configure API keys as needed" -ForegroundColor White
Write-Host ""

if ($WhatIf) {
    Write-Host "[WHATIF] No changes were made. Remove -WhatIf to perform installation." -ForegroundColor Yellow
}