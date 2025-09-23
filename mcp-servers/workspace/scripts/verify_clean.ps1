# MCP Federation Core - Verification Script
# Checks if system is ready for clean installation

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "                    MCP INSTALLATION READINESS CHECK                        " -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$mcpDir = "$env:USERPROFILE\mcp-servers"
$dbPath = "$mcpDir\mcp-unified.db"

$issues = @()
$warnings = @()

# Check Claude Desktop configuration
Write-Host "[CONFIG] Checking Claude Desktop configuration..." -ForegroundColor Yellow

if (Test-Path $configPath) {
    try {
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
        $mcpCount = 0

        if ($config.mcpServers) {
            $mcpCount = $config.mcpServers.PSObject.Properties.Count
        }

        if ($mcpCount -gt 0) {
            Write-Host "  Found $mcpCount existing MCPs" -ForegroundColor Yellow
            $warnings += "Existing MCPs will be affected by installation"

            # List existing MCPs
            Write-Host "  Existing MCPs:" -ForegroundColor Gray
            $config.mcpServers.PSObject.Properties.Name | ForEach-Object {
                Write-Host "    - $_" -ForegroundColor Gray
            }
        }
        else {
            Write-Host "  No MCPs configured (clean state)" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "  Config exists but cannot be parsed" -ForegroundColor Red
        $issues += "Claude Desktop config file is corrupted"
    }
}
else {
    Write-Host "  No config found (fresh installation)" -ForegroundColor Green
}

# Check MCP servers directory
Write-Host ""
Write-Host "[DIRECTORY] Checking MCP servers directory..." -ForegroundColor Yellow

if (Test-Path $mcpDir) {
    $items = Get-ChildItem $mcpDir -ErrorAction SilentlyContinue
    if ($items.Count -gt 0) {
        Write-Host "  Directory exists with $($items.Count) items" -ForegroundColor Yellow
        $warnings += "MCP servers directory contains existing files"
    }
    else {
        Write-Host "  Directory exists but is empty" -ForegroundColor Green
    }
}
else {
    Write-Host "  Directory does not exist (will be created)" -ForegroundColor Green
}

# Check database
Write-Host ""
Write-Host "[DATABASE] Checking unified database..." -ForegroundColor Yellow

if (Test-Path $dbPath) {
    $dbSize = (Get-Item $dbPath).Length / 1MB
    Write-Host "  Database exists (Size: $([Math]::Round($dbSize, 2)) MB)" -ForegroundColor Yellow
    $warnings += "Existing database will be preserved or replaced"
}
else {
    Write-Host "  No database found (will be created)" -ForegroundColor Green
}

# Check running processes
Write-Host ""
Write-Host "[PROCESSES] Checking for running processes..." -ForegroundColor Yellow

$claudeRunning = Get-Process -Name "Claude" -ErrorAction SilentlyContinue
if ($claudeRunning) {
    Write-Host "  Claude Desktop is running" -ForegroundColor Red
    $issues += "Claude Desktop must be closed before installation"
}
else {
    Write-Host "  Claude Desktop is not running" -ForegroundColor Green
}

# Check prerequisites
Write-Host ""
Write-Host "[PREREQUISITES] Checking required software..." -ForegroundColor Yellow

$prereqs = @(
    @{Name="Python"; Command="python"; Required=$true},
    @{Name="Node.js"; Command="node"; Required=$false},
    @{Name="Git"; Command="git"; Required=$false},
    @{Name="PowerShell 5.1+"; Check={$PSVersionTable.PSVersion.Major -ge 5}; Required=$true}
)

foreach ($prereq in $prereqs) {
    if ($prereq.Command) {
        try {
            & $prereq.Command --version 2>&1 | Out-Null
            Write-Host "  $($prereq.Name): Installed" -ForegroundColor Green
        }
        catch {
            if ($prereq.Required) {
                Write-Host "  $($prereq.Name): Not found (REQUIRED)" -ForegroundColor Red
                $issues += "$($prereq.Name) is required but not installed"
            }
            else {
                Write-Host "  $($prereq.Name): Not found (optional)" -ForegroundColor Yellow
            }
        }
    }
    elseif ($prereq.Check) {
        if (& $prereq.Check) {
            Write-Host "  $($prereq.Name): OK" -ForegroundColor Green
        }
        else {
            Write-Host "  $($prereq.Name): Failed" -ForegroundColor Red
            $issues += "$($prereq.Name) requirement not met"
        }
    }
}

# Check permissions
Write-Host ""
Write-Host "[PERMISSIONS] Checking file system permissions..." -ForegroundColor Yellow

try {
    $testFile = "$env:APPDATA\Claude\test_write_permission.tmp"
    "test" | Out-File $testFile -Force
    Remove-Item $testFile -Force
    Write-Host "  Can write to Claude config directory" -ForegroundColor Green
}
catch {
    Write-Host "  Cannot write to Claude config directory" -ForegroundColor Red
    $issues += "No write permission for Claude configuration"
}

# Summary
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "                           VERIFICATION SUMMARY                             " -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

if ($issues.Count -eq 0) {
    Write-Host "STATUS: READY FOR INSTALLATION" -ForegroundColor Green -BackgroundColor DarkGreen
    Write-Host ""

    if ($warnings.Count -gt 0) {
        Write-Host "Warnings:" -ForegroundColor Yellow
        $warnings | ForEach-Object {
            Write-Host "  ! $_" -ForegroundColor Yellow
        }
        Write-Host ""
    }

    Write-Host "Recommendations:" -ForegroundColor Cyan
    Write-Host "  1. Run backup script first: .\backup_mcps.ps1" -ForegroundColor White
    Write-Host "  2. Close Claude Desktop if running" -ForegroundColor White
    Write-Host "  3. Run installer: ..\installer.ps1" -ForegroundColor White
}
else {
    Write-Host "STATUS: NOT READY FOR INSTALLATION" -ForegroundColor Red -BackgroundColor DarkRed
    Write-Host ""

    Write-Host "Critical Issues:" -ForegroundColor Red
    $issues | ForEach-Object {
        Write-Host "  X $_" -ForegroundColor Red
    }
    Write-Host ""

    Write-Host "Please resolve these issues before installation." -ForegroundColor Yellow
}

Write-Host ""