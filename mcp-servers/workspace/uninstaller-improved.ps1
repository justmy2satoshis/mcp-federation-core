# MCP Federation Core - Improved Uninstaller Script v3.2.1
# Better detection of MCP name variations
# Preserves user configurations while removing Federation MCPs

param(
    [ValidateSet("selective", "full", "check")]
    [string]$Mode = "selective",
    [switch]$WhatIf,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "                  MCP FEDERATION CORE UNINSTALLER v3.2.1                    " -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$mcpBasePath = "$env:USERPROFILE\mcp-servers"
$backupDir = "$mcpBasePath\backups\uninstall_$(Get-Date -Format 'yyyyMMdd_HHmmss')"

# Define Federation MCPs with all known name variations
$federationMCPVariations = @{
    'sqlite' = @('sqlite', 'sqlite-data-warehouse', 'sqlite-mcp', 'sqlite_mcp')
    'expert-role-prompt' = @('expert-role-prompt', 'expert_role_prompt', 'expert-role')
    'kimi-k2-resilient-enhanced' = @('kimi-k2-resilient-enhanced', 'kimi-k2-resilient', 'kimi_k2_resilient', 'kimi-k2-resilient-mcp')
    'kimi-k2-code-context-enhanced' = @('kimi-k2-code-context-enhanced', 'kimi-k2-code-context', 'kimi_k2_code_context', 'kimi-k2-code')
    'rag-context' = @('rag-context', 'rag_context', 'rag-context-fixed', 'rag-context-mcp')
    'converse' = @('converse', 'converse-mcp', 'converse_mcp')
    'web-search' = @('web-search', 'web_search', 'brave-search', 'web-search-mcp')
    'github-manager' = @('github-manager', 'github_manager', 'github', 'github-mcp')
    'memory' = @('memory', 'memory-mcp', 'memory_mcp', 'knowledge-graph')
    'filesystem' = @('filesystem', 'filesystem-mcp', 'file-system', 'file_system')
    'desktop-commander' = @('desktop-commander', 'desktop_commander', 'desktop-cmd')
    'perplexity' = @('perplexity', 'perplexity-mcp', 'perplexity_mcp')
    'playwright' = @('playwright', 'playwright-mcp', 'playwright_mcp', 'browser-automation')
    'git-ops' = @('git-ops', 'git_ops', 'gitops', 'git-operations')
    'sequential-thinking' = @('sequential-thinking', 'sequential_thinking', 'seq-thinking')
}

# Function to check if MCP is a Federation MCP
function Test-FederationMCP {
    param([string]$MCPName)

    foreach ($variations in $federationMCPVariations.Values) {
        if ($MCPName -in $variations) {
            return $true
        }
    }
    return $false
}

# Function to get canonical Federation MCP name
function Get-CanonicalMCPName {
    param([string]$MCPName)

    foreach ($canonical in $federationMCPVariations.Keys) {
        $variations = $federationMCPVariations[$canonical]
        if ($MCPName -in $variations) {
            return $canonical
        }
    }
    return $null
}

# Check mode
if ($Mode -eq "check") {
    Write-Host "[CHECK MODE] Analyzing current MCP configuration..." -ForegroundColor Yellow
    Write-Host ""

    if (-not (Test-Path $configPath)) {
        Write-Host "No Claude Desktop configuration found." -ForegroundColor Red
        exit 0
    }

    try {
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
        $allMCPs = @()
        $federationMCPs = @()
        $userMCPs = @()

        if ($config.mcpServers) {
            $allMCPs = $config.mcpServers.PSObject.Properties.Name

            foreach ($mcp in $allMCPs) {
                if (Test-FederationMCP -MCPName $mcp) {
                    $canonical = Get-CanonicalMCPName -MCPName $mcp
                    $federationMCPs += @{
                        Installed = $mcp
                        Canonical = $canonical
                    }
                }
                else {
                    $userMCPs += $mcp
                }
            }
        }

        Write-Host "MCP Configuration Analysis:" -ForegroundColor Cyan
        Write-Host "  Total MCPs: $($allMCPs.Count)" -ForegroundColor White
        Write-Host ""

        if ($federationMCPs.Count -gt 0) {
            Write-Host "Federation MCPs Found: $($federationMCPs.Count) of 15" -ForegroundColor Yellow
            foreach ($fmcp in $federationMCPs) {
                Write-Host "  - $($fmcp.Installed)" -ForegroundColor Yellow
                if ($fmcp.Installed -ne $fmcp.Canonical) {
                    Write-Host "    (Canonical name: $($fmcp.Canonical))" -ForegroundColor Gray
                }
            }
        }
        else {
            Write-Host "No Federation MCPs found" -ForegroundColor Green
        }

        if ($userMCPs.Count -gt 0) {
            Write-Host ""
            Write-Host "User MCPs (will be preserved): $($userMCPs.Count)" -ForegroundColor Green
            foreach ($umcp in $userMCPs) {
                Write-Host "  + $umcp" -ForegroundColor Green
            }
        }

        # Check for missing Federation MCPs
        $missingCount = 15 - $federationMCPs.Count
        if ($missingCount -gt 0) {
            Write-Host ""
            Write-Host "Missing Federation MCPs: $missingCount" -ForegroundColor Gray

            $installedCanonical = $federationMCPs | ForEach-Object { $_.Canonical } | Select-Object -Unique
            $allCanonical = $federationMCPVariations.Keys

            foreach ($canonical in $allCanonical) {
                if ($canonical -notin $installedCanonical) {
                    Write-Host "  ? $canonical (not installed)" -ForegroundColor Gray
                }
            }
        }
    }
    catch {
        Write-Host "Error reading configuration: $_" -ForegroundColor Red
    }

    exit 0
}

# Backup configuration
if (Test-Path $configPath) {
    Write-Host "[BACKUP] Creating configuration backup..." -ForegroundColor Yellow

    New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
    $backupFile = Join-Path $backupDir "claude_desktop_config.json"
    Copy-Item $configPath $backupFile -Force

    Write-Host "  Backup saved: $backupFile" -ForegroundColor Green
}

# Load configuration
Write-Host ""
Write-Host "[ANALYSIS] Loading MCP configuration..." -ForegroundColor Yellow

if (-not (Test-Path $configPath)) {
    Write-Host "  No configuration file found. Nothing to uninstall." -ForegroundColor Yellow
    exit 0
}

try {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
}
catch {
    Write-Host "  Error reading configuration: $_" -ForegroundColor Red
    exit 1
}

if (-not $config.mcpServers) {
    Write-Host "  No MCPs configured. Nothing to uninstall." -ForegroundColor Yellow
    exit 0
}

# Analyze MCPs
$mcpsToRemove = @()
$mcpsToKeep = @()
$allMCPs = $config.mcpServers.PSObject.Properties.Name

foreach ($mcp in $allMCPs) {
    if ($Mode -eq "full") {
        $mcpsToRemove += $mcp
    }
    elseif ($Mode -eq "selective") {
        if (Test-FederationMCP -MCPName $mcp) {
            $mcpsToRemove += $mcp
        }
        else {
            $mcpsToKeep += $mcp
        }
    }
}

Write-Host "  Total MCPs: $($allMCPs.Count)" -ForegroundColor White
Write-Host "  Federation MCPs to remove: $($mcpsToRemove.Count)" -ForegroundColor Yellow
Write-Host "  User MCPs to preserve: $($mcpsToKeep.Count)" -ForegroundColor Green

# Confirm removal
if ($mcpsToRemove.Count -eq 0) {
    Write-Host ""
    Write-Host "No Federation MCPs found to remove." -ForegroundColor Green
    exit 0
}

Write-Host ""
Write-Host "[REMOVAL] MCPs to be removed:" -ForegroundColor Yellow
$mcpsToRemove | ForEach-Object {
    $canonical = Get-CanonicalMCPName -MCPName $_
    Write-Host "  - $_" -ForegroundColor Red
    if ($canonical -and $_ -ne $canonical) {
        Write-Host "    (Federation MCP: $canonical)" -ForegroundColor Gray
    }
}

if ($mcpsToKeep.Count -gt 0) {
    Write-Host ""
    Write-Host "[PRESERVE] MCPs to keep:" -ForegroundColor Green
    $mcpsToKeep | ForEach-Object {
        Write-Host "  + $_" -ForegroundColor Green
    }
}

if (-not $Force -and -not $WhatIf) {
    Write-Host ""
    $confirm = Read-Host "Continue with removal? (yes/no)"
    if ($confirm -ne "yes") {
        Write-Host "Uninstallation cancelled" -ForegroundColor Red
        exit 0
    }
}

if ($WhatIf) {
    Write-Host ""
    Write-Host "[WHATIF] No changes will be made" -ForegroundColor Yellow
    exit 0
}

# Remove MCPs from configuration
Write-Host ""
Write-Host "[REMOVING] Removing Federation MCPs from configuration..." -ForegroundColor Yellow

foreach ($mcp in $mcpsToRemove) {
    $config.mcpServers.PSObject.Properties.Remove($mcp)
    Write-Host "  Removed: $mcp" -ForegroundColor Red
}

# Save updated configuration
Write-Host ""
Write-Host "[SAVING] Writing updated configuration..." -ForegroundColor Yellow

$config | ConvertTo-Json -Depth 10 | Set-Content $configPath -Encoding UTF8
Write-Host "  Configuration updated" -ForegroundColor Green

# Clean up Federation files
Write-Host ""
Write-Host "[CLEANUP] Removing Federation files..." -ForegroundColor Yellow

$federationDirs = @(
    "$mcpBasePath\installers\unified",
    "$mcpBasePath\mcp-federation-core",
    "$mcpBasePath\federation-backup"
)

foreach ($dir in $federationDirs) {
    if (Test-Path $dir) {
        try {
            Remove-Item $dir -Recurse -Force
            Write-Host "  Removed: $dir" -ForegroundColor Red
        }
        catch {
            Write-Host "  Failed to remove: $dir" -ForegroundColor Yellow
        }
    }
}

# Remove database if requested
$dbPath = "$mcpBasePath\mcp-unified.db"
if (Test-Path $dbPath) {
    if ($Mode -eq "full" -or $Force) {
        Remove-Item $dbPath -Force
        Write-Host "  Removed: mcp-unified.db" -ForegroundColor Red
    }
    else {
        Write-Host "  Preserved: mcp-unified.db" -ForegroundColor Gray
    }
}

# Summary
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "                         UNINSTALLATION COMPLETE                            " -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  MCPs removed: $($mcpsToRemove.Count)" -ForegroundColor Red
Write-Host "  MCPs preserved: $($mcpsToKeep.Count)" -ForegroundColor Green
Write-Host "  Backup location: $backupDir" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Restart Claude Desktop to apply changes" -ForegroundColor White
Write-Host "  2. To restore, use backup at: $backupDir" -ForegroundColor White
Write-Host ""