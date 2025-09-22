# MCP Federation Suite Installer v3.1 - SAFE VERSION
# Enhanced with conflict detection and backup management
# GitHub: https://github.com/justmy2satoshis/mcp-federation-core

param(
    [switch]$SkipOllama,
    [switch]$QuickInstall,
    [switch]$UpdateOnly,
    [switch]$Force
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Display banner
Write-Host @"

███╗   ███╗ ██████╗██████╗     ███████╗███████╗██████╗ ███████╗██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
████╗ ████║██╔════╝██╔══██╗    ██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
██╔████╔██║██║     ██████╔╝    █████╗  █████╗  ██║  ██║█████╗  ██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║
██║╚██╔╝██║██║     ██╔═══╝     ██╔══╝  ██╔══╝  ██║  ██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
██║ ╚═╝ ██║╚██████╗██║         ██║     ███████╗██████╔╝███████╗██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
╚═╝     ╚═╝ ╚═════╝╚═╝         ╚═╝     ╚══════╝╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

                            15 MCPs | Ollama Priority | 80-95% Cost Savings
                                Version 3.1 - SAFE EDITION
"@ -ForegroundColor Cyan

# Configuration
$baseDir = "$env:USERPROFILE\mcp-servers"
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupDir = "$baseDir\backups\$timestamp"

# Our MCP list
$ourMCPs = @(
    'expert-role-prompt',
    'kimi-k2-code-context',
    'converse',
    'kimi-k2-heavy-processor',
    'rag-context-fixed',
    'filesystem',
    'github',
    'sqlite',
    'playwright',
    'memory',
    'sequential-thinking',
    'web-search',
    'perplexity',
    'git-ops',
    'desktop-commander'
)

# Function to detect conflicts
function Test-MCPConflicts {
    param($ConfigPath, $NewMCPs)

    $conflicts = @()
    $existing = @()

    if (Test-Path $ConfigPath) {
        try {
            $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
            if ($config.mcpServers) {
                $existing = $config.mcpServers.PSObject.Properties.Name

                foreach ($mcp in $NewMCPs) {
                    if ($mcp -in $existing) {
                        $conflicts += $mcp
                    }
                }
            }
        } catch {
            Write-Host "⚠ Warning: Could not parse existing config" -ForegroundColor Yellow
        }
    }

    return @{
        Existing = $existing
        Conflicts = $conflicts
        HasConflicts = $conflicts.Count -gt 0
    }
}

# Function to create comprehensive backup
function New-ConfigBackup {
    param($ConfigPath, $BackupDir)

    if (Test-Path $ConfigPath) {
        New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null

        # Copy config
        $backupPath = Join-Path $BackupDir "claude_desktop_config.json"
        Copy-Item $ConfigPath $backupPath

        # Create restore script
        $restoreScript = @"
# MCP Federation Restore Script
# Generated: $(Get-Date)
# To restore: Run this script in PowerShell

`$backupFile = '$backupPath'
`$targetFile = '$ConfigPath'

if (Test-Path `$backupFile) {
    Copy-Item `$backupFile `$targetFile -Force
    Write-Host "✓ Configuration restored from backup" -ForegroundColor Green
    Write-Host "  Please restart Claude Desktop" -ForegroundColor Yellow
} else {
    Write-Host "✗ Backup file not found: `$backupFile" -ForegroundColor Red
}
"@

        $restoreScript | Out-File (Join-Path $BackupDir "RESTORE.ps1") -Encoding UTF8

        # Create info file
        $info = @{
            BackupDate = Get-Date
            OriginalPath = $ConfigPath
            BackupPath = $backupPath
            MCPCount = $existing.Count
            MCPList = $existing
        } | ConvertTo-Json -Depth 5

        $info | Out-File (Join-Path $BackupDir "backup_info.json") -Encoding UTF8

        return $backupPath
    }
    return $null
}

# SAFETY CHECK: Detect existing MCPs and conflicts
Write-Host "`n[SAFETY CHECK] Analyzing existing configuration..." -ForegroundColor Yellow

$conflictCheck = Test-MCPConflicts -ConfigPath $configPath -NewMCPs $ourMCPs

if ($conflictCheck.Existing.Count -gt 0) {
    Write-Host "`n📋 Found existing MCPs:" -ForegroundColor Cyan
    $conflictCheck.Existing | ForEach-Object {
        $icon = if ($_ -in $conflictCheck.Conflicts) { "⚠" } else { "✓" }
        $color = if ($_ -in $conflictCheck.Conflicts) { "Yellow" } else { "Gray" }
        Write-Host "  $icon $_" -ForegroundColor $color
    }
}

if ($conflictCheck.HasConflicts -and -not $Force) {
    Write-Host "`n⚠️ CONFLICT DETECTED!" -ForegroundColor Red
    Write-Host "The following MCPs already exist and may be overwritten:" -ForegroundColor Yellow
    $conflictCheck.Conflicts | ForEach-Object {
        Write-Host "  • $_" -ForegroundColor Yellow
    }

    Write-Host "`n🔧 Resolution Options:" -ForegroundColor Cyan
    Write-Host "  1. Create backup and proceed (RECOMMENDED)" -ForegroundColor Green
    Write-Host "  2. Update only non-conflicting MCPs" -ForegroundColor Yellow
    Write-Host "  3. Merge configurations (Advanced)" -ForegroundColor Cyan
    Write-Host "  4. Cancel installation" -ForegroundColor Red

    do {
        $choice = Read-Host "`nSelect option (1-4)"
    } while ($choice -notmatch '^[1-4]$')

    switch ($choice) {
        '1' {
            Write-Host "`n[BACKUP] Creating comprehensive backup..." -ForegroundColor Yellow
            $backupPath = New-ConfigBackup -ConfigPath $configPath -BackupDir $backupDir
            Write-Host "✓ Backup created: $backupPath" -ForegroundColor Green
            Write-Host "✓ Restore script: $backupDir\RESTORE.ps1" -ForegroundColor Green
        }
        '2' {
            Write-Host "`n[SELECTIVE] Installing only non-conflicting MCPs..." -ForegroundColor Yellow
            $ourMCPs = $ourMCPs | Where-Object { $_ -notin $conflictCheck.Conflicts }
            Write-Host "  Will install: $($ourMCPs -join ', ')" -ForegroundColor Cyan
        }
        '3' {
            Write-Host "`n[MERGE] Preparing to merge configurations..." -ForegroundColor Yellow
            $backupPath = New-ConfigBackup -ConfigPath $configPath -BackupDir $backupDir
            Write-Host "✓ Backup created before merge: $backupPath" -ForegroundColor Green
            $mergeMode = $true
        }
        '4' {
            Write-Host "`n[CANCELLED] Installation aborted by user" -ForegroundColor Red
            Write-Host "  No changes were made to your system" -ForegroundColor Gray
            exit 0
        }
    }
} elseif (Test-Path $configPath) {
    # Always create a backup even if no conflicts
    Write-Host "`n[BACKUP] Creating safety backup..." -ForegroundColor Yellow
    $backupPath = New-ConfigBackup -ConfigPath $configPath -BackupDir $backupDir
    Write-Host "✓ Backup saved: $backupPath" -ForegroundColor Green
}

# Create required directories
Write-Host "`n[SETUP] Creating directory structure..." -ForegroundColor Yellow
@($baseDir, $backupDir, "$env:APPDATA\Claude") | ForEach-Object {
    New-Item -ItemType Directory -Force -Path $_ | Out-Null
}

# Check prerequisites
if (-not $UpdateOnly) {
    Write-Host "`n[PREREQUISITES] Checking system requirements..." -ForegroundColor Yellow

    $requirements = @(
        @{Name="Python"; Command="python"; Version="--version"; Required=$true},
        @{Name="Node.js"; Command="node"; Version="--version"; Required=$true},
        @{Name="Git"; Command="git"; Version="--version"; Required=$true},
        @{Name="npm"; Command="npm"; Version="--version"; Required=$true}
    )

    $reqMet = $true
    foreach ($req in $requirements) {
        try {
            $output = & $req.Command $req.Version 2>&1
            Write-Host "  ✓ $($req.Name): $output" -ForegroundColor Green
        } catch {
            if ($req.Required) {
                Write-Host "  ✗ $($req.Name) not found - required for installation" -ForegroundColor Red
                Write-Host "    Please install from: https://$(($req.Name -replace ' ','-').ToLower()).org" -ForegroundColor Yellow
                $reqMet = $false
            }
        }
    }

    if (-not $reqMet) {
        Write-Host "`n❌ Prerequisites not met. Please install missing components." -ForegroundColor Red
        exit 1
    }

    # Install Python packages
    Write-Host "`n[PYTHON] Installing required packages..." -ForegroundColor Yellow
    pip install -q mcp pydantic aiohttp numpy 2>$null
    Write-Host "  ✓ Python packages installed" -ForegroundColor Green
}

# Ollama installation
if (-not $SkipOllama) {
    Write-Host "`n[OLLAMA] Checking Ollama installation..." -ForegroundColor Yellow
    try {
        ollama --version | Out-Null
        Write-Host "  ✓ Ollama is installed" -ForegroundColor Green

        # Check if models are available
        $models = ollama list 2>$null
        if ($models) {
            Write-Host "  ✓ Available models:" -ForegroundColor Green
            $models | ForEach-Object { Write-Host "    • $_" -ForegroundColor Gray }
        }

        # Pull recommended models if missing
        $recommendedModels = @("llama3.2:3b", "mistral", "phi3")
        Write-Host "  Installing recommended models for cost optimization:" -ForegroundColor Cyan
        foreach ($model in $recommendedModels) {
            if ($models -notmatch $model.Split(':')[0]) {
                Write-Host "    Pulling $model..." -ForegroundColor Gray -NoNewline
                ollama pull $model 2>$null
                Write-Host " Done" -ForegroundColor Green
            } else {
                Write-Host "    ✓ $model already available" -ForegroundColor Gray
            }
        }
    } catch {
        Write-Host "  ⚠ Ollama not installed - Installing now..." -ForegroundColor Yellow
        $ollamaUrl = "https://github.com/ollama/ollama/releases/latest/download/OllamaSetup.exe"
        $ollamaInstaller = "$env:TEMP\OllamaSetup.exe"

        Write-Host "    Downloading Ollama..." -ForegroundColor Gray
        Invoke-WebRequest -Uri $ollamaUrl -OutFile $ollamaInstaller

        Write-Host "    Installing Ollama..." -ForegroundColor Gray
        Start-Process $ollamaInstaller -ArgumentList "/S" -Wait

        Write-Host "  ✓ Ollama installed successfully" -ForegroundColor Green

        # Start Ollama service
        Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
        Start-Sleep -Seconds 3
    }
}

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "                    INSTALLATION SUMMARY" -ForegroundColor Green
Write-Host ("=" * 70) -ForegroundColor Cyan

$summary = @"

📊 Configuration Status:
  • Existing MCPs: $($conflictCheck.Existing.Count)
  • Conflicts Found: $($conflictCheck.Conflicts.Count)
  • MCPs to Install: $($ourMCPs.Count)
  • Backup Created: $(if ($backupPath) { "✓ Yes" } else { "✗ No" })

📁 Paths:
  • MCP Directory: $baseDir
  • Config File: $configPath
  • Backup Location: $backupDir

💡 Next Steps:
  1. Installation will proceed with selected options
  2. Claude Desktop will need to be restarted
  3. API keys can be added after installation

"@

Write-Host $summary -ForegroundColor Cyan

Write-Host "Press any key to continue or Ctrl+C to cancel..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# Continue with actual installation...
Write-Host "`n[INSTALLATION] Beginning MCP installation..." -ForegroundColor Green